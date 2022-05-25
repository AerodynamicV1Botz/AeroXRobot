import asyncio
import telegram
import os
import requests
import datetime
import time
from PIL import Image
from io import BytesIO
from datetime import datetime
import random
from telethon import events, Button, custom, version
from TofuXrobot.events import register
from TofuXrobot import telethn as borg, OWNER_ID, OWNER_NAME
from TofuXrobot import StartTime, dispatcher
from telethon.tl.types import ChannelParticipantsAdmins
from pyrogram import __version__ as pyro


edit_time = 5
""" =======================CONSTANTS====================== """
file1 = "https://telegra.ph/file/dbb4b4277d305749a0798.png"
file2 = "https://telegra.ph/file/e264055da5e43d58f08e9.png"
file3 = "https://telegra.ph/file/ad0b6b42d4f9cad1e0954.png"
file4 = "https://telegra.ph/file/612e817351d4e8f8f4452.png"
""" =======================CONSTANTS====================== """

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)

@register(pattern=("/alive"))
async def hmm(yes):
    chat = await yes.get_chat()
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    Tofu = f"♡ **Hey [{yes.sender.first_name}](tg://user?id={yes.sender.id}), I'm Tofu**\n\n"
    Tofu += f"♡ **My Uptime** ~♪ `{uptime}`\n\n"
    Tofu += f"♡ **Telethon Version** ~♪ `{version.__version__}`\n\n"
    Tofu += f"♡ **Python Telegram Bot Version** ~♪ `{telegram.__version__}`\n\n"
    Tofu += f"♡ **Pyrogram Version** ~♪ `{pyro}`\n\n"
    Tofu += f"♡ **My Master** ~♪ [{OWNER_NAME}](tg://user?id={OWNER_ID})\n\n"
    Tofu += f"Thanks For Adding Me In {yes.chat.title}"
    BUTTON = [[Button.url("Support Chat", "https://t.me/tofu_support"), Button.url("Updates Channel", "https://t.me/Pegasusupdates")]]
    on = await borg.send_file(yes.chat_id, file=file2,caption=Tofu, buttons=BUTTON)

    await asyncio.sleep(edit_time)
    ok = await borg.edit_message(yes.chat_id, on, file=file3, buttons=BUTTON) 

    await asyncio.sleep(edit_time)
    ok2 = await borg.edit_message(yes.chat_id, ok, file=file4, buttons=BUTTON)

    await asyncio.sleep(edit_time)
    ok3 = await borg.edit_message(yes.chat_id, ok2, file=file1, buttons=BUTTON)
    
    await asyncio.sleep(edit_time)
    ok4 = await borg.edit_message(yes.chat_id, ok3, file=file2, buttons=BUTTON)
    
    await asyncio.sleep(edit_time)
    ok5 = await borg.edit_message(yes.chat_id, ok4, file=file1, buttons=BUTTON)
    
    await asyncio.sleep(edit_time)
    ok6 = await borg.edit_message(yes.chat_id, ok5, file=file3, buttons=BUTTON)
    
    await asyncio.sleep(edit_time)
    ok7 = await borg.edit_message(yes.chat_id, ok6, file=file4, buttons=BUTTON)

@register(pattern=("/repo"))
async def repo(event):
    Tofu = f"**Hey [{event.sender.first_name}](tg://user?id={event.sender.id}), Click The Button Below To Get My Repo**\n\n"
    BUTTON = [[Button.url("[► Support ◄]", "https://t.me/tofu_support"), Button.url("[► Repo ◄]", "https://github.com/Awesome-Tofu/Tofu-Robot")]]
    await borg.send_file(event.chat_id, file="https://telegra.ph/file/f627bc499679927ba7a4e.png", caption=Tofu, buttons=BUTTON)
