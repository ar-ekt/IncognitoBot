from general import *

class SendCommand:
    def command(update: Update, context: CallbackContext) -> int:
        set_user_data(context)
        delete_query(update, context)
        
        update.message.reply_text(Messages.SendCommand.START)
        
        context.user_data["active_command"] = "send"
        
        return States.SEND
        
    def message(update: Update, context: CallbackContext) -> int:
        pattern = [[InlineKeyboardButton(text=Messages.CANCEL_MESSAGE, callback_data="send cancel"),
                    InlineKeyboardButton(text=Messages.SEND_MESSAGE, callback_data="send send")]]
        markup = InlineKeyboardMarkup(pattern)
        sent_message = update.message.reply_text(Messages.SendCommand.SURE, reply_markup=markup)
        
        context.user_data["message_id"] = update.message.message_id
        context.user_data["query_id"] = sent_message.message_id
        
        return States.BEGIN
    
    def handle(update: Update, context: CallbackContext) -> int:
        selected = update.callback_query.data.split()[1]
        
        if selected == "send":
            message_id = context.user_data["message_id"]
            chat_id = update.callback_query.message.chat_id
            pattern = [[InlineKeyboardButton(text=Messages.MessageMenu.REJECT, callback_data="send reject"),
                        InlineKeyboardButton(text=Messages.MessageMenu.SEND_TO_CHANNEL, callback_data="send send")]]
            markup = InlineKeyboardMarkup(pattern)
            context.bot.copyMessage(chat_id=PRIVATE_CHANNEL_ID,
                                    from_chat_id=chat_id,
                                    message_id=message_id,
                                    reply_markup=markup)
            text = Messages.SendCommand.DONE
        
        elif selected == "cancel":
            text = Messages.SendCommand.CANCEL
        
        update.callback_query.message.edit_text(text)
        
        context.user_data["active_command"] = None
        context.user_data["message_id"] = None
        context.user_data["query_id"] = None
        
        return States.BEGIN