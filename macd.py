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
    position_opened = False

    df = get_dataframe(session, SYMBOL, SCALE, RANGE)
    df = get_full_dataframe(df)

    signals: [Signal] = []

    for i in range(0, len(df.index) - 2):
        signal: Signal = get_signal_for_candle(
            df, i, position_opened, take_profit=TAKE_PROFIT, stop_loss=STOP_LOSS
        )
        if signal.type == SignalType.LONG:
            print(signal)
            signals.append(signal)
            position_opened = True
        elif signal.type == SignalType.SHORT:
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
        if signal.type == SignalType.LONG:
            plt.scatter(
                signal.unix, signal.entry_point, color="green", s=100, marker="o"
            )
        else:
            plt.scatter(signal.unix, signal.entry_point, color="red", s=100, marker="o")
    # plt.legend()
    # plt.show()


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
        if signal.type == SignalType.LONG:
            print(signal)
            signals_count += 1
            current_signal = signal
            # LONG
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
