import pandas as pd
import pandas_ta as ta
from enum import Enum


class SignalType(Enum):
    BUY = 1
    SELL = 2
    HOLD = 3


class Signal:
    type: SignalType
    time: int
    entry_point: int
    take_profit: int
    stop_loss: int

    def __init__(self, type=SignalType.HOLD, time: int = 0, entry_point: int = 0, take_profit: int = 0, stop_loss: int = 0):
        self.type = type
        self.time = time
        self.entry_point = entry_point
        self.take_profit = take_profit
        self.stop_loss = stop_loss


def get_dataframe(session, symbol, interval, limit) -> pd.DataFrame:
    kline = session.get_kline(symbol=symbol, interval=interval, limit=limit)['result']['list']
    df = pd.DataFrame(
        data=kline,
        columns=["time", "open", "highest", "lowest", "close", "volume", "turnover"],
        dtype="float64",
    )
    df = df[::-1]
    df.index = df["time"].values.astype(int)
    # del df["time"]
    df.apply(pd.to_numeric)
    df['time'] = df['time'].astype(int)
    return df


def get_full_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # calculate MACD values
    df.ta.macd(close='close', fast=12, slow=26, append=True)
    # calculating the 200 EMA
    df['EMA200'] = ta.ema(df['close'], length=200)
    return df


def get_signal_for_candle(df: pd.DataFrame, i: int = 0, opened_position: bool = False):
    prev_h, cur_h = df['MACDh_12_26_9'].iloc[i-2], df['MACDh_12_26_9'].iloc[i-1]
    cur_MAgithCD, cur_signal = df['MACD_12_26_9'].iloc[i-1], df['MACDs_12_26_9'].iloc[i-1]
    cur_price = df['close'].iloc[i-1]
    cur_200ema = df['EMA200'].iloc[i-1]
    # Добавить условие
    # 1. Позиция не открыта
    # 2. Пересечение линий
    # 3. Цена ниже 200 EMA
    if not opened_position and (prev_h < 0 and cur_h > 0) and (cur_price > cur_200ema):
        return Signal(SignalType.BUY, time=df['time'].iloc[i-1])
    elif opened_position and (prev_h > 0 and cur_h < 0) and (cur_price < cur_200ema):
        return Signal(SignalType.SELL, time=df['time'].iloc[i-1])
    return Signal()
