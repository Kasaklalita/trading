from pybit.unified_trading import HTTP
from constants import SYMBOLS
from asdf import (
    Signal,
    analyze_symbol
)
from time import sleep
from bot import TradeBot
from typing import Dict
import threading


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
