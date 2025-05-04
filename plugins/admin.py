# admin.py

import asyncio
import os
import random
import sys
import time
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction, ChatMemberStatus, ChatType
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatMemberUpdated, ChatPermissions
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, InviteHashEmpty, ChatAdminRequired, PeerIdInvalid, UserIsBlocked, InputUserDeactivated
from bot import Bot
from config import *
from helper_func import *
from database.database import *

# Commands for adding admins by owner
@Bot.on_message(filters.command('add_admin') & filters.private & filters.user(OWNER_ID))
async def add_admins(client: Client, message: Message):
    pro = await message.reply("<b><i>ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ..</i></b>", quote=True)
    check = 0
    admin_ids = await db.get_all_admins()
    admins = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])

    if not admins:
        return await pro.edit(
            "<b>ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴘʀᴏᴠɪᴅᴇ ᴜꜱᴇʀ ɪᴅ(ꜱ) ᴛᴏ ᴀᴅᴅ ᴀꜱ ᴀᴅᴍɪɴ.</b>\n\n"
            "<b>ᴜꜱᴀɢᴇ:</b>\n"
            "<code>/add_admin [user_id]</code> — ᴀᴅᴅ ᴏɴᴇ ᴏʀ ᴍᴏʀᴇ ᴜꜱᴇʀ ɪᴅꜱ\n\n"
            "<b>Example:</b>\n"
            "<code>/add_admin 1234567890 9876543210</code>",
            reply_markup=reply_markup
        )

    admin_list = ""
    for id in admins:
        try:
            id = int(id)
        except:
            admin_list += f"<blockquote><b>Invalid ID: <code>{id}</code></b></blockquote>\n"
            continue

        if id in admin_ids:
            admin_list += f"<blockquote><b>ID <code>{id}</code> ᴀʟʀᴇᴀᴅʏ ᴇxɪꜱᴛꜱ.</b></blockquote>\n"
            continue

        id = str(id)
        if id.isdigit() and len(id) == 10:
            admin_list += f"<b><blockquote>(ID: <code>{id}</code>) ᴀᴅᴅᴇᴅ.</blockquote></b>\n"
            check += 1
        else:
            admin_list += f"<blockquote><b>ɪɴᴠᴀʟɪᴅ ɪᴅ: <code>{id}</code></b></blockquote>\n"

    if check == len(admins):
        for id in admins:
            await db.add_admin(int(id))
        await pro.edit(f"<b>✅ ᴀᴅᴍɪɴ(ꜱ) ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ:</b>\n\n{admin_list}", reply_markup=reply_markup)
    else:
        await pro.edit(
            f"<b>❌ ꜱᴏᴍᴇ ᴇʀʀᴏʀꜱ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴀᴅᴅɪɴɢ ᴀᴅᴍɪɴꜱ:</b>\n\n{admin_list.strip()}\n\n"
            "<b><i>ᴘʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.</i></b>",
            reply_markup=reply_markup
        )

@Bot.on_message(filters.command('deladmin') & filters.private & filters.user(OWNER_ID))
async def delete_admins(client: Client, message: Message):
    pro = await message.reply("<b><i>ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ..</i></b>", quote=True)
    admin_ids = await db.get_all_admins()
    admins = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])

    if not admins:
        return await pro.edit(
            "<b>ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴠᴀʟɪᴅ ᴀᴅᴍɪɴ ɪᴅ(ꜱ) ᴛᴏ ʀᴇᴍᴏᴠᴇ.</b>\n\n"
            "<b>ᴜꜱᴀɢᴇ:</b>\n"
            "<code>/deladmin [user_id]</code> — ʀᴇᴍᴏᴠᴇ ꜱᴘᴇᴄɪꜰɪᴄ ɪᴅꜱ\n"
            "<code>/deladmin all</code> — ʀᴇᴍᴏᴠᴇ ᴀʟʟ ᴀᴅᴍɪɴꜱ",
            reply_markup=reply_markup
        )

    if len(admins) == 1 and admins[0].lower() == "all":
        if admin_ids:
            for id in admin_ids:
                await db.del_admin(id)
            ids = "\n".join(f"<blockquote><code>{admin}</code> ✅</blockquote>" for admin in admin_ids)
            return await pro.edit(f"<b>⛔️ ᴀʟʟ ᴀᴅᴍɪɴ ɪᴅꜱ ʜᴀᴠᴇ ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ:</b>\n{ids}", reply_markup=reply_markup)
        else:
            return await pro.edit("<b><blockquote>ɴᴏ ᴀᴅᴍɪɴ ɪᴅꜱ ᴛᴏ ʀᴇᴍᴏᴠᴇ.</blockquote></b>", reply_markup=reply_markup)

    if admin_ids:
        passed = ''
        for admin_id in admins:
            try:
                id = int(admin_id)
            except:
                passed += f"<blockquote><b>ɪɴᴠᴀʟɪᴅ ɪᴅ: <code>{admin_id}</code></b></blockquote>\n"
                continue

            if id in admin_ids:
                await db.del_admin(id)
                passed += f"<blockquote><code>{id}</code> ✅ ʀᴇᴍᴏᴠᴇᴅ</blockquote>\n"
            else:
                passed += f"<blockquote><b>ID <code>{id}</code> ɴᴏᴛ ꜰᴏᴜɴᴅ ɪɴ ᴀᴅᴍɪɴ ʟɪꜱᴛ.</b></blockquote>\n"

        await pro.edit(f"<b>⛔️ ᴀᴅᴍɪɴ ʀᴇᴍᴏᴠᴀʟ ʀᴇꜱᴜʟᴛ:</b>\n\n{passed}", reply_markup=reply_markup)
    else:
        await pro.edit("<b><blockquote>ɴᴏ ᴀᴅᴍɪɴ ɪᴅꜱ ᴀᴠᴀɪʟᴀʙʟᴇ ᴛᴏ ᴅᴇʟᴇᴛᴇ.</blockquote></b>", reply_markup=reply_markup)

