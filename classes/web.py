from general import *

class Web:
    def send_message_to_private_channel(context: CallbackContext, message: dict) -> None:
        message_id: int = message["id"]
        messages_text: str = message["content"]
        reply_id: int = message["reply_id"]
        
        if reply_id == -1:
            pattern = [[InlineKeyboardButton(text=Messages.MessageMenu.REJECT, callback_data=f"send reject {message_id} -1"),
                        InlineKeyboardButton(text=Messages.MessageMenu.SEND_TO_CHANNEL, callback_data=f"send send {message_id} -1")]]
        else:
            pattern = [[InlineKeyboardButton(text=Messages.MessageMenu.REJECT, callback_data=f"reply reject {message_id} {reply_id}"),
                        InlineKeyboardButton(text=Messages.MessageMenu.SEND_TO_CHANNEL, callback_data=f"reply send {message_id} {reply_id}")],
                       [InlineKeyboardButton(text=Messages.MessageMenu.REPLYED_MESSAGE, callback_data="reply link {message_id} {reply_id}",
                                             url=Messages.ChannelMessage.LINK.format(CHANNEL_NAME, reply_id))]]
        markup = InlineKeyboardMarkup(pattern)
        
        try:
            context.bot.send_message(PRIVATE_CHANNEL_ID, messages_text, reply_markup=markup)
            context.bot_data["last_web_message_id"] = message_id
        except:
            pass
    
    def get_web_messages(context: CallbackContext) -> None:
        last_message_id = context.bot_data["last_web_message_id"]
        
        response = requests.get("http://{}/api.php?TOKEN={}&last={}".format(WEB_URL, WEB_API_TOKEN, last_message_id))
        if response.status_code == 200:
            messages = json.loads(response.content)
            for message in messages:
                Web.send_message_to_private_channel(context, message)
            
    def accept_web_message(message_id: int) -> None:
        requests.get("http://{}/api.php?TOKEN={}&accept={}".format(WEB_URL, WEB_API_TOKEN, message_id))
    
    def send_bot_message(message_text: str, reply_id: int, status: int) -> None:
        requests.post("http://{}/api.php?TOKEN={}&content={}&reply_id={}&status={}".format(WEB_URL, WEB_API_TOKEN, message_text, reply_id, status))