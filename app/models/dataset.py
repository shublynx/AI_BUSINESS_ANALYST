import uuid
from sqlalchemy import Column, String, DateTime, Text
from app.db import Base
from datetime import datetime, timezone


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=False)

    # ingestion lifecycle
    status = Column(String, nullable=False, default="uploaded")

    # error visibility (important for debugging + UI)
    error_message = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        onupdate=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )
