import os
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models.dataset import Dataset

from app.workers.process_dataset import process_dataset  # Import the background task

UPLOAD_DIR = "storage/uploads"  # Directory to store uploaded files

router = APIRouter(
    prefix="/datasets",          # Base path for dataset APIs
    tags=["datasets"]            # Swagger grouping
)


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
)
def upload_dataset(
    file: UploadFile = File(...),  # File received via multipart/form-data
):
    """
    Handles dataset upload and creates an ingestion record.
    """

    # Reject requests without a valid filename
    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid file")

    # Extract and validate file extension
    extension = file.filename.split(".")[-1].lower()
    if extension not in {"csv", "xlsx"}:
        raise HTTPException(
            status_code=400,
            detail="Only CSV or Excel files are supported",
        )

    # Create upload directory if it does not exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Build absolute file path for storage
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Stream uploaded file content to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Open database session
    db: Session = SessionLocal()
    try:
        dataset = Dataset(
            filename=file.filename,   # Store original filename
            status="uploaded",        # Mark dataset as ready for processing
        )
        db.add(dataset)              # Stage the dataset object
        db.commit()                  # Persist the transaction
        db.refresh(dataset)          # Load generated fields (id, timestamps)

        # Start dataset processing in the background
        process_dataset.delay(dataset.id)
        
    finally:
        db.close()                   # Always release DB connection

    # Return minimal reference for client-side tracking
    return {
        "dataset_id": dataset.id,
        "filename": dataset.filename,
        "status": dataset.status,
    }
# End of file app/api/datasets.py