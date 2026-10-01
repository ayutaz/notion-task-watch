import os

from dotenv import load_dotenv

from DBHandler import DBHandler

load_dotenv()

DB_ENVIRONMENT_NAMES = ("PRIVATE_DB", "WORK_DB", "SIDEWORK_DB")


def TaskDoneWatch(db_id) -> None:
    results = db_handler.get_done_task_db(db_id)
    for result in results:
        page_id = db_handler.get_page_id(result)
        db_handler.update_task_date(page_id)


def TaskPriorityWatch(db_id) -> None:
    results = db_handler.get_doing_task_db(db_id)
    for result in results:
        page_id = db_handler.get_page_id(result)
        deadline_data = db_handler.get_task_deadline_date(result)
        new_task_priority = db_handler.get_task_priority(deadline_data)
        new_task_deadline = db_handler.get_task_deadline(deadline_data)
        # 値が変わらないタスクは更新しない (API呼び出し回数を抑える)
        if (db_handler.get_select_name(result, 'Priority') == new_task_priority
                and db_handler.get_select_name(result, '期限') == new_task_deadline):
            continue
        db_handler.update_task_status(page_id, new_task_priority, new_task_deadline)


def TaskWatch(db_id) -> None:
    TaskDoneWatch(db_id)
    TaskPriorityWatch(db_id)


db_handler = DBHandler(os.getenv("NOTION_TOKEN"))

if __name__ == "__main__":
    for environment_name in DB_ENVIRONMENT_NAMES:
        database_id = os.getenv(environment_name)
        if not database_id:
            print(f"{environment_name} is not set. skip.")
            continue
        TaskWatch(database_id)
