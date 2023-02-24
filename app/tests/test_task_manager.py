import unittest
from pymongo import MongoClient
from myapp.task_manager import AirflowTaskManager
from myapp.models import TriggerMessage

class AirflowTaskManagerTestCase(unittest.TestCase):
    def setUp(self):
        mongo_uri = "mongodb://localhost:27017"
        db_name = "testdb"
        self.client = MongoClient(mongo_uri)
        self.client.drop_database(db_name)
        self.manager = AirflowTaskManager(mongo_uri, db_name)

    def tearDown(self):
        self.client.drop_database("testdb")

    def test_create_trigger_message(self):
        message = TriggerMessage(
            trigger_id="12345",
            trigger_type="Kafka",
            message="hello, world!"
        )
        self.manager.create_trigger_message(message.dict())
        messages = self.manager.get_trigger_messages()
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["trigger_id"], "12345")

    def test_update_production_task(self):
        task = {
            "kafka_id": "67890",
            "task_name": "test task",
            "status": "pending"
        }
        result = self.manager.create_production_task(task)
        task_id = result.inserted_id
        updated_task = {
            "status": "running"
        }
        self.manager.update_production_task(task_id, updated_task)
        tasks = self.manager.get_production_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["status"], "running")
