import asyncio
import os
import random
import sys
import re
import string 
import string as rohit
import time
from datetime import datetime, timedelta
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatInviteLink, ChatPrivileges
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant
from bot import Bot
from config import *
from helper_func import *
from database.database import *
from database.db_premium import *

EMOJI_MODE = True
REACTIONS = ["👍", "😍", "🔥", "🎉", "❤️"]
STICKER_ID = "CAACAgUAAxkBAAJFeWd037UWP-vgb_dWo55DCPZS9zJzAAJpEgACqXaJVxBrhzahNnwSHgQ"

BAN_SUPPORT = f"{BAN_SUPPORT}"
TUT_VID = f"{TUT_VID}"

async def short_url(client: Client, message: Message, base64_string):
    try:
        prem_link = f"https://t.me/{client.username}?start=yu3elk{base64_string}"
        short_link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, prem_link)

        buttons = [
            [
                InlineKeyboardButton(text="Download", url=short_link),
                InlineKeyboardButton(text="Tutorial", url=TUT_VID)
            ],
            [
                InlineKeyboardButton(text="Premium", callback_data="premium")
            ]
        ]

        await message.reply_photo(
            photo=SHORTENER_PIC,
            caption=SHORT_MSG.format(),
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    except IndexError:
        pass

@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    id = message.from_user.id
    is_premium = await is_premium_user(id)

    if EMOJI_MODE:
        await message.react(emoji=random.choice(REACTIONS), big=True)

    banned_users = await db.get_ban_users()
    if user_id in banned_users:
        return await message.reply_text(
            "<b>⛔️ You are banned from using this bot.</b>\n\n"
            "<i>Contact support if you think this is a mistake.</i>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Contact Support", url=BAN_SUPPORT)]]
            )
        )

    if not await is_subscribed(client, user_id):
        return await not_joined(client, message)

    FILE_AUTO_DELETE = await db.get_del_timer()

    if not await db.present_user(user_id):
        try:
            await db.add_user(user_id)
        except:
            pass

    text = message.text

    if len(text) > 7:
        try:
            basic = text.split(" ", 1)[1]
            if basic.startswith("yu3elk"):
                base64_string = basic[6:-1]
            else:
                base64_string = basic

            if not is_premium and user_id != OWNER_ID and not basic.startswith("yu3elk"):
                await short_url(client, message, base64_string)
                return

        except Exception as e:
            print(f"Error processing start payload: {e}")

        string = await decode(base64_string)
        argument = string.split("-")

        ids = []
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = range(start, end + 1) if start <= end else list(range(start, end - 1, -1))
            except Exception as e:
                print(f"Error decoding IDs: {e}")
                return

        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except Exception as e:
                print(f"Error decoding ID: {e}")
                return

        temp_msg = await message.reply("<b>Please wait...</b>")
        try:
            messages = await get_messages(client, ids)
        except Exception as e:
            await message.reply_text("Something went wrong!")
            print(f"Error getting messages: {e}")
            return
        finally:
            await temp_msg.delete()

        codeflix_msgs = []
        for msg in messages:
            caption = (CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, 
                                             filename=msg.document.file_name) if bool(CUSTOM_CAPTION) and bool(msg.document)
                       else ("" if not msg.caption else msg.caption.html))

            reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None

            try:
                copied_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, 
                                            reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                codeflix_msgs.append(copied_msg)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                copied_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, 
                                            reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                codeflix_msgs.append(copied_msg)
            except Exception as e:
                print(f"Failed to send message: {e}")
                pass

        if FILE_AUTO_DELETE > 0:
            notification_msg = await message.reply(
                f"<b>⚠️ This file will be deleted in {get_exp_time(FILE_AUTO_DELETE)}. Please save or forward it to your saved messages before it gets deleted.</b>"
            )

            await asyncio.sleep(FILE_AUTO_DELETE)

            for snt_msg in codeflix_msgs:    
                if snt_msg:
                    try:    
                        await snt_msg.delete()  
                    except Exception as e:
                        print(f"Error deleting message {snt_msg.id}: {e}")

            try:
                reload_url = (
                    f"https://t.me/{client.username}?start={message.command[1]}"
                    if message.command and len(message.command) > 1
                    else None
                )
                keyboard = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Get File Again!", url=reload_url)]]
                ) if reload_url else None

                await notification_msg.edit(
                    "<b>Your video/file is successfully deleted!\n\nClick below to get your deleted video/file 👇</b>",
                    reply_markup=keyboard
                )
            except Exception as e:
                print(f"Error updating notification with 'Get File Again' button: {e}")
    else:
        m = await message.reply_text("<i>Welcome to my bot.\nHope you're doing well...</i>")
        await asyncio.sleep(0.4)
        await m.edit_text("⏳")
        await asyncio.sleep(0.5)
        await m.edit_text("👀")
        await asyncio.sleep(0.5)
        await m.edit_text("<b><i>Starting...</i></b>")
        await asyncio.sleep(0.4)
        await m.delete()
        m = await message.reply_sticker(STICKER_ID)
        await asyncio.sleep(1)
        await m.delete()

        start_images = await db.get_images("start")
        photo = random.choice(start_images) if start_images else START_PIC

        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("• More Channels •", url="https://t.me/Nova_Flix/50")],
                [
                    InlineKeyboardButton("• About", callback_data="about"),
                    InlineKeyboardButton('Help •', callback_data="help")
                ]
            ]
        )
        await message.reply_photo(
            photo=photo,
            caption=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            message_effect_id=5104841245755180586
        )
        return

@Bot.on_message(filters.command('help') & filters.private)
async def help_command(client: Client, message: Message):
    help_images = await db.get_images("help")
    photo = random.choice(help_images) if help_images else HELP_PIC  # Assuming HELP_PIC is defined in config.py
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Back to Start", callback_data="start")]
        ]
    )
    await message.reply_photo(
        photo=photo,
        caption="This is the help message. Here you can find information on how to use the bot.",
        reply_markup=reply_markup
    )

@Bot.on_message(filters.command('about') & filters.private)
async def about_command(client: Client, message: Message):
    about_images = await db.get_images("about")
    photo = random.choice(about_images) if about_images else ABOUT_PIC  # Assuming ABOUT_PIC is defined in config.py
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Back to Start", callback_data="start")]
        ]
    )
    await message.reply_photo(
        photo=photo,
        caption="This is the about message. Learn more about the bot and its creator.",
        reply_markup=reply_markup
    )

# Remaining functions (not_joined, myplan, etc.) remain unchanged as they are unrelated to the image issue.
# Include them as they were in your original start.py if needed.
