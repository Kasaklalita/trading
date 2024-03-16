from pybit.unified_trading import HTTP
from asdf import (
    get_dataframe,
    get_macd_signal,
    SignalType,
    Signal,
)
from constants import TAKE_PROFIT, STOP_LOSS, SYMBOL, SCALE, RANGE
from time import sleep
from bot import TradeBot


def main():
    session = HTTP()

    df = get_dataframe(session, SYMBOL, SCALE, RANGE)

    bot = TradeBot()

    while True:
        signal: Signal = get_macd_signal(
            df,
            0,
            take_profit=TAKE_PROFIT,
            stop_loss=STOP_LOSS,
        )
        if signal.type == SignalType.BUY:
            pass
        elif signal.type == SignalType.SELL:
            pass
        else:
            pass
        bot.notify(signal.__str__())
        sleep(SCALE * 55)


if __name__ == "__main__":
    main()
