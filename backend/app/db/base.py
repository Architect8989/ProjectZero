from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.

    - No logic
    - No side effects
    - Only metadata and table declarations

    All domain models must inherit from this class.
    """
    pass
