from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId

class AirflowTaskManager:
    def __init__(self, mongo_uri, db_name):
        self.mongo = MongoClient(mongo_uri)[db_name]

    def create_trigger_message(self, message):
        try:
            self.mongo.triggers.insert_one(message)
        except PyMongoError as e:
            raise Exception("Failed to create trigger message: " + str(e))

    def create_production_task(self, task):
        try:
            self.mongo.production.insert_one(task)
        except PyMongoError as e:
            raise Exception("Failed to create production task: " + str(e))

    def create_result(self, result):
        try:
            self.mongo.results.insert_one(result)
        except PyMongoError as e:
            raise Exception("Failed to create result: " + str(e))

    def get_trigger_messages(self):
        return list(self.mongo.triggers.find())

    def get_trigger_message_by_id(self, message_id):
        return self.mongo.triggers.find_one({"_id": ObjectId(message_id)})

    def get_production_tasks(self):
        return list(self.mongo.production.find())

    def get_production_task_by_id(self, task_id):
        return self.mongo.production.find_one({"_id": ObjectId(task_id)})

    def get_results(self):
        return list(self.mongo.results.find())

    def get_result_by_id(self, result_id):
        return self.mongo.results.find_one({"_id": ObjectId(result_id)})

    def update_production_task(self, task_id, task):
        try:
            self.mongo.production.update_one({"_id": ObjectId(task_id)}, {"$set": task})
        except PyMongoError as e:
            raise Exception("Failed to update production task: " + str(e))

    def update_result(self, result_id, result):
        try:
            self.mongo.results.update_one({"_id": ObjectId(result_id)}, {"$set": result})
        except PyMongoError as e:
            raise Exception("Failed to update result: " + str(e))

    def delete_trigger_message(self, message_id):
        try:
            self.mongo.triggers.delete_one({"_id": ObjectId(message_id)})
        except PyMongoError as e:
            raise Exception("Failed to delete trigger message: " + str(e))
