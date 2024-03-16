from pybit.unified_trading import HTTP
from constants import SYMBOLS, INTERVAL
from asdf import (
    get_dataframe,
    get_macd_signal,
    SignalType,
    Signal,
    analyze_symbol
)
from time import sleep
from bot import TradeBot
import threading


def main():
    session = HTTP()
    bot = TradeBot()

    while True:
        for symbol in SYMBOLS:
            threading.Thread(target=analyze_symbol, args=(session, bot, symbol)).start()
        print('all')
        sleep(INTERVAL)


if __name__ == "__main__":
    main()
