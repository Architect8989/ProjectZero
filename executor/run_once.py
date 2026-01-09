import time
import hashlib
import requests
from pathlib import Path

import pyautogui
from mss import mss

# -----------------------------
# CONFIG
# -----------------------------
BACKEND_URL = "http://127.0.0.1:8000"
OUT_DIR = Path(__file__).parent / "artifacts"
OUT_DIR.mkdir(parents=True, exist_ok=True)

pyautogui.FAILSAFE = True  # move mouse to corner to abort


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


def post_json(url: str, payload: dict):
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()
    return r.json()


def post_params(url: str, params: dict):
    r = requests.post(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()


# -----------------------------
# MAIN (ONE-SHOT EXECUTION)
# -----------------------------
def main():
    # 1) Start execution
    exec_resp = post_json(f"{BACKEND_URL}/executions/start", {
        "environment": "local-os-demo"
    })
    execution_id = exec_resp["id"]

    # 2) BEFORE screenshot
    before_path = OUT_DIR / "before.png"
    capture_screen(before_path)
    before_hash = sha256(before_path)

    post_json(f"{BACKEND_URL}/observations", {
        "execution_id": execution_id,
        "storage_uri": str(before_path),
        "checksum": before_hash
    })

    time.sleep(0.5)

    # 3) ONE real OS action (deterministic)
    # NOTE: choose coordinates that safely cause a visible change
    # Example: click somewhere neutral or open a menu
    pyautogui.moveTo(400, 400, duration=0.4)
    pyautogui.click()

    time.sleep(0.5)

    # 4) AFTER screenshot
    after_path = OUT_DIR / "after.png"
    capture_screen(after_path)
    after_hash = sha256(after_path)

    post_json(f"{BACKEND_URL}/observations", {
        "execution_id": execution_id,
        "storage_uri": str(after_path),
        "checksum": after_hash
    })

    # 5) (Optional) Delta artifact (hash-only MVP)
    # For MVP, storing both frames + hashes is sufficient proof.
    # If you want a real pixel-delta image later, add it here.
    post_json(f"{BACKEND_URL}/artifacts", {
        "execution_id": execution_id,
        "artifact_type": "delta",
        "storage_uri": "before->after",
        "checksum": f"{before_hash}:{after_hash}"
    })

    # 6) Complete execution (seal)
    post_params(
        f"{BACKEND_URL}/executions/{execution_id}/complete",
        {"success": True}
    )

    print(f"[OK] Execution completed: {execution_id}")
    print(f"[OK] Artifacts saved to: {OUT_DIR}")


if __name__ == "__main__":
    main()
