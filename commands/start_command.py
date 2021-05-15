from general import *

class StartCommand:
    def command(update: Update, context: CallbackContext) -> int:
        set_user_data(context)
        delete_query(update, context)
        
        update.message.reply_text(Messages.START.format(BOT_NAME, CHANNEL_NAME))
        
        return States.BEGIN