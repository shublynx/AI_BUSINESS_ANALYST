# app/api/query.py

from fastapi import APIRouter, HTTPException, Query
import pandas as pd
import os
import json

from app.db import SessionLocal
from app.models.dataset import Dataset
from app.core.ai_planner import generate_plan
from app.core.query_engine import execute_plan


router = APIRouter(prefix="/query", tags=["query"])


@router.post("/{dataset_id}")
def query_dataset(
    dataset_id: str,
    question: str = Query(..., description="User natural language question"),
):
    """
    Phase 5:
    Uses AI planner to convert user question into structured query plan.
    Then executes plan safely using deterministic engine.
    """

    # 🔎 1️⃣ Fetch dataset from DB
    db = SessionLocal()
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    db.close()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # 📁 2️⃣ Locate file
    file_path = f"storage/uploads/{dataset.filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # 📊 3️⃣ Load dataset safely
    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load dataset: {str(e)}")

    # 🧹 4️⃣ Normalize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # 📦 5️⃣ Load metadata
    if not dataset.dataset_metadata:
        raise HTTPException(
            status_code=400,
            detail="Dataset metadata not available. Ensure background processing completed.",
        )

    metadata = (
        dataset.dataset_metadata
        if isinstance(dataset.dataset_metadata, dict)
        else json.loads(dataset.dataset_metadata)
    )

    # 🧠 6️⃣ AI Planner decides what to do
    try:
        plan = generate_plan(question, metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM planning failed: {str(e)}")

    # ⚙️ 7️⃣ Deterministic execution
    try:
        answer = execute_plan(df, plan)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Execution failed: {str(e)}")

    # 📤 8️⃣ Return structured response
    return {
        "dataset_id": dataset_id,
        "question": question,
        "plan": plan,
        "answer": answer,
    }
