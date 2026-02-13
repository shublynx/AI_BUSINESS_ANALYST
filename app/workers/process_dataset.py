import pandas as pd
import json
import os

from app.workers.celery_app import celery_app
from app.db import SessionLocal
from app.models.dataset import Dataset
from app.core.metadata import extract_metadata


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def process_dataset(self, dataset_id: str):

    db = SessionLocal()
    try:
        dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

        if not dataset:
            return

        file_path = f"storage/uploads/{dataset.filename}"

        if not os.path.exists(file_path):
            dataset.status = "failed"
            db.commit()
            return

        # Load file
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            dataset.status = "failed"
            db.commit()
            return

        # Normalize column names
        df.columns = df.columns.str.lower().str.replace(" ", "_")

        # Extract metadata
        metadata = extract_metadata(df)

        # SAVE metadata in DB  ✅ THIS IS CRITICAL
        dataset.dataset_metadata = json.dumps(metadata)

        # Mark dataset completed
        dataset.status = "completed"

        db.commit()

    finally:
        db.close()
