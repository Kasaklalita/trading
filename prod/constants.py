from decouple import Csv, config

API_KEY = config("API_KEY")
SECRET_KEY = config("SECRET_KEY")
TAKE_PROFIT = config("TAKE_PROFIT", cast=float)
STOP_LOSS = config("STOP_LOSS", cast=float)
SYMBOLS = config("SYMBOLS", cast=Csv())

INTERVAL = config("INTERVAL", cast=int)
LIMIT = config("LIMIT", cast=int)
BOT_KEY = config("BOT_KEY")
CHAT_IDS = config("CHAT_IDS", cast=Csv(int))

INTERVALS = ['1', '3', '5', '15', '30', '60', '120', '240', '360', '720', 'D', 'M', 'W']
