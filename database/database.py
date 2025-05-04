from motor.motor_asyncio import AsyncIOMotorClient
import os
from os import environ

# Database configuration
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://animelord:animelord@animelord.1g3ujsr.mongodb.net/?retryWrites=true&w=majority&appName=animelord")
DB_NAME = os.environ.get("DATABASE_NAME", "animelord")

# Initialize MongoDB client
client = AsyncIOMotorClient(DB_URI)
db = client[DB_NAME]

# Collections
admins_collection = db["admins"]
images_collection = db["images"]
temp_state_collection = db["temp_state"]

async def add_admin(user_id: int):
    """Add a user ID to the admins collection."""
    await admins_collection.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id}},
        upsert=True
    )

async def del_admin(user_id: int):
    """Remove a user ID from the admins collection."""
    await admins_collection.delete_one({"user_id": user_id})

async def get_all_admins():
    """Get a list of all admin user IDs."""
    admins = await admins_collection.find().to_list(None)
    return [admin["user_id"] for admin in admins]

async def add_image(image_type: str, file_id: str):
    """Add an image file ID to the specified image type collection."""
    await images_collection.update_one(
        {"type": image_type},
        {"$push": {"file_ids": file_id}},
        upsert=True
    )

async def get_images(image_type: str):
    """Get all image file IDs for the specified image type."""
    doc = await images_collection.find_one({"type": image_type})
    return doc["file_ids"] if doc and "file_ids" in doc else []

async def remove_image(image_type: str, index: int):
    """Remove an image file ID at the specified index for the image type."""
    await images_collection.update_one(
        {"type": image_type},
        {"$unset": {f"file_ids.{index}": ""}}
    )
    await images_collection.update_one(
        {"type": image_type},
        {"$pull": {"file_ids": None}}
    )

async def clear_images(image_type: str):
    """Clear all image file IDs for the specified image type."""
    await images_collection.delete_one({"type": image_type})

async def get_temp_state(chat_id: int):
    """Get the temporary state for a chat ID."""
    doc = await temp_state_collection.find_one({"chat_id": chat_id})
    return doc["state"] if doc and "state" in doc else None

async def set_temp_state(chat_id: int, state: str):
    """Set the temporary state for a chat ID."""
    await temp_state_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"chat_id": chat_id, "state": state}},
        upsert=True
    )

async def clear_temp_state(chat_id: int):
    """Clear the temporary state for a chat ID."""
    await temp_state_collection.delete_one({"chat_id": chat_id})
