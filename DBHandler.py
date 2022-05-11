import datetime

from notion_client import Client


class DBHandler:
    def __init__(self, notion_token: str):
        self.notion_token = notion_token
        self.notion = Client(auth=self.notion_token)
        self.today = datetime.datetime.today()

    def get_doing_task_db(self, db_id: str):
        db = self.notion.databases.query(
            **{
                'database_id': db_id,
                "filter": {
                    "and": [
                        {
                            "property": "期限",
                            "select": {
                                "does_not_equal": 'Done'
                            }
                        }
                    ]
                }
            }
        )
        return db['results']

    def get_done_task_db(self, db_id: str):
        db = self.notion.databases.query(
            **{
                'database_id': db_id,
                "filter": {
                    "and": [
                        {
                            "property": "期限",
                            "select": {
                                "equals": 'Done'
                            }
                        },
                        {
                            "property": "完了日時",
                            "date": {
                                "is_empty": True
                            }
                        }

                    ]
                }
            }
        )
        return db['results']

    def update_task_date(self, page_id: str) -> None:
        today = str(datetime.datetime.now().isoformat())
        self.notion.pages.update(
            page_id,
            properties={
                '完了日時': {
                    'date': {
                        'start': today,
                        'time_zone': 'Asia/Tokyo'
                    }
                }
            }
        )

    def update_task_status(self, page_id: str, priority: str, deadline: str) -> None:
        self.notion.pages.update(
            page_id,
            properties={
                'Priority': {
                    'select': {
                        'name': priority
                    }
                },
                '期限': {
                    'select': {
                        'name': deadline
                    }
                }
            }
        )

    def get_task_priority(self, deadline_date) -> str:
        # 3日以内の場合は、高
        # 3日以上7日以内の場合は、中
        # 7日以上の場合は、低
        if deadline_date is None:
            return '低'
        if deadline_date <= self.today + datetime.timedelta(days=3):
            return '高'
        elif self.today + datetime.timedelta(days=3) < deadline_date <= self.today + datetime.timedelta(days=7):
            return '中'
        else:
            return '低'

    def get_task_deadline(self, deadline_date) -> str:
        # 1日以内の場合は、dau
        # 2日以上7日以内の場合は、week
        # 7日以上の場合は、none

        if deadline_date is None:
            return 'none'
        if deadline_date <= self.today + datetime.timedelta(days=1):
            return 'day'
        elif deadline_date <= self.today + datetime.timedelta(days=7):
            return 'week'
        else:
            return 'none'

    @staticmethod
    def get_page_id(db_result) -> str:
        return db_result['id']

    @staticmethod
    def get_task_deadline_date(db_result):
        if db_result['properties']['期日']['date'] is None:
            return None
        else:
            return datetime.datetime.strptime(db_result['properties']['期日']['date']['start'], '%Y-%m-%d')
