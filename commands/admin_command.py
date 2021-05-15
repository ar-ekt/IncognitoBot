from general import *

class AdminCommand:
    def command(update: Update, context: CallbackContext) -> int:
        set_user_data(context)
        delete_query(update, context)
        
        update.message.reply_text(Messages.AdminCommand.START)
        
        context.user_data["active_command"] = "admin"
        
        return States.ADMIN
        
    def message(update: Update, context: CallbackContext) -> int:
        message_text = update.message.text
    
        pattern = [[InlineKeyboardButton(text=Messages.CANCEL_MESSAGE, callback_data="admin cancel"),
                    InlineKeyboardButton(text=Messages.SEND_MESSAGE, callback_data="admin send")]]
        markup = InlineKeyboardMarkup(pattern)
        sent_message = update.message.reply_text(Messages.AdminCommand.SURE, reply_markup=markup)
        
        context.user_data["message_id"] = update.message.message_id
        context.user_data["query_id"] = sent_message.message_id
    
        return States.BEGIN
        
    def handle(update: Update, context: CallbackContext) -> int:
        selected = update.callback_query.data.split()[1]
                
        if selected == "send":
            message_id = context.user_data["message_id"]
            chat_id = update.callback_query.message.chat_id
            
            sent_message = context.bot.copyMessage(chat_id=PRIVATE_CHANNEL_ID,
                                                   from_chat_id=chat_id,
                                                   message_id=message_id)
            
            text = Messages.AdminCommand.DONE
        
        elif selected == "cancel":
            text = Messages.AdminCommand.CANCEL
            
        update.callback_query.message.edit_text(text)
        
        context.user_data["active_command"] = None
        context.user_data["message_id"] = None
        context.user_data["query_id"] = None
        
        return States.BEGIN