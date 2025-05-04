import os
import sys
import asyncio
import logging
import signal
from pyrogram import Client
from aiohttp import web
from config import (
    API_HASH,
    APP_ID,
    LOGGER,
    OWNER_ID,
    TG_BOT_TOKEN,
    TG_BOT_WORKERS,
    CHANNEL_ID,
    PORT,
    DB_URI,
    DB_NAME
)
from database.database import Database

# Initialize database
db = Database(DB_URI, DB_NAME, "users")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            bot_token=TG_BOT_TOKEN,
            workers=TG_BOT_WORKERS,
            plugins={"root": "plugins"},
        )
        self.uptime = None

    async def start(self):
        await super().start()
        self.uptime = asyncio.get_event_loop().time()
        logger.info("Bot is starting...")
        logger.info(f"Bot deployed by @who-am-i")
        logger.info(f"Bot made by @AnimeLord")
        logger.info("✅ Bot is now alive and running!")

    async def stop(self, *args):
        logger.info("🛑 Bot is stopping...")
        await super().stop()
        logger.info("🌀 Bot stopped successfully")

async def health_check(request):
    """Essential health check endpoint"""
    return web.Response(text="OK", status=200)

async def web_server():
    """Create web application with routes"""
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)
    # Add your other routes here
    return app

async def main():
    # Initialize bot
    bot = Bot()
    await bot.start()
    
    # Setup web server
    port = int(os.environ.get("PORT", PORT))
    app = await web_server()
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"🌐 Web server started on port {port}")
    
    # Signal handling for graceful shutdown
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()
    
    def signal_handler(sig):
        logger.info(f"Received signal {sig.name}, shutting down...")
        loop.call_soon_threadsafe(stop_event.set)
    
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, signal_handler, sig)
    
    # Keep the application running
    try:
        await stop_event.wait()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        logger.info("Starting cleanup process...")
        await site.stop()
        await runner.cleanup()
        await bot.stop()
        logger.info("✅ Cleanup completed")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        logger.info("Application terminated")
