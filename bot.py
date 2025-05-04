import os
import sys
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from config import API_HASH, APP_ID, LOGGER, OWNER_ID, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, CHANNEL_ID, PORT, DB_URI, DB_NAME, COLLECTION_NAME
from aiohttp import web
from plugins import web_server
from database.database import Database

db = Database(DB_URI, DB_NAME, COLLECTION_NAME)

__version__ = "1.0.0"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pyrogram.client").setLevel(logging.WARNING)
logging.getLogger("pyrogram.session.auth").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram.session.session").setLevel(logging.CRITICAL)

class Bot(Client):
    def __init__(self):
        super().__init__(
            "Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            bot_token=TG_BOT_TOKEN,
            workers=TG_BOT_WORKERS,
            plugins={"root": "plugins"},
        )
        self.LOGGER = LOGGER
        self.uptime = None

    async def start(self):
        await super().start()
        self.uptime = asyncio.get_event_loop().time()
        await self.LOGGER(__name__).info("ʙᴏᴛ ɪꜱ ᴀʟɪᴠᴇ..!")
        await self.LOGGER(__name__).info(f"ʙᴏᴛ ᴅᴇᴘʟᴏʏᴇᴅ ʙʏ @ᴡʜᴏ-ᴀᴍ-ɪ")
        await self.LOGGER(__name__).info(f"ʙᴏᴛ ɪꜱ ᴀʟɪᴠᴇ..! ᴍᴀᴅᴇ ʙʏ @Aɴɪᴍᴇ Lᴏʀᴅ")
        await self.LOGGER(__name__).info(f"ʙᴏᴛ ɪꜱ ɴᴏᴡ ᴀʟɪᴠᴇ. ᴛʜᴀɴᴋꜱ ᴛᴏ @ᴡʜᴏ-ᴀᴍ-ɪ")

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")

async def check_admin(client, message):
    user_id = message.from_user.id
    if user_id == OWNER_ID:
        return True
    return await db.admin_exist(user_id)

admin = filters.create(check_admin)

app = Bot()

async def main():
    await app.start()
    port = int(os.environ.get("PORT", PORT))
    try:
        server = web.AppRunner(await web_server())
        await server.setup()
        await web.TCPSite(server, "0.0.0.0", port).start()
        await asyncio.Event().wait()
    finally:
        await app.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        LOGGER(__name__).info("Bot stopped!")
