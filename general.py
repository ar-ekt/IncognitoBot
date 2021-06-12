from telegram import (Update,
                      ParseMode,
                      InlineKeyboardButton,
                      InlineKeyboardMarkup)

from telegram.ext import (Updater,
                          Filters,
                          CommandHandler,
                          MessageHandler,
                          CallbackContext,
                          ConversationHandler,
                          CallbackQueryHandler)

from telegram.utils.helpers import escape_markdown

import requests
import json

from environ_vars import *
from classes.messages import Messages

def set_user_data(context: CallbackContext) -> None:
    if not context.user_data:
        key_values = {"active_command": None,
                      "message_id": None,
                      "reply_id": None,
                      "query_id": None}
        for key, value in key_values.items():
            context.user_data[key] = value
    
def delete_query(update: Update, context: CallbackContext) -> None:
    if context.user_data["query_id"] != None:
        user_id = update.message.from_user.id
        try:
            context.bot.deleteMessage(user_id, context.user_data["query_id"])
        except:
            pass
        context.user_data["query_id"] = None

class States:
    BEGIN, SEND, REPLY, ADMIN, REPLY_FORWARD = range(0, 5)