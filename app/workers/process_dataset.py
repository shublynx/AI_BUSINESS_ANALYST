import os
import pandas as pd

from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.dataset import Dataset
from app.workers.celery_app import celery_app
from app.core.data_utils import normalize_column
from app.core.metadata import extract_metadata

UPLOAD_DIR = "storage/uploads"


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def process_dataset(self, dataset_id: str):
    db: Session = SessionLocal()

    try:
        dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
        if not dataset:
            raise ValueError(f"Dataset {dataset_id} not found")

        # 1️⃣ Transition to processing
        dataset.status = "processing"
        db.commit()

        # 2️⃣ Load file
        file_path = os.path.join(UPLOAD_DIR, dataset.filename)

        if dataset.filename.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif dataset.filename.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format")

        # 3️⃣ Normalize column names
        original_columns = df.columns.tolist()
        df.columns = [normalize_column(c) for c in df.columns]

        # 4️⃣ Extract metadata AFTER normalization
        metadata = extract_metadata(df)

        # Optional debug logging
        print("Original columns:", original_columns)
        print("Normalized columns:", df.columns.tolist())

        # 5️⃣ Persist results
        dataset.dataset_metadata = metadata
        dataset.status = "completed"
        db.commit()

    except Exception as exc:
        db.rollback()
        if "dataset" in locals():
            dataset.status = "failed"
            db.commit()
        raise exc

    finally:
        db.close()
