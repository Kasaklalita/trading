import telebot
from constants import BOT_KEY, CHAT_ID


class TradeBot:
    bot: telebot.TeleBot

    def __init__(self):
        self.bot = telebot.TeleBot(token=BOT_KEY)

    def notify(self, message):
        self.bot.send_message(CHAT_ID, message)


# 894133017 id чата с Лизой
