import json
import re
import os
import html
import requests

from time import sleep
from telegram import ParseMode
from telegram import (CallbackQuery, Chat, MessageEntity, InlineKeyboardButton,
                      InlineKeyboardMarkup, Message, Update, Bot, User)
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler,
                          DispatcherHandlerStop, Filters, MessageHandler,
                          run_async)
from telegram.error import BadRequest, RetryAfter, Unauthorized
from telegram.utils.helpers import mention_html, mention_markdown, escape_markdown

from KURUMIBOT.modules.helper_funcs.filters import CustomFilters
from KURUMIBOT.modules.helper_funcs.chat_status import user_admin, user_admin_no_reply
from KURUMIBOT import dispatcher, updater, SUPPORT_CHAT
from KURUMIBOT.modules.log_channel import gloggable

CHATS = []

@user_admin_no_reply
@gloggable
def kukirm(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    chat: Optional[Chat] = update.effective_chat
    match = re.match(r"rm_chat\((.+?)\)", query.data)
    if match:
        user_id = update.effective_user.id
        is_kuki = CHATS.remove(chat.id)
        if is_kuki:
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"AI_DISABLED\n"
                f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "Miku Chatbot disable by {}.".format(mention_html(user.id, user.first_name)),
                parse_mode=ParseMode.HTML,
            )

    return ""

@user_admin_no_reply
@gloggable
def kukiadd(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    chat: Optional[Chat] = update.effective_chat
    user: Optional[User] = update.effective_user
    match = re.match(r"add_chat\((.+?)\)", query.data)
    if match:
        user_id = update.effective_chat.id
        is_kuki = CHATS.append(chat.id)
        if is_kuki:
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"AI_ENABLE\n"
                f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "Miku Chatbot enable by {}.".format(mention_html(user.id, user.first_name)),
                parse_mode=ParseMode.HTML,
            )

    return ""

@user_admin
@gloggable
def kuki(update: Update, context: CallbackContext):
    user = update.effective_user
    message = update.effective_message
    msg = "Choose an option"
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            text="Enable",
            callback_data="add_chat({})"),
        InlineKeyboardButton(
            text="Disable",
            callback_data="rm_chat({})")]])
    message.reply_text(
        msg,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )

def kuki_message(context: CallbackContext, message):
    reply_message = message.reply_to_message
    if message.text.lower() == "kuki":
        return True
    if reply_message:
        if reply_message.from_user.id == context.bot.get_me().id:
            return True
    else:
        return False
        

def chatbot(update: Update, context: CallbackContext):
    message = update.effective_message
    chat: Optional[Chat] = update.effective_chat
    bot = context.bot
    is_kuki = chat.id in CHATS
    if not is_kuki:
        return
	
    if message.text and not message.document:
        if not kuki_message(context, message):
            return
        Message = message.text
        bot.send_chat_action(chat_id=chat.id, action="typing")
        kukiurl = requests.get('http://Kukiapi.xyz/api/apikey=5145883564-KUKISf4kHn2oT0/Miku/@h0daka/message='+Message)
        Kuki = json.loads(kukiurl.text)
        kuki = Kuki['reply']
        sleep(0.3)
        message.reply_text(kuki, timeout=60)

def list_all_chats(update: Update, context: CallbackContext):
    text = "<b>Miku Chatbot Enabled Chats</b>\n"
    for chat in CHATS:
        try:
            x = context.bot.get_chat(int(*chat))
            name = x.title or x.first_name
            text += f"• <code>{name}</code>\n"
        except (BadRequest, Unauthorized):
            CHATS.remove(*chat)
        except RetryAfter as e:
            sleep(e.retry_after)
    update.effective_message.reply_text(text, parse_mode="HTML")

__help__ = """
Chatbot utilizes the Kuki's api which allows Miku to talk and provide a more interactive group chat experience.

*Admins only Commands*:
  ➢ `/Chatbot`*:* Shows chatbot control panel.

"""

__mod_name__ = "ChatBot"


CHATBOTK_HANDLER = CommandHandler("chatbot", kuki, run_async=True)
ADD_CHAT_HANDLER = CallbackQueryHandler(kukiadd, pattern=r"add_chat", run_async=True)
RM_CHAT_HANDLER = CallbackQueryHandler(kukirm, pattern=r"rm_chat", run_async=True)
CHATBOT_HANDLER = MessageHandler(
    Filters.text & (~Filters.regex(r"^#[^\s]+") & ~Filters.regex(r"^!")
                    & ~Filters.regex(r"^\/")), chatbot, run_async=True)
LIST_ALL_CHATS_HANDLER = CommandHandler(
    "allchats", list_all_chats, filters=CustomFilters.dev_filter, run_async=True)

dispatcher.add_handler(ADD_CHAT_HANDLER)
dispatcher.add_handler(CHATBOTK_HANDLER)
dispatcher.add_handler(RM_CHAT_HANDLER)
dispatcher.add_handler(LIST_ALL_CHATS_HANDLER)
dispatcher.add_handler(CHATBOT_HANDLER)

__handlers__ = [
    ADD_CHAT_HANDLER,
    CHATBOTK_HANDLER,
    RM_CHAT_HANDLER,
    LIST_ALL_CHATS_HANDLER,
    CHATBOT_HANDLER,
]
`
