from TofuXrobot import telethn as tbot
from TofuXrobot.events import register
import os
import asyncio
import os
import time

from datetime import datetime
from TofuXrobot import OWNER_ID, DEV_USERS
from TofuXrobot import TEMP_DOWNLOAD_DIRECTORY as path
from TofuXrobot import TEMP_DOWNLOAD_DIRECTORY
from datetime import datetime
water = './TofuXrobot/imagefiles/IMG_20211114_164239_236.jpg'
client = tbot

@register(pattern=r"^/gift ?(.*)")
async def Prof(event):
    if event.sender_id == OWNER_ID or event.sender_id == DEV_USERS:
        pass
    else:
        return
    thumb = water
    message_id = event.message.id
    input_str = event.pattern_match.group(1)
    the_plugin_file = "./TofuXrobot/modules/{}.py".format(input_str)
    if os.path.exists(the_plugin_file):
     message_id = event.message.id
     await event.client.send_file(
             event.chat_id,
             the_plugin_file,
             force_document=True,
             allow_cache=False,
             thumb=thumb,
             reply_to=message_id,
         )
    else:
        await event.reply("No File Found!")
