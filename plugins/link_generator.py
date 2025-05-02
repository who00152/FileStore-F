from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from helper_func import encode, get_message_id, admin
from asyncio import sleep, CancelledError
import asyncio

# গ্লোবাল ভ্যারিয়েবল
active_commands = {}

async def delete_with_animation(message):
    """ᴅᴇʟᴇᴛᴇ ᴍᴇꜱꜱᴀɢᴇ ᴡɪᴛʜ ʙᴇᴀᴜᴛɪꜰᴜʟ ᴀɴɪᴍᴀᴛɪᴏɴ"""
    try:
        for i in range(5, 0, -1):
            await message.edit(f"🗑️ {'█'*i}{'░'*(5-i)}")
            await sleep(0.15)
        await message.delete()
    except:
        try:
            await message.delete()
        except:
            pass

@Bot.on_callback_query(filters.regex("^close$"))
async def close_button(client, query):
    """ᴄʟᴏꜱᴇ ʙᴜᴛᴛᴏɴ ʜᴀɴᴅʟᴇʀ"""
    user_id = query.from_user.id
    if user_id in active_commands:
        try:
            active_commands[user_id].cancel()
            await query.message.reply("✅ কমান্ড বন্ধ করা হয়েছে।")
        except Exception as e:
            await query.message.reply(f"❌ কমান্ড বন্ধ করতে সমস্যা: {e}")
        finally:
            active_commands.pop(user_id, None)
    await delete_with_animation(query.message)

@Bot.on_callback_query(filters.regex("^stop$"))
async def stop_button(client, query):
    """ꜱᴛᴏᴘ ʙᴜᴛᴛᴏɴ ʜᴀɴᴅʟᴇʀ"""
    user_id = query.from_user.id
    if user_id in active_commands:
        try:
            active_commands[user_id].cancel()
            await query.message.reply("✅ ব্যাচ প্রক্রিয়া বন্ধ করা হয়েছে।")
        except Exception as e:
            await query.message.reply(f"❌ ব্যাচ বন্ধ করতে সমস্যা: {e}")
        finally:
            active_commands.pop(user_id, None)
    await delete_with_animation(query.message)

@Bot.on_message(filters.private & admin & filters.command('batch'))
async def batch(client: Client, message: Message):
    user_id = message.from_user.id
    task = asyncio.current_task()
    active_commands[user_id] = task
    
    try:
        # প্রথম মেসেজ
        while True:
            try:
                first_message = await client.ask(
                    text="ꜰᴏʀᴡᴀʀᴅ ᴛʜᴇ ꜰɪʀꜱᴛ ᴍᴇꜱꜱᴀɢᴇ ꜰʀᴏᴍ 🅳🅱 ᴄʜᴀɴɴᴇʟ (ᴡɪᴛʜ ǫᴜᴏᴛᴇꜱ)..\n\nᴏʀ ꜱᴇɴᴅ ᴛʜᴇ 🅳🅱 ᴄʜᴀɴɴᴇʟ ᴘᴏꜱᴛ ʟɪɴᴋ",
                    chat_id=user_id,
                    filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                    timeout=60,
                    reply_markup=InlineKeyboardMarkup([])  # কোনো বাটন নেই
                )
                f_msg_id = await get_message_id(client, first_message)
                if f_msg_id: break
                await first_message.reply("❌ ᴇʀʀᴏʀ\n\nᴛʜɪꜱ ꜰᴏʀᴡᴀʀᴅᴇᴅ ᴘᴏꜱᴛ ɪꜱ ɴᴏᴛ ꜰʀᴏᴍ ᴍʏ 🅳🅱 ᴄʜᴀɴɴᴇʟ", quote=True)
            except CancelledError:
                return
            except Exception:
                return

        # দ্বিতীয় মেসেজ
        while True:
            try:
                second_message = await client.ask(
                    text="Fᴏʀᴡᴀʀᴅ ᴛʜᴇ ʟᴀꜱᴛ ᴍᴇꜱꜱᴀɢᴇ ꜰʀᴏᴍ 🅳🅱 ᴄʜᴀɴɴᴇʟ (ᴡɪᴛʜ ǫᴜᴏᴛᴇꜱ)..\nᴏʀ ꜱᴇɴᴅ ᴛʜᴇ 🅳🅱 ᴄʜᴀɴɴᴇʟ ᴘᴏꜱᴛ ʟɪɴᴋ",
                    chat_id=user_id,
                    filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                    timeout=60,
                    reply_markup=InlineKeyboardMarkup([])  # কোনো বাটন নেই
                )
                s_msg_id = await get_message_id(client, second_message)
                if s_msg_id: break
                await second_message.reply("❌ ᴇʀʀᴏʀ\n\nᴛʜɪꜱ ꜰᴏʀᴡᴀʀᴅᴇᴅ ᴘᴏꜱᴛ ɪꜱ ɴᴏᴛ ꜰʀᴏᴍ ᴍʏ 🅳🅱 ᴄʜᴀɴɴᴇʟ", quote=True)
            except CancelledError:
                return
            except Exception:
                return

        # লিংক জেনারেট
        string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
        base64_string = await encode(string)
        link = f"https://t.me/{client.username}?start={base64_string}"
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔁 ꜱʜᴀʀᴇ ᴜʀʟ", url=f'https://telegram.me/share/url?url={link}')],
            [InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]
        ])
        await second_message.reply_text(
            f"<b>ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ ʟɪɴᴋ</b>\n\n{link}",
            quote=True,
            reply_markup=reply_markup
        )

    finally:
        active_commands.pop(user_id, None)

