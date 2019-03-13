from pymongo import MongoClient

def init_mongodb(db_name, db_port):
    client = MongoClient('localhost', db_port)
    db = client[db_name]
    return client, db

