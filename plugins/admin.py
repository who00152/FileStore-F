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

@Bot.on_message(filters.command('add_admin') & filters.private & filters.user(OWNER_ID))
async def add_admins(client: Client, message: Message):
    pro = await message.reply("<b><i>Please wait...</i></b>", quote=True)
    check = 0
    admin_ids = await db.get_all_admins()
    admins = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]])

    if not admins:
        return await pro.edit(
            "<b>You need to provide user ID(s) to add as admin.</b>\n\n"
            "<b>Usage:</b>\n"
            "<code>/add_admin [user_id]</code> — add one or more user IDs\n\n"
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
            admin_list += f"<blockquote><b>ID <code>{id}</code> already exists.</b></blockquote>\n"
            continue

        id = str(id)
        if id.isdigit() and len(id) == 10:
            admin_list += f"<b><blockquote>(ID: <code>{id}</code>) added.</blockquote></b>\n"
            check += 1
        else:
            admin_list += f"<blockquote><b>Invalid ID: <code>{id}</code></b></blockquote>\n"

    if check == len(admins):
        for id in admins:
            await db.add_admin(int(id))
        await pro.edit(f"<b>✅ Admin(s) added successfully:</b>\n\n{admin_list}", reply_markup=reply_markup)
    else:
        await pro.edit(
            f"<b>❌ Some errors occurred while adding admins:</b>\n\n{admin_list.strip()}\n\n"
            "<b><i>Please check and try again.</i></b>",
            reply_markup=reply_markup
        )

@Bot.on_message(filters.command('deladmin') & filters.private & filters.user(OWNER_ID))
async def delete_admins(client: Client, message: Message):
    pro = await message.reply("<b><i>Please wait...</i></b>", quote=True)
    admin_ids = await db.get_all_admins()
    admins = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]])

    if not admins:
        return await pro.edit(
            "<b>Please provide valid admin ID(s) to remove.</b>\n\n"
            "<b>Usage:</b>\n"
            "<code>/deladmin [user_id]</code> — remove specific IDs\n"
            "<code>/deladmin all</code> — remove all admins",
            reply_markup=reply_markup
        )

    if len(admins) == 1 and admins[0].lower() == "all":
        if admin_ids:
            for id in admin_ids:
                await db.del_admin(id)
            ids = "\n".join(f"<blockquote><code>{admin}</code> ✅</blockquote>" for admin in admin_ids)
            return await pro.edit(f"<b>⛔️ All admin IDs have been removed:</b>\n{ids}", reply_markup=reply_markup)
        else:
            return await pro.edit("<b><blockquote>No admin IDs to remove.</blockquote></b>", reply_markup=reply_markup)

    if admin_ids:
        passed = ''
        for admin_id in admins:
            try:
                id = int(admin_id)
            except:
                passed += f"<blockquote><b>Invalid ID: <code>{admin_id}</code></b></blockquote>\n"
                continue

            if id in admin_ids:
                await db.del_admin(id)
                passed += f"<blockquote><code>{id}</code> ✅ removed</blockquote>\n"
            else:
                passed += f"<blockquote><b>ID <code>{id}</code> not found in admin list.</b></blockquote>\n"

        await pro.edit(f"<b>⛔️ Admin removal result:</b>\n\n{passed}", reply_markup=reply_markup)
    else:
        await pro.edit("<b><blockquote>No admin IDs available to delete.</blockquote></b>", reply_markup=reply_markup)

@Bot.on_message(filters.command('admins') & filters.private & admin)
async def get_admins(client: Client, message: Message):
    pro = await message.reply("<b><i>Please wait...</i></b>", quote=True)
    admin_ids = await db.get_all_admins()

    if not admin_ids:
        admin_list = "<b><blockquote>❌ No admins found.</blockquote></b>"
    else:
        admin_list = "\n".join(f"<b><blockquote>ID: <code>{id}</code></blockquote></b>" for id in admin_ids)

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]])
    await pro.edit(f"<b>⚡ Current admin list:</b>\n\n{admin_list}", reply_markup=reply_markup)

@Bot.on_message(filters.command("pic") & filters.private & admin)
async def pic_command(client: Client, message: Message):
    await message.reply_text(
        "Use the following commands to manage images for start, help, or about messages:\n\n"
        "/set_pic - Set new images\n"
        "/rev_pic - Remove existing images",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]])
    )

@Bot.on_message(filters.command("set_pic") & filters.private & admin)
async def set_pic(client: Client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Set Start Image", callback_data="set_start")],
            [InlineKeyboardButton("Set Help Image", callback_data="set_help")],
            [InlineKeyboardButton("Set About Image", callback_data="set_about")],
        ]
    )
    await message.reply_text("Select an option to set an image:", reply_markup=keyboard)

@Bot.on_message(filters.command("rev_pic") & filters.private & admin)
async def rev_pic(client: Client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Remove Start Image", callback_data="remove_start")],
            [InlineKeyboardButton("Remove Help Image", callback_data="remove_help")],
            [InlineKeyboardButton("Remove About Image", callback_data="remove_about")],
        ]
    )
    await message.reply_text("Select an option to remove images:", reply_markup=keyboard)

@Bot.on_message(filters.command("rev_start") & filters.private & admin)
async def rev_start(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /rev_start <image_number>")
        return
    try:
        index = int(message.command[1]) - 1
        await db.remove_image("start", index)
        await message.reply_text(f"Start image removed! Total start images: {len(await db.get_images('start'))}")
    except ValueError:
        await message.reply_text("Please provide a valid number.")
    except IndexError:
        await message.reply_text("Image number out of range.")

@Bot.on_message(filters.command("rev_all_start") & filters.private & admin)
async def rev_all_start(client: Client, message: Message):
    await db.clear_images("start")
    await message.reply_text("All start images have been removed.")

@Bot.on_message(filters.command("rev_help") & filters.private & admin)
async def rev_help(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /rev_help <image_number>")
        return
    try:
        index = int(message.command[1]) - 1
        await db.remove_image("help", index)
        await message.reply_text(f"Help image removed! Total help images: {len(await db.get_images('help'))}")
    except ValueError:
        await message.reply_text("Please provide a valid number.")
    except IndexError:
        await message.reply_text("Image number out of range.")

@Bot.on_message(filters.command("rev_all_help") & filters.private & admin)
async def rev_all_help(client: Client, message: Message):
    await db.clear_images("help")
    await message.reply_text("All help images have been removed.")

@Bot.on_message(filters.command("rev_about") & filters.private & admin)
async def rev_about(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /rev_about <image_number>")
        return
    try:
        index = int(message.command[1]) - 1
        await db.remove_image("about", index)
        await message.reply_text(f"About image removed! Total about images: {len(await db.get_images('about'))}")
    except ValueError:
        await message.reply_text("Please provide a valid number.")
    except IndexError:
        await message.reply_text("Image number out of range.")

@Bot.on_message(filters.command("rev_all_about") & filters.private & admin)
async def rev_all_about(client: Client, message: Message):
    await db.clear_images("about")
    await message.reply_text("All about images have been removed.")
