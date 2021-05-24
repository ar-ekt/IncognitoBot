from general import *

from classes.commands.start_command import StartCommand
from classes.commands.help_command import HelpCommand
from classes.commands.send_command import SendCommand
from classes.commands.reply_command import ReplyCommand
from classes.commands.admin_command import AdminCommand
from classes.commands.cancel_command import CancelCommand

from classes.query_handler import QueryHandler

from classes.web import Web

class Bot:
    def __init__(self):
        self.updater = Updater(TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.set_conversation_handler()
        self.dispatcher.add_handler(self.conversation_handler)
        self.dispatcher.add_handler(CallbackQueryHandler(QueryHandler.handle))
        
        self.dispatcher.bot_data["last_web_message_id"] = 0
    
    def run(self) -> None:
        self.updater.job_queue.run_repeating(Web.get_web_messages, WEB_REQUEST_TIME*60)
        
        if PORT:
            self.updater.start_webhook(listen = "0.0.0.0",
                                       port = int(PORT),
                                       url_path = TOKEN,
                                       webhook_url = "https://{}.herokuapp.com/{}".format(NAME, TOKEN))
        else:
            self.updater.start_polling()
            
        self.updater.idle()
    
    def wrong_command(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text(Messages.UNRECOGNIZED_COMMAND)
        
        return States.BEGIN
    
    def set_conversation_handler(self) -> None:
        commands = [CommandHandler(command="start", callback=StartCommand.command, filters=Filters.chat_type.private),
                    CommandHandler(command="help", callback=HelpCommand.command, filters=Filters.chat_type.private),
                    CommandHandler(command="send", callback=SendCommand.command, filters=Filters.chat_type.private),
                    CommandHandler(command="reply", callback=ReplyCommand.command, filters=Filters.chat_type.private),
                    CommandHandler(command="admin", callback=AdminCommand.command, filters=Filters.chat_type.private),
                    CommandHandler(command="cancel", callback=CancelCommand.command, filters=Filters.chat_type.private),
                    MessageHandler(Filters.text & Filters.command & ~Filters.via_bot(BOT_ID) & Filters.chat_type.private, self.wrong_command)]

        self.conversation_handler = ConversationHandler(
            entry_points = commands,
            states = {
                States.BEGIN: commands,
                
                States.SEND: [
                    MessageHandler(Filters.all & ~Filters.command & ~Filters.via_bot(BOT_ID) & Filters.chat_type.private & ~Filters.update.edited_message, SendCommand.message)
                ] + commands,
                
                States.REPLY: [
                    MessageHandler(Filters.all & ~Filters.command & ~Filters.via_bot(BOT_ID) & Filters.chat_type.private & ~Filters.update.edited_message, ReplyCommand.message)
                ] + commands,
                
                States.ADMIN: [
                    MessageHandler(Filters.all & ~Filters.command & ~Filters.via_bot(BOT_ID) & Filters.chat_type.private & ~Filters.update.edited_message, AdminCommand.message)
                ] + commands,
                
                States.REPLY_FORWARD: [
                    MessageHandler(Filters.all & Filters.forwarded & Filters.chat_type.private & ~Filters.update.edited_message, ReplyCommand.forward_message)
                ] + commands,
            },
            fallbacks = [],
        )