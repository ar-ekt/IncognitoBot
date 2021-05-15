from general import *

class ReplyCommand:
    def command(update: Update, context: CallbackContext) -> int:
        set_user_data(context)
        delete_query(update, context)
        
        update.message.reply_text(Messages.ReplyCommand.START)
        
        context.user_data["active_command"] = "reply"
        
        return States.REPLY_FORWARD
    
    def forward_message(update: Update, context: CallbackContext) -> int:
        forwarded_message = update.effective_message
        if forwarded_message["forward_from_chat"] and forwarded_message["forward_from_chat"]["username"] == CHANNEL_NAME:
            forwarded_message_id = forwarded_message["forward_from_message_id"]
            context.user_data["reply_id"] = forwarded_message_id
            update.message.reply_text(Messages.ReplyCommand.MESSAGE)
            return States.REPLY
        
        else:
            update.message.reply_text(Messages.ReplyCommand.ERROR.format(CHANNEL_NAME))
            return States.REPLY_FORWARD
        
    def message(update: Update, context: CallbackContext) -> int:
        pattern = [[InlineKeyboardButton(text=Messages.CANCEL_MESSAGE, callback_data="reply cancel"),
                    InlineKeyboardButton(text=Messages.SEND_MESSAGE, callback_data="reply send")]]
        markup = InlineKeyboardMarkup(pattern)
        sent_message = update.message.reply_text(Messages.ReplyCommand.SURE, reply_markup=markup)
        
        context.user_data["message_id"] = update.message.message_id
        context.user_data["query_id"] = sent_message.message_id
        
        return States.BEGIN
        
    def handle(update: Update, context: CallbackContext) -> int:
        selected = update.callback_query.data.split()[1]
        
        if selected == "send":
            message_id = context.user_data["message_id"]
            reply_id = context.user_data["reply_id"]
            chat_id = update.callback_query.message.chat_id
            pattern = [[InlineKeyboardButton(text=Messages.MessageMenu.REJECT, callback_data=f"reply reject {reply_id}"),
                        InlineKeyboardButton(text=Messages.MessageMenu.SEND_TO_CHANNEL, callback_data=f"reply send {reply_id}")],
                       [InlineKeyboardButton(text=Messages.MessageMenu.REPLYED_MESSAGE, callback_data="reply link {reply_id}",
                                             url=Messages.ChannelMessage.LINK.format(CHANNEL_NAME, reply_id))]]
            markup = InlineKeyboardMarkup(pattern)
            context.bot.copyMessage(chat_id=PRIVATE_CHANNEL_ID,
                                    from_chat_id=chat_id,
                                    message_id=message_id,
                                    reply_markup=markup)
            text = Messages.ReplyCommand.DONE
        
        elif selected == "cancel":
            text = Messages.ReplyCommand.CANCEL
        
        update.callback_query.message.edit_text(text)
        
        context.user_data["active_command"] = None
        context.user_data["message_id"] = None
        context.user_data["reply_id"] = None
        context.user_data["query_id"] = None
        
        return States.BEGIN