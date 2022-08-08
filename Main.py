import os

from dotenv import load_dotenv

from DBHandler import DBHandler

load_dotenv()


def TaskDoneWatch(db_id) -> None:
    results = db_handler.get_done_task_db(db_id)
    for idx in range(len(results)):
        page_id = db_handler.get_page_id(results[idx])
        db_handler.update_task_date(page_id)


def TaskPriorityWatch(db_id) -> None:
    results = db_handler.get_doing_task_db(db_id)
    for idx in range(len(results)):
        page_id = db_handler.get_page_id(results[idx])
        deadline_data = db_handler.get_task_deadline_date(results[idx])
        new_task_priority = db_handler.get_task_priority(deadline_data)
        new_task_deadline = db_handler.get_task_deadline(deadline_data)
        db_handler.update_task_status(page_id, new_task_priority, new_task_deadline)


def TaskWatch(db_id) -> None:
    TaskDoneWatch(db_id)
    TaskPriorityWatch(db_id)


db_handler = DBHandler(os.getenv("NOTION_TOKEN"))

TaskWatch(os.getenv("PRIVATE_DB"))
TaskWatch(os.getenv("WORK_DB"))
TaskWatch(os.getenv("SIDEWORK_DB"))
