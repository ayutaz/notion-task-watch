import datetime
from typing import Any, Optional

from notion_client import Client


class DBHandler:
    def __init__(self, notion_token: Optional[str]):
        self.notion_token = notion_token
        self.notion = Client(auth=self.notion_token)
        self.today = datetime.datetime.today()

    def query_database(self, db_id: str, query_filter: dict) -> list:
        # Notion APIは1回のクエリで最大100件しか返さないため、全ページを取得する
        results: list = []
        kwargs: dict = {"filter": query_filter}
        while True:
            response: Any = self.notion.databases.query(db_id, **kwargs)
            results.extend(response['results'])
            if not response.get('has_more') or not response.get('next_cursor'):
                return results
            kwargs["start_cursor"] = response['next_cursor']

    def get_doing_task_db(self, db_id: str) -> list:
        return self.query_database(
            db_id,
            {
                "and": [
                    {
                        "property": "期限",
                        "select": {
                            "does_not_equal": 'Done'
                        }
                    }
                ]
            }
        )

    def get_done_task_db(self, db_id: str) -> list:
        return self.query_database(
            db_id,
            {
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
        )

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
        # 1日以内の場合は、day
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
    def get_select_name(db_result, property_name: str) -> Optional[str]:
        select = (db_result['properties'].get(property_name) or {}).get('select')
        if select is None:
            return None
        return select.get('name')

    @staticmethod
    def get_task_deadline_date(db_result):
        if db_result['properties']['期日']['date'] is None:
            return None
        else:
            # 時刻付きの期日 (例: 2022-05-11T10:00:00.000+09:00) でも日付部分のみで判定する
            start = db_result['properties']['期日']['date']['start']
            return datetime.datetime.strptime(start[:10], '%Y-%m-%d')
