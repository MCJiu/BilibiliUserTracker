#--用于与MongoDB交互--
import pymongo

DB_PORT = 'MONGODB_PORT'


class MongoDB:

    def __init__(self, collection, database='bilibili'):
        self.client = pymongo.MongoClient(host='localhost', port=DB_PORT)
        self.database = self.client[database]
        self.col = self.database[collection]

    def insert_one_info(self, info: dict):
        res = self.col.insert_one(info)
        return res.acknowledged