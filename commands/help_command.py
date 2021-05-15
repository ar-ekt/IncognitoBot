from general import *

class HelpCommand:
    def command(update: Update, context: CallbackContext) -> int:
        set_user_data(context)
        delete_query(update, context)
               
        update.message.reply_text(Messages.HELP.format(BOT_NAME, CHANNEL_NAME))
        
        return States.BEGIN
