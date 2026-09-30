import datetime
import unittest
from unittest import mock

import Main
from DBHandler import DBHandler


def make_task(page_id, due=None, priority=None, deadline=None):
    return {
        "id": page_id,
        "properties": {
            "期日": {"date": None if due is None else {"start": due}},
            "Priority": {"select": None if priority is None else {"name": priority}},
            "期限": {"select": None if deadline is None else {"name": deadline}},
        },
    }


class DBHandlerTests(unittest.TestCase):
    def setUp(self):
        self.handler = DBHandler("dummy-token")
        self.handler.notion = mock.MagicMock()
        self.handler.today = datetime.datetime(2024, 5, 10, 15, 0)

    def test_deadline_date_accepts_date_and_datetime_values(self):
        expected = datetime.datetime(2024, 5, 11)
        self.assertEqual(self.handler.get_task_deadline_date(make_task("a", "2024-05-11")), expected)
        self.assertEqual(
            self.handler.get_task_deadline_date(make_task("a", "2024-05-11T10:00:00.000+09:00")),
            expected,
        )
        self.assertIsNone(self.handler.get_task_deadline_date(make_task("a")))

    def test_priority_and_deadline_thresholds(self):
        def day(offset):
            return datetime.datetime(2024, 5, 10) + datetime.timedelta(days=offset)

        self.assertEqual(self.handler.get_task_priority(day(3)), "高")
        self.assertEqual(self.handler.get_task_priority(day(5)), "中")
        self.assertEqual(self.handler.get_task_priority(day(8)), "低")
        self.assertEqual(self.handler.get_task_priority(None), "低")
        self.assertEqual(self.handler.get_task_deadline(day(1)), "day")
        self.assertEqual(self.handler.get_task_deadline(day(2)), "week")
        self.assertEqual(self.handler.get_task_deadline(day(8)), "none")
        self.assertEqual(self.handler.get_task_deadline(None), "none")

    def test_query_database_follows_pagination(self):
        self.handler.notion.databases.query.side_effect = [
            {"results": [{"id": "1"}], "has_more": True, "next_cursor": "cursor-1"},
            {"results": [{"id": "2"}], "has_more": False, "next_cursor": None},
        ]

        results = self.handler.get_doing_task_db("db-id")

        self.assertEqual([result["id"] for result in results], ["1", "2"])
        calls = self.handler.notion.databases.query.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertNotIn("start_cursor", calls[0].kwargs)
        self.assertEqual(calls[1].kwargs["start_cursor"], "cursor-1")
        self.assertEqual(calls[1].args, ("db-id",))


class TaskPriorityWatchTests(unittest.TestCase):
    def test_updates_only_tasks_whose_values_change(self):
        handler = DBHandler("dummy-token")
        handler.today = datetime.datetime(2024, 5, 10, 15, 0)
        handler.notion = mock.MagicMock()
        handler.notion.databases.query.return_value = {
            "results": [
                make_task("unchanged", "2024-05-11", priority="高", deadline="day"),
                make_task("changed", "2024-05-11", priority="低", deadline="none"),
            ],
            "has_more": False,
            "next_cursor": None,
        }

        with mock.patch.object(Main, "db_handler", handler):
            Main.TaskPriorityWatch("db-id")

        handler.notion.pages.update.assert_called_once()
        self.assertEqual(handler.notion.pages.update.call_args.args, ("changed",))


if __name__ == "__main__":
    unittest.main()
