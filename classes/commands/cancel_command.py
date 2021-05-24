from general import *

class CancelCommand:
    def command(update: Update, context: CallbackContext) -> int:
        set_user_data(context)
        delete_query(update, context)
        
        active_command = context.user_data["active_command"]
        if active_command == None:
            text = Messages.CancelCommand.ERROR
        else:
            context.user_data["active_command"] = None
            text = Messages.CancelCommand.DONE.format(active_command)
        update.message.reply_text(text)
        
        return States.BEGIN