from pybit.unified_trading import HTTP
import pandas as pd
import pandas_ta as ta
import numpy as np
from time import sleep
from asdf import get_dataframe, get_full_dataframe, get_signal_for_candle, SignalType, Signal


def main():
    session = HTTP(
      
    )
    position_opened = False

    df = get_dataframe(session, 'OPUSDT', 3, 1000)
    df = get_full_dataframe(df)

    for i in range(0, len(df.index) - 2):
        signal: Signal = get_signal_for_candle(df, i, position_opened)
        if signal.type == SignalType.BUY:
            print(signal.type, signal.time)
            position_opened = True
        elif signal.type == SignalType.SELL:
            print(signal.type, signal.time)
            position_opened = False
        else:
            pass


def tradingstrat(session, open_position=False):
    while True:
        df = get_dataframe(session, 'OPUSDT', 3, 1000)
        df = get_full_dataframe(df)
        print(df.size-2)
        print('')
        for i in range(0, df.size - 2):
            signal: Signal = get_signal_for_candle(df, i, True)
            print(signal)

        # print(prev_h, cur_h)
        # print(cur_MACD, cur_signal)
        return


if __name__ == '__main__':
    main()
