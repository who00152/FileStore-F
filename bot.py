from aiohttp import web
from plugins import web_server
import asyncio
import pyromod.listen
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import sys
from datetime import datetime
from config import *
from database.database import *

name = """
▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄
 A N I M E _ L O R D  イズ  ヒア
▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀
   ╔╦╗┳ ┳╦ ╦╔═╗╔╗╔╔═╗╦ ╦
    ║ ┃ ┃║ ║╠╣ ║║║║  ╠═╣
    ╩ ┻ ┻╚═╝╚  ╝╚╝╚═╝╩ ╩
 **BY Anime Lord**
"""

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Make sure bot is admin in DB channel, and double check the CHANNEL_ID value, current value {CHANNEL_ID}")
            self.LOGGER(__name__).info("\nBot stopped. Join https://t.me/+3lpawaYvxBU4YTY1 for support")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot is alive..!\n\nCreated by \n Who-Am-I")
        self.LOGGER(__name__).info(f"Bot deployed by @Who-Am-I")
        self.LOGGER(__name__).info(f"""
▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄
 A N I M E _ L O R D  イズ  ヒア
▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀
   ╔╦╗┳ ┳╦ ╦╔═╗╔╗╔╔═╗╦ ╦
    ║ ┃ ┃║ ║╠╣ ║║║║  ╠═╣
    ╩ ┻ ┻╚═╝╚  ╝╚╝╚═╝╩ ╩
""")  # Exact ASCII art as requested

        self.set_parse_mode(ParseMode.HTML)
        self.username = usr_bot_me.username
        self.LOGGER(__name__).info(f"Bot is alive..! Made by @ A N I M E _ L O R D  イズ  ヒア")   

        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", PORT).start()

        try:
            await self.send_message(OWNER_ID, text=f"<b><blockquote>Bot Restarted by @ A N I M E _ L O R D  イズ  ヒア\n\n<code>{name}</code></blockquote></b>")
        except Exception as e:
            self.LOGGER(__name__).warning(f"Failed to send startup message to OWNER_ID: {str(e)}")

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())
        self.LOGGER(__name__).info(f"Bot is now alive. Thanks to @Who-Am-I\n\n{name}")  # ASCII art in run logs
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            self.LOGGER(__name__).info("Shutting down...")
        finally:
            loop.run_until_complete(self.stop())

@Bot.on_message(filters.photo & filters.private & filters.user(admin))
async def handle_admin_photo(client: Client, message: Message):
    chat_id = message.chat.id
    state = await db.get_temp_state(chat_id)
    try:
        if state in ["set_start", "set_help", "set_about"]:
            type_map = {"set_start": "start", "set_help": "help", "set_about": "about"}
            image_type = type_map[state]
            file_id = message.photo.file_id
            await db.add_image(image_type, file_id)
            await message.reply_text(
                f"New {image_type} image has been successfully set! Total {image_type} images: {len(await db.get_images(image_type))}",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]])
            )
            await db.clear_temp_state(chat_id)
        else:
            await message.reply_text("No image setting command is active. Please use /set_pic to start.")
    except Exception as e:
        await message.reply_text(f"Error processing the image: {str(e)}")
