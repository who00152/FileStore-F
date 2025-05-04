import os
import sys
import asyncio
import logging
import signal
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from config import API_HASH, APP_ID, LOGGER, OWNER_ID, TG_BOT_TOKEN, TG_BOT_WORKERS, CHANNEL_ID, PORT, DB_URI, DB_NAME
from aiohttp import web
from plugins import web_server
from database.database import Database

db = Database(DB_URI, DB_NAME, "users")

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
        self.LOGGER(__name__).info("ʙᴏᴛ ɪꜱ ᴀʟɪᴠᴇ..!")
        self.LOGGER(__name__).info(f"ʙᴏᴛ ᴅᴇᴘʟᴏʏᴇᴅ ʙʏ @ᴡʜᴏ-ᴀᴍ-ɪ")
        self.LOGGER(__name__).info(f"ʙᴏᴛ ɪꜱ ᴀʟɪᴠᴇ..! ᴍᴀᴅᴇ ʙʏ @Aɴɪᴍᴇ Lᴏʀᴅ")
        self.LOGGER(__name__).info(f"ʙᴏᴛ ɪꜱ ɴᴏᴡ ᴀʟɪᴠᴇ. ᴛʜᴀɴᴋꜱ ᴛᴏ @ᴡʜᴏ-ᴀᴍ-ɪ")

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")

app = Bot()

async def main():
    # Initialize bot
    await app.start()
    
    # Setup web server
    port = int(os.environ.get("PORT", PORT))
    runner = web.AppRunner(await web_server())
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    
    # Signal handling for graceful shutdown
    loop = asyncio.get_running_loop()
    shutdown_event = asyncio.Event()
    
    def signal_handler(sig):
        loop.call_soon_threadsafe(shutdown_event.set)
    
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, signal_handler, sig)
    
    # Wait for shutdown signal
    await shutdown_event.wait()
    
    # Cleanup
    await site.stop()
    await runner.cleanup()
    await app.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    finally:
        logging.info("Bot has been gracefully terminated.")
