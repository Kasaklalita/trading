from decouple import config, Csv

API_KEY = config("API_KEY")
SECRET_KEY = config("SECRET_KEY")
TAKE_PROFIT = config("TAKE_PROFIT", cast=float)
STOP_LOSS = config("STOP_LOSS", cast=float)
SYMBOLS = config("SYMBOLS", cast=Csv())
INTERVAL = config("INTERVAL", cast=int)
LIMIT = config("LIMIT", cast=int)
BOT_KEY = config("BOT_KEY")
CHAT_ID = config("CHAT_ID", cast=int)