@Bot.on_message(filters.private & admin & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    user_id = message.from_user.id
    task = asyncio.current_task()
    active_commands[user_id] = task
    
    try:
        while True:
            try:
                channel_message = await client.ask(
                    text="ꜰᴏʀᴡᴀʀᴅ ᴍᴇꜱꜱᴀɢᴇ ꜰʀᴏᴍ ᴛʜᴇ 🅳🅱 ᴄʜᴀɴɴᴇʟ (ᴡɪᴛʜ ǫᴜᴏᴛᴇꜱ)..\nᴏʀ ꜱᴇɴᴅ ᴛʜᴇ 🅳🅱 ᴄʜᴀɴɴᴇʟ ᴘᴏꜱᴛ ʟɪɴᴋ",
                    chat_id=user_id,
                    filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                    timeout=60,
                    reply_markup=InlineKeyboardMarkup([])  # কোনো বাটন নেই
                )
                msg_id = await get_message_id(client, channel_message)
                if msg_id: break
                await channel_message.reply("❌ ᴇʀʀᴏʀ\n\nᴛʜɪꜱ ꜰᴏʀᴡᴀʀᴅᴇᴅ ᴘᴏꜱᴛ ɪꜱ ɴᴏᴛ ꜰʀᴏᴍ ᴍʏ 🅳🅱 ᴄʜᴀɴɴᴇʟ", quote=True)
            except CancelledError:
                return
            except Exception:
                return

        base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
        link = f"https://t.me/{client.username}?start={base64_string}"
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔁 ꜱʜᴀʀᴇ ᴜʀʟ", url=f'https://telegram.me/share/url?url={link}')],
            [InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]
        ])
        await channel_message.reply_text(
            f"<b>ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ ʟɪɴᴋ</b>\n\n{link}",
            quote=True,
            reply_markup=reply_markup
        )

    finally:
        active_commands.pop(user_id, None)

@Bot.on_message(filters.private & admin & filters.command("custom_batch"))
async def custom_batch(client: Client, message: Message):
    user_id = message.from_user.id
    task = asyncio.current_task()
    active_commands[user_id] = task
    collected = []
    
    try:
        await message.reply(
            "ꜱᴇɴᴅ ᴀʟʟ ᴍᴇꜱꜱᴀɢᴇꜱ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ɪɴᴄʟᴜᴅᴇ ɪɴ ʙᴀᴛᴄʜ.\n\nᴄʟɪᴄᴋ 'STOP' ᴡʜᴇɴ ʏᴏᴜ'ʀᴇ ᴅᴏɴᴇ.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("STOP", callback_data="stop")]
            ])
        )

        while True:
            try:
                user_msg = await client.ask(
                    chat_id=user_id,
                    text="ᴡᴀɪᴛɪɴɢ ꜰᴏʀ ꜰɪʟᴇꜱ/ᴍᴇꜱꜱᴀɢᴇꜱ...\nᴄʟɪᴄᴋ *STOP* ᴛᴏ ꜰɪɴɪꜱʹ.",
                    timeout=60,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("STOP", callback_data="stop")]
                    ])
                )
                
                sent = await user_msg.copy(client.db_channel.id, disable_notification=True)
                collected.append(sent.id)
                
            except CancelledError:
                break
            except Exception as e:
                await message.reply(f"❌ ꜰᴀɪʟᴇᴅ ᴛᴏ ꜱᴛᴏʀᴇ ᴀ ᴍᴇꜱꜱᴀɢᴇ:\n<code>{e}</code>")
                continue

        if not collected:
            await message.reply("❌ ɴᴏ ᴍᴇꜱꜱᴀɢᴇꜱ ᴡᴇʀᴇ ᴀᴅᴅᴇᴅ ᴛᴏ ʙᴀᴛᴄʜ.")
            return

        start_id = collected[0] * abs(client.db_channel.id)
        end_id = collected[-1] * abs(client.db_channel.id)
        string = f"get-{start_id}-{end_id}"
        base64_string = await encode(string)
        link = f"https://t.me/{client.username}?start={base64_string}"

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔁 ꜱʜᴀʀᴇ ᴜʀʟ", url=f'https://telegram.me/share/url?url={link}')],
            [InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]
        ])
        await message.reply(
            f"<b>ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ ʟɪɴᴋ:</b>\n\n{link}",
            reply_markup=reply_markup
        )

    finally:
        active_commands.pop(user_id, None)
