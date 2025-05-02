# (©)Codexbotz

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from helper_func import encode, get_message_id, admin
import asyncio

@Bot.on_message(filters.private & admin & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(text = "Forward the First Message from DB Channel (with Quotes)..\n\nor Send the DB Channel Post Link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote = True)
            continue

    while True:
        try:
            second_message = await client.ask(text = "Forward the Last Message from DB Channel (with Quotes)..\nor Send the DB Channel Post link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote = True)
            continue

    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await second_message.reply_text(f"<b>Here is your link</b>\n\n{link}", quote=True, reply_markup=reply_markup)

@Bot.on_message(filters.private & admin & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(text = "Forward Message from the DB Channel (with Quotes)..\nor Send the DB Channel Post link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is not taken from DB Channel", quote = True)
            continue

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await channel_message.reply_text(f"<b>Here is your link</b>\n\n{link}", quote=True, reply_markup=reply_markup)

@Bot.on_message(filters.private & admin & filters.command("custom_batch"))
async def custom_batch(client: Client, message: Message):
    collected = []  # সংগ্রহ করা বার্তার আইডি সংরক্ষণের জন্য লিস্ট
    stop_event = asyncio.Event()  # "STOP" বাটন টিপা পর্যন্ত অপেক্ষা করার জন্য ইভেন্ট

    # প্রথম বার্তা, এখানে কোনো বাটন নেই
    await message.reply("Send all messages you want to include in batch.\n\nPress STOP when you're done.")

    # বার্তা সংগ্রহের জন্য হ্যান্ডলার ফাংশন
    async def collect_messages(client, msg):
        try:
            sent = await msg.copy(client.db_channel.id, disable_notification=True)
            collected.append(sent.id)
        except Exception as e:
            await msg.reply(f"❌ Failed to store a message:\n<code>{e}</code>")

    # ইনলাইন কীবোর্ড তৈরি
    stop_button = InlineKeyboardButton("STOP", callback_data="stop_batch")
    stop_keyboard = InlineKeyboardMarkup([[stop_button]])

    # ব্যবহারকারীর বার্তার জন্য অপেক্ষা করা শুরু
    collect_handler = MessageHandler(collect_messages, filters.user(message.from_user.id))
    client.add_handler(collect_handler)

    # "Waiting for files/messages..." বার্তা পাঠানো, এখানে STOP বাটন যোগ করা হবে
    waiting_msg = await message.reply("Waiting for files/messages...\nPress STOP to finish.", reply_markup=stop_keyboard)

    # "STOP" বাটন টিপলে কী হবে তার হ্যান্ডলার
    async def stop_batch_handler(client, callback_query):
        if callback_query.data == "stop_batch":
            stop_event.set()  # ইভেন্ট সেট করে লুপ বন্ধ করা
            client.remove_handler(collect_handler)  # মেসেজ হ্যান্ডলার সরানো
            await callback_query.answer("Batch collection stopped.")  # ব্যবহারকারীকে জানানো

    # কলব্যাক হ্যান্ডলার যোগ করা
    stop_handler = CallbackQueryHandler(stop_batch_handler, filters.regex("stop_batch"))
    client.add_handler(stop_handler)

    # "STOP" বাটন টিপা পর্যন্ত অপেক্ষা
    await stop_event.wait()

    # হ্যান্ডলার সরানো
    client.remove_handler(stop_handler)

    # যদি কোনো বার্তা সংগ্রহ না হয়
    if not collected:
        await message.reply("❌ No messages were added to batch.")
        return

    # ব্যাচ লিঙ্ক তৈরি
    start_id = collected[0] * abs(client.db_channel.id)
    end_id = collected[-1] * abs(client.db_channel.id)
    string = f"get-{start_id}-{end_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await message.reply(f"<b>Here is your custom batch link:</b>\n\n{link}", reply_markup=reply_markup)
