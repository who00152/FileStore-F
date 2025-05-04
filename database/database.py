from motor.motor_asyncio import AsyncIOMotorClient
from config import DB_URI, DB_NAME

class Database:
    def __init__(self, uri, database_name, collection_name):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[database_name][collection_name]
        self.ban_collection = self.client[database_name]["banned_users"]
        self.admin_collection = self.client[database_name]["admins"]
        self.user_collection = self.client[database_name]["users"]
        self.channel_collection = self.client[database_name]["channels"]
        self.image_collection = self.client[database_name]["images"]
        self.temp_collection = self.client[database_name]["temp"]
        self.verify_collection = self.client[database_name]["verify"]
        self.request_collection = self.client[database_name]["requests"]

    async def add_ban_user(self, user_id):
        await self.ban_collection.update_one(
            {"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True
        )

    async def del_ban_user(self, user_id):
        await self.ban_collection.delete_one({"user_id": user_id})

    async def get_ban_users(self):
        cursor = self.ban_collection.find({})
        return [doc["user_id"] async for doc in cursor]

    async def add_admin(self, admin_id):
        await self.admin_collection.update_one(
            {"admin_id": admin_id}, {"$set": {"admin_id": admin_id}}, upsert=True
        )

    async def del_admin(self, admin_id):
        await self.admin_collection.delete_one({"admin_id": admin_id})

    async def get_all_admins(self):
        cursor = self.admin_collection.find({})
        return [doc["admin_id"] async for doc in cursor]

    async def admin_exist(self, admin_id):
        return await self.admin_collection.find_one({"admin_id": admin_id}) is not None

    async def add_user(self, user_id):
        await self.user_collection.update_one(
            {"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True
        )

    async def del_user(self, user_id):
        await self.user_collection.delete_one({"user_id": user_id})

    async def present_user(self, user_id):
        return await self.user_collection.find_one({"user_id": user_id}) is not None

    async def full_userbase(self):
        cursor = self.user_collection.find({})
        return [doc["user_id"] async for doc in cursor]

    async def add_channel(self, channel_id):
        await self.channel_collection.update_one(
            {"channel_id": channel_id}, {"$set": {"channel_id": channel_id, "mode": "on"}}, upsert=True
        )

    async def rem_channel(self, channel_id):
        await self.channel_collection.delete_one({"channel_id": channel_id})

    async def show_channels(self):
        cursor = self.channel_collection.find({})
        return [doc["channel_id"] async for doc in cursor]

    async def get_channel_mode(self, channel_id):
        doc = await self.channel_collection.find_one({"channel_id": channel_id})
        return doc.get("mode", "on") if doc else "on"

    async def set_channel_mode(self, channel_id, mode):
        await self.channel_collection.update_one(
            {"channel_id": channel_id}, {"$set": {"mode": mode}}, upsert=True
        )

    async def add_image(self, type, image_id):
        await self.image_collection.update_one(
            {"type": type}, {"$push": {"images": image_id}}, upsert=True
        )

    async def get_images(self, type):
        doc = await self.image_collection.find_one({"type": type})
        return doc.get("images", []) if doc else []

    async def remove_image(self, type, index):
        await self.image_collection.update_one(
            {"type": type}, {"$pull": {"images": {"$position": index}}}
        )

    async def clear_images(self, type):
        await self.image_collection.delete_one({"type": type})

    async def set_temp_state(self, chat_id, state):
        await self.temp_collection.update_one(
            {"chat_id": chat_id}, {"$set": {"state": state}}, upsert=True
        )

    async def get_temp_state(self, chat_id):
        doc = await self.temp_collection.find_one({"chat_id": chat_id})
        return doc.get("state") if doc else None

    async def set_del_timer(self, duration):
        await self.temp_collection.update_one(
            {"key": "delete_timer"}, {"$set": {"duration": duration}}, upsert=True
        )

    async def get_del_timer(self):
        doc = await self.temp_collection.find_one({"key": "delete_timer"})
        return doc.get("duration", 0) if doc else 0

    async def get_total_verify_count(self):
        doc = await self.verify_collection.find_one({"key": "total_verify"})
        return doc.get("count", 0) if doc else 0

    async def reqChannel_exist(self, channel_id):
        return await self.request_collection.find_one({"channel_id": channel_id}) is not None

    async def req_user(self, channel_id, user_id):
        await self.request_collection.update_one(
            {"channel_id": channel_id, "user_id": user_id},
            {"$set": {"channel_id": channel_id, "user_id": user_id}},
            upsert=True
        )

    async def req_user_exist(self, channel_id, user_id):
        return await self.request_collection.find_one({"channel_id": channel_id, "user_id": user_id}) is not None

    async def del_req_user(self, channel_id, user_id):
        await self.request_collection.delete_one({"channel_id": channel_id, "user_id": user_id})
