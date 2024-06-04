from pymongo import MongoClient
from bson import ObjectId
from app.config import Settings

class MongoDB:
    def __init__(self):
        setting = Settings()
        self.uri = setting.mongodb_url
        self.db_name = setting.mongodb_db_name
        self.collection_name = setting.mongo_collection_name
        self.db = self.connect_to_mongodb(self.uri, self.db_name)
        self.last_star_id = 'LAST_STAR_ID'  # Special ID for the 'last_star' document

    def connect_to_mongodb(self, uri: str, db_name: str):
        client = MongoClient(uri)
        return client[db_name]

    def save(self, document: dict):
        collection = self.db[self.collection_name]

        collection.insert_one(document)

    def load_last_star(self):
        # Load the 'last_star' document
        collection = self.db[self.collection_name]
        doc = collection.find_one({'_id': self.last_star_id})
        return doc['last_star'] if doc is not None else None

    def save_last_star(self, last_star):
        # Save the 'last_star'
        collection = self.db[self.collection_name]
        collection.update_one({'_id': self.last_star_id}, {'$set': {'last_star': last_star}}, upsert=True)

    def find_documents_paginated(self, query=None, page_num=1, page_size=10):
        """ 分页查询符合条件的文档 """
        collection = self.db[self.collection_name]
        if query is None:
            query = {}  


        skips = page_size * (page_num - 1)


        documents = collection.find(query).skip(skips).limit(page_size)
        return list(documents)