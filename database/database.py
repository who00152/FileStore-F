from motor.motor_asyncio import AsyncIOMotorClient
from config import DB_URI, DB_NAME

class Database:
    def __init__(self, uri, database_name):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.users = self.db.users  # Users collection
        self.ban_users = self.db.ban_users  # Banned users collection
        self.channels = self.db.channels  # Channels collection
        self.images = self.db.images  # Images collection
        self.timer = self.db.timer  # Auto-delete timer collection
        self.join_requests = self.db.join_requests  # Join requests collection

    async def add_user(self, user_id: int):
        """Add a user to the users collection."""
        await self.users.update_one(
            {"_id": user_id},
            {"$set": {"_id": user_id}},
            upsert=True
        )

    async def present_user(self, user_id: int) -> bool:
        """Check if a user exists in the users collection."""
        return bool(await self.users.find_one({"_id": user_id}))

    async def full_userbase(self) -> list:
        """Get all user IDs from the users collection."""
        users = await self.users.find().to_list(None)
        return [user["_id"] for user in users]

    async def del_user(self, user_id: int):
        """Delete a user from the users collection."""
        await self.users.delete_one({"_id": user_id})

    async def add_ban_user(self, user_id: int):
        """Add a user to the ban_users collection."""
        await self.ban_users.update_one(
            {"_id": user_id},
            {"$set": {"_id": user_id}},
            upsert=True
        )

    async def del_ban_user(self, user_id: int):
        """Remove a user from the ban_users collection."""
        await self.ban_users.delete_one({"_id": user_id})

    async def get_ban_users(self) -> list:
        """Get all banned user IDs."""
        banned = await self.ban_users.find().to_list(None)
        return [user["_id"] for user in banned]

    async def add_channel(self, channel_id: int):
        """Add a channel to the channels collection with default mode 'on'."""
        await self.channels.update_one(
            {"_id": channel_id},
            {"$set": {"_id": channel_id, "mode": "on"}},
            upsert=True
        )

    async def rem_channel(self, channel_id: int):
        """Remove a channel from the channels collection."""
        await self.channels.delete_one({"_id": channel_id})

    async def show_channels(self) -> list:
        """Get all channel IDs."""
        channels = await self.channels.find().to_list(None)
        return [channel["_id"] for channel in channels]

    async def set_channel_mode(self, channel_id: int, mode: str):
        """Set the mode (on/off) for a channel."""
        await self.channels.update_one(
            {"_id": channel_id},
            {"$set": {"mode": mode}}
        )

    async def get_channel_mode(self, channel_id: int) -> str:
        """Get the mode of a channel."""
        channel = await self.channels.find_one({"_id": channel_id})
        return channel.get("mode", "on") if channel else "on"

    async def set_del_timer(self, duration: int):
        """Set the auto-delete timer."""
        await self.timer.update_one(
            {"_id": "delete_timer"},
            {"$set": {"duration": duration}},
            upsert=True
        )

    async def get_del_timer(self) -> int:
        """Get the auto-delete timer."""
        timer = await self.timer.find_one({"_id": "delete_timer"})
        return timer.get("duration", 0) if timer else 0

    async def add_admin(self, admin_id: int):
        """Add an admin to the admins collection."""
        await self.db.admins.update_one(
            {"_id": admin_id},
            {"$set": {"_id": admin_id}},
            upsert=True
        )

    async def del_admin(self, admin_id: int):
        """Remove an admin from the admins collection."""
        await self.db.admins.delete_one({"_id": admin_id})

    async def get_all_admins(self) -> list:
        """Get all admin IDs."""
        admins = await self.db.admins.find().to_list(None)
        return [admin["_id"] for admin in admins]

    async def set_temp_state(self, user_id: int, state: str):
        """Set temporary state for a user."""
        await self.db.temp_state.update_one(
            {"_id": user_id},
            {"$set": {"state": state}},
            upsert=True
        )

    async def get_temp_state(self, user_id: int) -> str:
        """Get temporary state for a user."""
        state = await self.db.temp_state.find_one({"_id": user_id})
        return state.get("state", "") if state else ""

    async def clear_temp_state(self, user_id: int):
        """Clear temporary state for a user."""
        await self.db.temp_state.delete_one({"_id": user_id})

    async def add_image(self, image_type: str, file_id: str):
        """Add an image file ID to the specified image type collection."""
        await self.images.update_one(
            {"type": image_type},
            {"$push": {"file_ids": file_id}},
            upsert=True
        )

    async def get_images(self, image_type: str):
        """Get all image file IDs for the specified image type."""
        doc = await self.images.find_one({"type": image_type})
        return doc["file_ids"] if doc and "file_ids" in doc else []

    async def remove_image(self, image_type: str, index: int):
        """Remove an image file ID at the specified index for the image type."""
        images = await self.get_images(image_type)
        if index < len(images):
            images.pop(index)
            await self.images.update_one(
                {"type": image_type},
                {"$set": {"file_ids": images}}
            )

    async def clear_images(self, image_type: str):
        """Clear all image file IDs for the specified image type."""
        await self.images.delete_one({"type": image_type})

    async def reqChannel_exist(self, channel_id: int) -> bool:
        """Check if a channel exists in the channels collection."""
        return bool(await self.channels.find_one({"_id": channel_id}))

    async def req_user(self, channel_id: int, user_id: int):
        """Add a user to the channel's join request list."""
        await self.join_requests.update_one(
            {"_id": f"{channel_id}_{user_id}"},
            {"$set": {"channel_id": channel_id, "user_id": user_id}},
            upsert=True
        )

    async def req_user_exist(self, channel_id: int, user_id: int) -> bool:
        """Check if a user exists in the channel's join request list."""
        return bool(await self.join_requests.find_one({"_id": f"{channel_id}_{user_id}"}))

    async def del_req_user(self, channel_id: int, user_id: int):
        """Remove a user from the channel's join request list."""
        await self.join_requests.delete_one({"_id": f"{channel_id}_{user_id}"})

# Initialize the database
db = Database(DB_URI, DB_NAME)
