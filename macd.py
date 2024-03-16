from pybit.unified_trading import HTTP
from asdf import (
    get_dataframe,
    get_full_dataframe,
    get_signal_for_candle,
    SignalType,
    Signal,
)
import matplotlib.pyplot as plt
from constants import API_KEY, SECRET_KEY, TAKE_PROFIT, STOP_LOSS, SYMBOL, SCALE, RANGE


def main():
    session = HTTP()

    df = get_dataframe(session, SYMBOL, SCALE, RANGE)
    df = get_full_dataframe(df)

    current_signal = None
    signals_count = 0
    take_profits, stop_losses = 0, 0

    for i in range(0, len(df.index) - 2):
        low, high = df["lowest"].iloc[i - 1], df["highest"].iloc[i - 1]
        # probable signal on current candle
        signal: Signal = get_signal_for_candle(
            df,
            i,
            bool(current_signal),
            take_profit=TAKE_PROFIT,
            stop_loss=STOP_LOSS,
        )
        if signal.type == SignalType.BUY:
            print(signal)
            signals_count += 1
            current_signal = signal
            # BUY
        elif current_signal:
            if high > current_signal.take_profit:
                print("TAKE_PROFIT", df["datetime"].iloc[i - 1])
                current_signal = None
                take_profits += 1
            elif low < current_signal.stop_loss:
                print("STOP LOSS", df["datetime"].iloc[i - 1])
                current_signal = None
                stop_losses += 1

    print(signals_count, take_profits, stop_losses)


def backtest():
    session = HTTP()

    df = get_dataframe(session, SYMBOL, SCALE, RANGE)
    df = get_full_dataframe(df)

    current_signal = None
    signals_count = 0
    take_profits, stop_losses = 0, 0

    for i in range(0, len(df.index) - 2):
        low, high = df["lowest"].iloc[i - 1], df["highest"].iloc[i - 1]
        # probable signal on current candle
        signal: Signal = get_signal_for_candle(
            df,
            i,
            bool(current_signal),
            take_profit=TAKE_PROFIT,
            stop_loss=STOP_LOSS,
        )
        if signal.type == SignalType.BUY:
            print(signal)
            signals_count += 1
            current_signal = signal
            # BUY
        elif current_signal:
            if high > current_signal.take_profit:
                print("TAKE_PROFIT", df["datetime"].iloc[i - 1])
                current_signal = None
                take_profits += 1
            elif low < current_signal.stop_loss:
                print("STOP LOSS", df["datetime"].iloc[i - 1])
                current_signal = None
                stop_losses += 1

    print(signals_count, take_profits, stop_losses)


if __name__ == "__main__":
    backtest()
