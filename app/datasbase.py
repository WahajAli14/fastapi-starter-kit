import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

load_dotenv()

Mongo_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
Mongo_DB = os.getenv("MONGO_DB", "mydatabase")

client = MongoClient(Mongo_URI)
db = client[Mongo_DB]

async_client = AsyncIOMotorClient(Mongo_URI)
async_db = async_client[Mongo_DB]
