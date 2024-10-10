from pymongo import MongoClient
import os,csv

with MongoClient("mongodb://localhost:27017/") as client:
    db = client["accounting"]
    collection = db["data"]
    result = collection.delete_many({})