from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

Mongo_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
Mongo_DB = os.getenv("MONGO_DB", "mydatabase")

client = MongoClient(Mongo_URI)
db = client[Mongo_DB]