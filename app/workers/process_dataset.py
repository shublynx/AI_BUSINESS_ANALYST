from celery.utils.log import get_task_logger
from app.workers.celery_app import celery_app
from app.db import SessionLocal
from app.models.dataset import Dataset

logger = get_task_logger(__name__)


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def process_dataset(self, dataset_id: str):
    """
    Background task that processes an uploaded dataset.
    """

    db = SessionLocal()  # Open DB session
    try:
        dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

        if not dataset:
            logger.error(f"Dataset not found: {dataset_id}")
            return

        dataset.status = "processing"   # Mark job as started
        db.commit()

        # ---- SIMULATED WORK (placeholder) ----
        # Later: CSV parsing, cleaning, EDA, embeddings
        import time
        time.sleep(3)
        # --------------------------------------

        dataset.status = "completed"    # Mark job as completed
        db.commit()

    except Exception as e:
        dataset.status = "failed"       # Mark job as failed
        dataset.error_message = str(e)  # Store failure reason
        db.commit()
        raise                            # Triggers retry

    finally:
        db.close()                      # Release DB connection
