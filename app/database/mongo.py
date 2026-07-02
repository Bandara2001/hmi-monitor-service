from pymongo import MongoClient
from app.config.settings import MONGO_URI, MONGO_DB

class MongoDB:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB]

    def get_device_collection(self):
        return self.db["Device"]
    
    def get_machine_collection(self):
        return self.db["Machine"]


mongo_db = MongoDB()
device_collection = mongo_db.get_device_collection()
machine_collection = mongo_db.get_machine_collection()