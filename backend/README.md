fast api: uvicorn app.main:app --port 8000 --reload
celery: celery -A app.worker.celery_app worker --loglevel=info
