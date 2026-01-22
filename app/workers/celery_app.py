from celery import Celery

# Create Celery application instance
celery_app = Celery(
    "ai_business_analyst",
    broker="redis://localhost:6379/0",   # Message broker
    backend="redis://localhost:6379/1",  # Result backend
)

# Basic Celery configuration
celery_app.conf.update(
    task_track_started=True,   # Track task state
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)
