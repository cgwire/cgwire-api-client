import unittest
import json
import requests_mock

import gazu


class TaskTestCase(unittest.TestCase):

    def test_all_for_shot(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url('data/assets/asset-01/tasks'),
                text=json.dumps([
                    {"id": 1, "name": "Master Modeling"},
                    {"id": 2, "name": "Master Animation"},
                ])
            )

            asset = {"id": "asset-01"}
            tasks = gazu.task.all_for_asset(asset)
            task = tasks[0]
            self.assertEquals(task["name"], "Master Animation")



    def test_all_for_asset(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url('data/assets/asset-01/tasks'),
                text=json.dumps([
                    {"id": 1, "name": "Master Modeling"},
                    {"id": 2, "name": "Master Animation"},
                ])
            )

            asset = {"id": "asset-01"}
            tasks = gazu.task.all_for_asset(asset)
            task = tasks[0]
            self.assertEquals(task["name"], "Master Animation")

    def test_all_task_types_for_shot(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url('data/shots/shot-1/task_types'),
                text='[{"id": 1, "name": "Modeling"}]'
            )

            shot = {"id": "shot-1"}
            task_types = gazu.task.all_task_types_for_shot(shot)
            task_type = task_types[0]
            self.assertEquals(task_type["name"], "Modeling")

    def test_get_task_by_task_type(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url(
                    'data/tasks?task_type_id=type-1&entity_id=entity-1'
                ),
                text=json.dumps(
                    [{"name": "Task 01", "project_id": "project-1"}]
                )
            )
            test_task = gazu.task.get_task_by_task_type(
                {"id": "type-1"}, {"id": "entity-1"}
            )
            self.assertEquals(test_task[0]["name"], "Task 01")

    def test_get_task_by_name(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url(
                    'data/tasks?name=Modeling&entity_id=entity-1'
                ),
                text=json.dumps(
                    [{"name": "Task 01", "project_id": "project-1"}]
                )
            )
            test_task = gazu.task.get_task_by_name(
                "Modeling", {"id": "entity-1"}
            )
            self.assertEquals(test_task["name"], "Task 01")

    def test_get_task_type(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/task_types"),
                text=json.dumps([
                    {"name": "FX", "id": "task-type-fx"},
                    {"name": "Modeling", "id": "task-type-modeling"},
                ])
            )
            task_type = gazu.task.get_task_type("FX")
            self.assertEquals(task_type["name"], "FX")

    def test_get_task_from_path(self):
        with requests_mock.mock() as mock:
            file_path = "/simple/SE01/S01/animation/blocking"
            mock.post(
                gazu.client.get_full_url("project/tasks/from-path"),
                text=json.dumps({"id": "task-id"})
            )
            task = gazu.task.get_task_from_path(
                {"id": "project-id"},
                file_path,
                "shot"
            )
            request_body_string = mock.request_history[0].body.decode("utf-8")
            request_body = json.loads(request_body_string)
            self.assertEquals(request_body["project_id"], "project-id")
            self.assertEquals(request_body["type"], "shot")
            self.assertEquals(request_body["file_path"], file_path)
            self.assertIsNotNone(task)
            self.assertEquals(task["id"], "task-id")

    def test_get_task_status(self):
        with requests_mock.mock() as mock:
            path = "data/task_status?id=status-01"
            mock.get(
                gazu.client.get_full_url(path),
                text=json.dumps([{"name": "WIP", "id": "status-01"}])
            )
            status = gazu.task.get_task_status({
                "id": "task-01",
                "task_status_id": "status-01"
            })
            self.assertEquals(status["id"], "status-01")

    def test_start_task(self):
        with requests_mock.mock() as mock:
            mock.put(
                gazu.client.get_full_url(
                    'data/tasks/task-1/start'
                ),
                text='{"name": "Task 01", "task_status_id": "wip-1"}'
            )
            test_task = gazu.task.start_task({"id": "task-1"})
            self.assertEquals(test_task["task_status_id"], "wip-1")
