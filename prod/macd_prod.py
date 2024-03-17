import threading
from time import sleep
from typing import Dict

from pybit.unified_trading import HTTP

from asdf import Signal, analyze_symbol
from bot import TradeBot
from constants import SYMBOLS


def main():
    session = HTTP()
    bot = TradeBot()

    current_signals: Dict[str, Signal] = {}

    while True:
        for symbol in SYMBOLS:
            threading.Thread(target=analyze_symbol, args=(session, bot, symbol, current_signals)).start()
        print(SYMBOLS)
        sleep(60)


if __name__ == "__main__":
    main()
