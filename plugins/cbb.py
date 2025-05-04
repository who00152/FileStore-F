# cbb.py

from pyrogram import Client
from bot import Bot
from config import *
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from database.database import *
import random

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data

    if data == "help":
        help_images = await db.get_images("help")
        if help_images:
            photo = random.choice(help_images)
            await query.message.edit_media(
                media=InputMediaPhoto(media=photo, caption=HELP_TXT.format(first=query.from_user.first_name)),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
                     InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data='close')]
                ])
            )
        else:
            await query.message.edit_text(
                text=HELP_TXT.format(first=query.from_user.first_name),
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
                     InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data='close')]
                ])
            )

    elif data == "about":
        about_images = await db.get_images("about")
        if about_images:
            photo = random.choice(about_images)
            await query.message.edit_media(
                media=InputMediaPhoto(media=photo, caption=ABOUT_TXT.format(first=query.from_user.first_name)),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
                     InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data='close')]
                ])
            )
        else:
            await query.message.edit_text(
                text=ABOUT_TXT.format(first=query.from_user.first_name),
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
                     InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data='close')]
                ])
            )

    elif data == "start":
        start_images = await db.get_images("start")
        if start_images:
            photo = random.choice(start_images)
            await query.message.edit_media(
                media=InputMediaPhoto(media=photo, caption=START_MSG.format(first=query.from_user.first_name)),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("ʜᴇʟᴘ", callback_data='help'),
                     InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data='about')]
                ])
            )
        else:
            await query.message.edit_text(
                text=START_MSG.format(first=query.from_user.first_name),
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("ʜᴇʟᴘ", callback_data='help'),
                     InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data='about')]
                ])
            )

    elif data == "premium":
        await query.message.delete()
        await client.send_photo(
            chat_id=query.message.chat.id,
            photo=QR_PIC,
            caption=(
                f"👋 {query.from_user.username}\n\n"
                f"🎖️ Available Plans :\n\n"
                f"● {PRICE1}  For 0 Days Prime Membership\n\n"
                f"● {PRICE2}  For 1 Month Prime Membership\n\n"
                f"● {PRICE3}  For 3 Months Prime Membership\n\n"
                f"● {PRICE4}  For 6 Months Prime Membership\n\n"
                f"● {PRICE5}  For 1 Year Prime Membership\n\n\n"
                f"💵 ᴀꜱᴋ ᴜᴘɪ ɪᴅ ᴛᴏ ᴀᴅᴍɪɴ ᴀɴᴅ ᴘᴀʏ ᴛʜᴇʀᴇ -  <code>{UPI_ID}</code>\n\n\n"
                f"♻️ ᴘᴀʏᴍᴇɴᴛ ʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ ɪɴꜱᴛᴀɴᴛ ᴍᴇᴍʙᴇʀꜱʜɪᴘ \n\n\n"
                f"‼️ ᴍᴜꜱᴛ ꜱᴇɴᴅ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ ᴀꜰᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ & ɪꜰ ᴀɴʏᴏɴᴇ ᴡᴀɴᴛ ᴄᴜꜱᴛᴏᴍ ᴛɪᴍᴇ ᴍᴇᴍʙʀꜱʜɪᴘ ᴛʜᴇɴ ᴀꜱᴋ ᴀᴅᴍɪɴ"
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "ADMIN 24/7", url=(SCREENSHOT_URL)
                        )
                    ],
                    [InlineKeyboardButton("🔒 Close", callback_data="close")],
                ]
            )
        )

    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

    elif data.startswith("rfs_ch_"):
        cid = int(data.split("_")[2])
        try:
            chat = await client.get_chat(cid)
            mode = await db.get_channel_mode(cid)
            status = "🟢 ᴏɴ" if mode == "on" else "🔴 ᴏғғ"
            new_mode = "ᴏғғ" if mode == "on" else "on"
            buttons = [
                [InlineKeyboardButton(f"ʀᴇǫ ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}", callback_data=f"rfs_toggle_{cid}_{new_mode}")],
                [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back")]
            ]
            await query.message.edit_text(
                f"Channel: {chat.title}\nCurrent Force-Sub Mode: {status}",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except Exception:
            await query.answer("ꜰᴀɪʟᴇᴅ ᴛᴏ ꜰᴇᴛᴄʜ ᴄʜᴀɴɴᴇʟ ɪɴꜰᴏ", show_alert=True)

    elif data.startswith("rfs_toggle_"):
        cid, action = data.split("_")[2:]
        cid = int(cid)
        mode = "on" if action == "on" else "off"

        await db.set_channel_mode(cid, mode)
        await query.answer(f"ꜰᴏʀᴄᴇ-ꜱᴜʙ ꜱᴇᴛ ᴛᴏ {'ON' if mode == 'on' else 'OFF'}")

        chat = await client.get_chat(cid)
        status = "🟢 ON" if mode == "on" else "🔴 OFF"
        new_mode = "off" if mode == "on" else "on"
        buttons = [
            [InlineKeyboardButton(f"ʀᴇǫ ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}", callback_data=f"rfs_toggle_{cid}_{new_mode}")],
            [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back")]
        ]
        await query.message.edit_text(
            f"ᴄʜᴀɴɴᴇʟ: {chat.title}\nᴄᴜʀʀᴇɴᴛ ꜰᴏʀᴄᴇ-ꜱᴜʙ ᴍᴏᴅᴇ: {status}",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data == "fsub_back":
        channels = await db.show_channels()
        buttons = []
        for cid in channels:
            try:
                chat = await client.get_chat(cid)
                mode = await db.get_channel_mode(cid)
                status = "🟢" if mode == "on" else "🔴"
                buttons.append([InlineKeyboardButton(f"{status} {chat.title}", callback_data=f"rfs_ch_{cid}")])
            except:
                continue

        await query.message.edit_text(
            "sᴇʟᴇᴄᴛ ᴀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴛᴏɢɢʟᴇ ɪᴛs ғᴏʀᴄᴇ-sᴜʙ ᴍᴏᴅᴇ:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data.startswith("set_"):
        type = data.split("_")[1]
        await db.set_temp_state(query.message.chat.id, f"set_{type}")
        await query.message.reply_text(f"Please send me the {type} image.")
        await query.answer()

    elif data.startswith("remove_"):
        type = data.split("_")[1]
        images = await db.get_images(type)
        if not images:
            await query.message.reply_text(f"There are no {type} images set.")
        else:
            nums = list(range(1, len(images) + 1))
            text = f"Current {type} images: {', '.join(map(str, nums))}\nTo remove a single image, use /rev_{type} <number>\nTo remove all, use /rev_all_{type}"
            await query.message.reply_text(text)
        await query.answer()
