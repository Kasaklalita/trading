from decouple import config

API_KEY = config("API_KEY")
SECRET_KEY = config("SECRET_KEY")
TAKE_PROFIT = config("TAKE_PROFIT", cast=float)
STOP_LOSS = config("STOP_LOSS", cast=float)
SYMBOL = config("SYMBOL")
SCALE = config("SCALE", cast=int)
RANGE = config("RANGE", cast=int)
BOT_KEY = config("BOT_KEY")
CHAT_ID = config("CHAT_ID", cast=int)