@Bot.on_message(filters.command('admins') & filters.private & admin)
async def get_admins(client: Client, message: Message):
    pro = await message.reply("<b><i>ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ..</i></b>", quote=True)
    admin_ids = await db.get_all_admins()

    if not admin_ids:
        admin_list = "<b><blockquote>❌ ɴᴏ ᴀᴅᴍɪɴꜱ ꜰᴏᴜɴᴅ.</blockquote></b>"
    else:
        admin_list = "\n".join(f"<b><blockquote>ID: <code>{id}</code></blockquote></b>" for id in admin_ids)

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])
    await pro.edit(f"<b>⚡ ᴄᴜʀʀᴇɴᴛ ᴀᴅᴍɪɴ ʟɪꜱᴛ:</b>\n\n{admin_list}", reply_markup=reply_markup)

# New command for managing images
@Bot.on_message(filters.command("pic") & filters.private & admin)
async def pic_command(client: Client, message: Message):
    await message.reply_text(
        "If you want to set/remove any images for start, help, or about messages, reply with:\n\n"
        "/set_pic - to set images\n"
        "/rev_pic - to remove images",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])
    )

@Bot.on_message(filters.command("set_pic") & filters.private & admin)
async def set_pic(client: Client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Set Start Img", callback_data="set_start")],
            [InlineKeyboardButton("Set Help Img", callback_data="set_help")],
            [InlineKeyboardButton("Set About Img", callback_data="set_about")],
        ]
    )
    await message.reply_text("Please select which image to set:", reply_markup=keyboard)

@Bot.on_message(filters.command("rev_pic") & filters.private & admin)
async def rev_pic(client: Client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Remove Start Img", callback_data="remove_start")],
            [InlineKeyboardButton("Remove Help Img", callback_data="remove_help")],
            [InlineKeyboardButton("Remove About Img", callback_data="remove_about")],
        ]
    )
    await message.reply_text("Please select which images to remove from:", reply_markup=keyboard)

@Bot.on_message(filters.command("rev_start") & filters.private & admin)
async def rev_start(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Please provide the image number to remove.")
        return
    try:
        index = int(message.command[1]) - 1
        await db.remove_image("start", index)
        await message.reply_text(f"Image removed! Now current number of start images: {len(await db.get_images('start'))}")
    except ValueError:
        await message.reply_text("Invalid number.")
    except IndexError:
        await message.reply_text("Image number out of range.")

@Bot.on_message(filters.command("rev_all_start") & filters.private & admin)
async def rev_all_start(client: Client, message: Message):
    await db.clear_images("start")
    await message.reply_text("All start images removed.")

@Bot.on_message(filters.command("rev_help") & filters.private & admin)
async def rev_help(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Please provide the image number to remove.")
        return
    try:
        index = int(message.command[1]) - 1
        await db.remove_image("help", index)
        await message.reply_text(f"Image removed! Now current number of help images: {len(await db.get_images('help'))}")
    except ValueError:
        await message.reply_text("Invalid number.")
    except IndexError:
        await message.reply_text("Image number out of range.")

@Bot.on_message(filters.command("rev_all_help") & filters.private & admin)
async def rev_all_help(client: Client, message: Message):
    await db.clear_images("help")
    await message.reply_text("All help images removed.")

@Bot.on_message(filters.command("rev_about") & filters.private & admin)
async def rev_about(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Please provide the image number to remove.")
        return
    try:
        index = int(message.command[1]) - 1
        await db.remove_image("about", index)
        await message.reply_text(f"Image removed! Now current number of about images: {len(await db.get_images('about'))}")
    except ValueError:
        await message.reply_text("Invalid number.")
    except IndexError:
        await message.reply_text("Image number out of range.")

@Bot.on_message(filters.command("rev_all_about") & filters.private & admin)
async def rev_all_about(client: Client, message: Message):
    await db.clear_images("about")
    await message.reply_text("All about images removed.")
