from general import *

from commands.send_command import SendCommand
from commands.reply_command import ReplyCommand
from commands.admin_command import AdminCommand

class QueryHandler:
    def private_channel_handle(update: Update, context: CallbackContext) -> None:
        selected = update.callback_query.data.split()
        message_type, action = selected[0:2]
        
        message = update.callback_query.message
        message_id = message.message_id
        
        reply_id = int(selected[2]) if message_type == "reply" else None
                        
        if message.text != None:
            message_text = message.text or ""
            
            if action == "send":
                text_main_channel = Messages.ChannelMessage.FORMAT.format(message_text, CHANNEL_NAME, BOT_NAME)
                context.bot.sendMessage(chat_id=f"@{CHANNEL_NAME}",
                                        text=text_main_channel,
                                        reply_to_message_id=reply_id,
                                        allow_sending_without_reply=True)
            
                text_private_channel = Messages.MessageMenu.Send_TO_CHANNEL_STATE.format(message_text)
            
            elif action == "reject":
                text_private_channel = Messages.MessageMenu.REJECT_STATE.format(message_text)
                
            update.callback_query.message.edit_text(text=text_private_channel, reply_markup=None)
            
        else:
            message_caption = message.caption or ""
            
            if action == "send":
                caption_main_channel = Messages.ChannelMessage.FORMAT.format(message_caption, CHANNEL_NAME, BOT_NAME)
                context.bot.copyMessage(chat_id=f"@{CHANNEL_NAME}",
                                        from_chat_id=PRIVATE_CHANNEL_ID,
                                        message_id=message_id,
                                        reply_to_message_id=reply_id,
                                        allow_sending_without_reply=True,
                                        caption=caption_main_channel)
                
                caption_private_channel = Messages.MessageMenu.Send_TO_CHANNEL_STATE.format(message_caption)
            
            elif action == "reject":
                caption_private_channel = Messages.MessageMenu.REJECT_STATE.format(message_caption)
            
            try:
                update.callback_query.message.edit_caption(caption=caption_private_channel, reply_markup=None)
            except:
                update.callback_query.edit_message_reply_markup(reply_markup=None)
        
        answer_message = Messages.MessageMenu.SEND_TO_CHANNEL_DONE if action == "send" else Messages.MessageMenu.REJECT_DONE
        update.callback_query.answer(answer_message)
    
    def handle(update: Update, context: CallbackContext) -> int:
        chat_id = update.callback_query.message.chat_id
        
        message_type = update.callback_query.data.split()[0]
        
        if chat_id == PRIVATE_CHANNEL_ID:
            QueryHandler.private_channel_handle(update, context)
        
        elif message_type == "admin":
            AdminCommand.handle(update, context)
        
        elif message_type == "reply":
            ReplyCommand.handle(update, context)
        
        elif message_type == "send":
            SendCommand.handle(update, context)
        
        return States.BEGIN