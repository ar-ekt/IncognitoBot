from general import *

from classes.commands.send_command import SendCommand
from classes.commands.reply_command import ReplyCommand
from classes.commands.admin_command import AdminCommand

from classes.web import Web

class QueryHandler:
    def private_channel_handle(update: Update, context: CallbackContext) -> None:
        selected = update.callback_query.data.split()
        message_type, action = selected[0:2]
        
        message = update.callback_query.message
        message_id = message.message_id
        
        message_web_id = int(selected[2])
        reply_id = int(selected[3]) if int(selected[3]) != -1 else None
        
        if message.text != None:
            message_text = message.text or ""
            
            if action == "send":
                text_main_channel = Messages.ChannelMessage.FORMAT.format(message_text)
                context.bot.sendMessage(chat_id=f"@{CHANNEL_NAME}",
                                        text=text_main_channel,
                                        reply_to_message_id=reply_id,
                                        allow_sending_without_reply=True,
                                        parse_mode=ParseMode.MARKDOWN,
                                        disable_web_page_preview=True)
                
                text_private_channel = Messages.MessageMenu.Send_TO_CHANNEL_STATE.format(message_text)
            
            elif action == "reject":
                text_private_channel = Messages.MessageMenu.REJECT_STATE.format(message_text)
                
            update.callback_query.message.edit_text(text=text_private_channel, reply_markup=None)
            
            if message_web_id == -1:
                Web.send_bot_message(message_text,
                                     reply_id if reply_id != None else -1,
                                     int(action == "send"))
            
        else:
            message_caption = message.caption or ""
            
            if action == "send":
                caption_main_channel = Messages.ChannelMessage.FORMAT.format(message_caption)
                context.bot.copyMessage(chat_id=f"@{CHANNEL_NAME}",
                                        from_chat_id=PRIVATE_CHANNEL_ID,
                                        message_id=message_id,
                                        reply_to_message_id=reply_id,
                                        allow_sending_without_reply=True,
                                        caption=caption_main_channel,
                                        parse_mode=ParseMode.MARKDOWN)
                
                caption_private_channel = Messages.MessageMenu.Send_TO_CHANNEL_STATE.format(message_caption)
            
            elif action == "reject":
                caption_private_channel = Messages.MessageMenu.REJECT_STATE.format(message_caption)
            
            try:
                update.callback_query.message.edit_caption(caption=caption_private_channel, reply_markup=None)
            except:
                update.callback_query.edit_message_reply_markup(reply_markup=None)
        
        if message_web_id != -1 and action == "send":
            Web.accept_web_message(message_web_id)
        
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