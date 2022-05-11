import datetime

from notion_client import Client


class DBHandler:
    def __init__(self, notion_token: str):
        self.notion_token = notion_token
        self.notion = Client(auth=self.notion_token)

    def get_done_task_db(self, db_id: str) -> dict:
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
                            "property": "日付",
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
                '日付': {
                    'date': {
                        'start': today,
                        'time_zone': 'Asia/Tokyo'
                    }
                }
            }
        )

    @staticmethod
    def get_page_id(db_result) -> str:
        return db_result['id']
