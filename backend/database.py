from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://admin:admin@mongo:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "appointment_manager")
client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]

users_collection = db["users"]
appointments_collection = db["appointments"]
