from aiohttp import web
from plugins import web_server
import asyncio
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime
#Aɴɪᴍᴇ Lᴏʀᴅ
from config import *

name = """
▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄
 A N I M E _ L O R D  イズ  ヒア
▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀
   ╔╦╗┳ ┳╦ ╦╔═╗╔╗╔╔═╗╦ ╦
    ║ ┃ ┃║ ║╠╣ ║║║║  ╠═╣
    ╩ ┻ ┻╚═╝╚  ╝╚╝╚═╝╩ ╩
 **BY Aɴɪᴍᴇ Lᴏʀᴅ**
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
            self.LOGGER(__name__).warning(f"ᴍᴀᴋᴇ ꜱᴜʀᴇ ʙᴏᴛ ɪꜱ ᴀᴅᴍɪɴ ɪɴ ᴅʙ ᴄʜᴀɴɴᴇʟ, ᴀɴᴅ ᴅᴏᴜʙʟᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ_ɪᴅ ᴠᴀʟᴜᴇ, ᴄᴜʀʀᴇɴᴛ ᴠᴀʟᴜᴇ {CHANNEL_ID}")
            self.LOGGER(__name__).info("\nʙᴏᴛ ꜱᴛᴏᴘᴘᴇᴅ. ᴊᴏɪɴ https://t.me/+3lpawaYvxBU4YTY1 ꜰᴏʀ ꜱᴜᴘᴘᴏʀᴛ")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"ʙᴏᴛ ɪꜱ ᴀʟɪᴠᴇ..!\n\nᴄʀᴇᴀᴛᴇᴅ ʙʏ \n ᴡʜᴏ-ᴀᴍ-ɪ")
        self.LOGGER(__name__).info(f"ʙᴏᴛ ᴅᴇᴘʟᴏʏᴇᴅ ʙʏ @ᴡʜᴏ-ᴀᴍ-ɪ")
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
        self.LOGGER(__name__).info(f"ʙᴏᴛ ɪꜱ ᴀʟɪᴠᴇ..! ᴍᴀᴅᴇ ʙʏ @Aɴɪᴍᴇ Lᴏʀᴅ")   

        # Start Web Server
        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", PORT).start()

        try:
            await self.send_message(OWNER_ID, text=f"<b><blockquote>Bᴏᴛ Rᴇsᴛᴀʀᴛᴇᴅ by @Anime_Lord_Bot\n\n<code>{name}</code></blockquote></b>")
        except Exception as e:
            self.LOGGER(__name__).warning(f"Failed to send startup message to OWNER_ID: {str(e)}")

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("ʙᴏᴛ ꜱᴛᴏᴘᴘᴇᴅ.")

    def run(self):
        """Run the bot."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())
        self.LOGGER(__name__).info(f"ʙᴏᴛ ɪꜱ ɴᴏᴡ ᴀʟɪᴠᴇ. ᴛʜᴀɴᴋꜱ ᴛᴏ @ᴡʜᴏ-ᴀᴍ-ɪ")
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            self.LOGGER(__name__).info("ꜰᴜᴄᴋɪɴ ᴅᴏᴡɴ...")
        finally:
            loop.run_until_complete(self.stop())

#
# Copyright (C) 2025 by Codeflix-Bots@Github, < https://github.com/Codeflix-Bots >.
#
# This file is part of < https://github.com/Codeflix-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/Codeflix-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
