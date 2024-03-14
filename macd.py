from pybit.unified_trading import HTTP
import pandas as pd
import pandas_ta as ta
import numpy as np
from time import sleep
from asdf import (
    get_dataframe,
    get_full_dataframe,
    get_signal_for_candle,
    SignalType,
    Signal,
)
from decouple import config
import matplotlib.pyplot as plt


API_KEY = config("API_KEY")
SECRET_KEY = config("SECRET_KEY")


def main():
    session = HTTP()
    position_opened = False

    df = get_dataframe(session, "OPUSDT", 3, 500)
    df = get_full_dataframe(df)

    signals: [Signal] = []

    for i in range(0, len(df.index) - 2):
        signal: Signal = get_signal_for_candle(df, i, position_opened)
        if signal.type == SignalType.BUY:
            print(signal)
            signals.append(signal)
            position_opened = True
        elif signal.type == SignalType.SELL:
            print(signal)
            signals.append(signal)
            position_opened = False
        else:
            pass

    print(df)

    # plt.plot(df["MACDs_12_26_9"], label="signal", color="red")
    # plt.plot(df["MACD_12_26_9"], label="MACD", color="green")
    plt.plot(df["close"], color="black")
    for signal in signals:
        if signal.type == SignalType.BUY:
            plt.scatter(
                signal.time, signal.entry_point, color="green", s=100, marker="o"
            )
        else:
            plt.scatter(signal.time, signal.entry_point, color="red", s=100, marker="o")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
