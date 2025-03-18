from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

client = AsyncIOMotorClient(MONGO_URI)
db = client["sentiment_analysis_db"]
products_collection = db["products"]
reviews_collection = db["reviews"]
markets_collection = db["markets"]
