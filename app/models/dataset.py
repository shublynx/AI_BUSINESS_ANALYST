import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from app.db import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    filename = Column(String, nullable=False)

    status = Column(
        String,
        nullable=False,
        default="uploaded"
    )

    
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
