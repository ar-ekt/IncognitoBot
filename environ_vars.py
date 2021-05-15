import os

NAME = "arcane-retreat-34149" # os.environ.get("APP_NAME")
PORT = os.environ.get('PORT')

TOKEN = os.environ.get("TOKEN")
BOT_ID = TOKEN[:TOKEN.index(":")]
BOT_NAME = "CseIncognitoBot" # os.environ.get("BOT_NAME")

CHANNEL_NAME = "CseIncognito" # os.environ.get("CHANNEL_NAME")
PRIVATE_CHANNEL_ID = int(os.environ.get("PRIVATE_CHANNEL_ID"))
