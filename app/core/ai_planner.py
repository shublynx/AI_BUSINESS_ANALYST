# app/core/ai_planner.py

import json
from openai import OpenAI
from app.config import settings

# Use Groq OpenAI-compatible endpoint
client = OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


def generate_plan(question: str, metadata: dict) -> dict:
    """
    Uses LLM to convert natural language question
    into structured query intent.
    """

    system_prompt = """
You are a data analysis planner.

Your job is to convert a user question into structured JSON.

Return ONLY valid JSON.
Do not add explanations.

Available operations:
- aggregate
- filter
- compare

For aggregate, include:
- aggregation (sum, mean, max, min, count)
- group_by (column name or null)
- target_column (numeric column)
- ranking (max or min or null)

Use column names exactly as provided.
"""

    user_prompt = f"""
Dataset metadata:
{json.dumps(metadata)}

Question:
{question}
"""

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,  # from config
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except Exception:
        raise ValueError(f"LLM returned invalid JSON:\n{content}")
