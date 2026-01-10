import time
import hashlib
import requests
import sys
from pathlib import Path

import pyautogui
import numpy as np
from PIL import Image
from mss import mss

# -----------------------------
# CONFIG
# -----------------------------
BACKEND_URL = "http://127.0.0.1:8000"
OUT_DIR = Path(__file__).parent / "artifacts"
OUT_DIR.mkdir(parents=True, exist_ok=True)

pyautogui.FAILSAFE = False


# -----------------------------
# UTILS
# -----------------------------
def capture_screen(path: Path) -> None:
    with mss() as sct:
        sct.shot(output=str(path))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def pixel_delta(a: Path, b: Path) -> int:
    A = np.asarray(Image.open(a))
    B = np.asarray(Image.open(b))

    if A.shape != B.shape:
        return -1

    diff = np.abs(A.astype(np.int16) - B.astype(np.int16))
    return int(np.count_nonzero(diff))


def post_json(url: str, payload: dict):
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()
    return r.json()


def post_params(url: str, params: dict):
    r = requests.post(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()


# -----------------------------
# MAIN (CRE EXECUTION)
# -----------------------------
def main():
    exec_resp = post_json(f"{BACKEND_URL}/executions/start", {
        "environment": "local-os-demo"
    })
    execution_id = exec_resp["id"]

    before_path = OUT_DIR / "before.png"
    capture_screen(before_path)
    before_hash = sha256(before_path)

    post_json(f"{BACKEND_URL}/observations", {
        "execution_id": execution_id,
        "storage_uri": str(before_path),
        "checksum": before_hash
    })

    time.sleep(0.5)

    # ---- REAL OS ACTION ----
    w, h = pyautogui.size()
    x, y = w // 2, h // 2
    pyautogui.moveTo(x, y, duration=0.3)
    pyautogui.click()
    time.sleep(0.3)
    pyautogui.hotkey("alt", "f1")

    time.sleep(0.7)

    after_path = OUT_DIR / "after.png"
    capture_screen(after_path)
    after_hash = sha256(after_path)

    changed_pixels = pixel_delta(before_path, after_path)
    if changed_pixels <= 0:
        print("CRE FAILURE: no causal pixel change detected")
        sys.exit(1)

    post_json(f"{BACKEND_URL}/observations", {
        "execution_id": execution_id,
        "storage_uri": str(after_path),
        "checksum": after_hash
    })

    post_json(f"{BACKEND_URL}/artifacts", {
        "execution_id": execution_id,
        "artifact_type": "pixel_delta",
        "storage_uri": "before->after",
        "checksum": f"{before_hash}:{after_hash}"
    })

    post_params(
        f"{BACKEND_URL}/executions/{execution_id}/complete",
        {"success": True, "pixels_changed": changed_pixels}
    )

    print("CRE VERIFIED")
    print(f"pixels_changed: {changed_pixels}")
    print("action: real_os_input")
    print("process: terminated")
    sys.exit(0)


if __name__ == "__main__":
    main()
