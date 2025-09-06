# backend/app/worker/tasks.py

import uuid
from app.worker.celery_app import celery
from app.research_agent.graph import agent_app
from app.db.session import SyncSessionLocal
from app.db.crud import get_task_sync, update_task_status_sync, create_report_sync
from app.db.crud import create_task_log_sync

# --- REVERT THE DECORATOR AND SIGNATURE ---
@celery.task(throws=(Exception,)) # <-- Add throws=(Exception,)
def run_research_agent(task_id: str): # <-- Remove self and bind=True
    """
    The main Celery task to run the research agent graph.
    """
    db = SyncSessionLocal()
    task_id_uuid = uuid.UUID(task_id)

    try:
        task = get_task_sync(db, task_id_uuid)
        if not task:
            print(f"Task {task_id} not found.")
            return

        create_task_log_sync(db, task_id_uuid, f"Starting research agent for query: '{task.query}'")
        update_task_status_sync(db, task_id_uuid, "IN_PROGRESS")

        initial_state = {
            "task_id": task_id_uuid,
            "db": db, # <-- Pass the db session into the state
            "query": task.query,
            "subreddits": ["SomebodyMakeThis", "startups", "Entrepreneur"]
        }

        final_state = agent_app.invoke(initial_state)
        final_report = final_state.get("final_report", "Error: Report not generated.")

        create_report_sync(db, task_id_uuid, final_report)
        update_task_status_sync(db, task_id_uuid, "COMPLETED")
        print(f"Task {task_id} completed successfully.")

    except Exception as e:
        print(f"Error processing task {task_id}: {e}")
        update_task_status_sync(db, task_id_uuid, "FAILED")
        create_task_log_sync(db, task_id_uuid, f"Error processing task: {e}")
        # --- REMOVE raise e; let the decorator handle it ---
        raise # Using `raise` by itself re-raises the caught exception
        
    finally:
        db.close()

    return {"task_id": str(task_id_uuid), "status": "COMPLETED"}