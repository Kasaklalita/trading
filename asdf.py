import pandas as pd
import pandas_ta as ta
from enum import Enum
from copy import deepcopy


class SignalType(Enum):
    BUY = 1
    SELL = 2
    HOLD = 3


class Swap(Enum):
    UP = 1  # switched to up
    DOWN = 2  # switched to down
    STALL = 3  # didn`t switch


class Signal:
    type: SignalType
    datetime: str
    entry_point: int
    take_profit: int
    stop_loss: int

    def __init__(
        self,
        type=SignalType.HOLD,
        unix: int = 0,
        datetime: str = "",
        entry_point: int = 0,
        take_profit: int = 0,
        stop_loss: int = 0,
    ):
        self.type = type
        self.unix = unix
        self.datetime = datetime
        self.entry_point = entry_point
        self.take_profit = take_profit
        self.stop_loss = stop_loss

    def __str__(self):
        return f"Time: {self.datetime}, type: {self.type}, entry: {self.entry_point}, tp: {self.take_profit}, sl: {self.stop_loss}"

    def __repr__(self):
        return f"Time: {self.datetime}, type: {self.type}, entry: {self.entry_point}, tp: {self.take_profit}, sl: {self.stop_loss}"


def get_dataframe(session, symbol, interval, limit) -> pd.DataFrame:
    kline = session.get_kline(symbol=symbol, interval=interval, limit=limit)["result"][
        "list"
    ]
    df = pd.DataFrame(
        data=kline,
        columns=["time", "open", "highest", "lowest", "close", "volume", "turnover"],
        dtype="float64",
    )
    df = df[::-1]
    df.index = pd.to_numeric(df["time"]).div(1000).values.astype(int)
    df.apply(pd.to_numeric)
    df["datetime"] = pd.to_datetime(df["time"].div(1000), unit="s").dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    df.rename(columns={"time": "unix"}, inplace=True)
    df["unix"] = df["unix"].div(1000).values.astype(int)
    # df["time"] = df["time"].astype(int)
    return df


def calculate_swap(prev_h: int, cur_h) -> Swap:
    swap = Swap.STALL
    if prev_h < 0 and cur_h > 0:
        swap = Swap.UP
    if prev_h > 0 and cur_h < 0:
        swap = Swap.DOWN
    return swap


def get_macd_signal(
    df: pd.DataFrame,
    i: int = 0,
    take_profit: float = 10,
    stop_loss: float = 5,
):
    df = deepcopy(df)
    df.ta.macd(close="close", fast=12, slow=26, append=True)
    df.ta.ema(length=200, append=True)
    prev_h, cur_h = df["MACDh_12_26_9"].iloc[i - 2], df["MACDh_12_26_9"].iloc[i - 1]
    cur_MACD, _ = (
        df["MACD_12_26_9"].iloc[i - 1],
        df["MACDs_12_26_9"].iloc[i - 1],
    )
    cur_price = df["close"].iloc[i - 1]
    cur_200ema = df["EMA_200"].iloc[i - 1]
    take_profit_diff = cur_price * take_profit / 100
    stop_loss_diff = cur_price * stop_loss / 100
    # Добавить условие
    # 2. Пересечение линий
    # 3. Цена ниже 200 EMA
    swap = calculate_swap(prev_h, cur_h)

    if swap == Swap.UP and (cur_price > cur_200ema) and cur_MACD < 0:
        return Signal(
            SignalType.BUY,
            df["unix"].iloc[i - 1],
            df["datetime"].iloc[i - 1],
            cur_price,
            cur_price + take_profit_diff,
            cur_price - stop_loss_diff,
        )
    elif swap == Swap.DOWN and (cur_price < cur_200ema) and cur_MACD > 0:
        return Signal(
            SignalType.SELL,
            df["unix"].iloc[i - 1],
            df["datetime"].iloc[i - 1],
            cur_price,
            cur_price + take_profit_diff,
            cur_price - stop_loss_diff,
        )
        # OPEN SHORT
        # if swap == Swap.DOWN and (cur_price < cur_200ema) and cur_MACD > 0:
        #     return Signal(
        #         SignalType.SELL,
        #         df["time"].iloc[i - 1],
        #         cur_price,
        #         cur_price - take_profit_diff,
        #         cur_price + stop_loss_diff,
        #     )
    # elif opened_position:
    #     # CLOSE LONG
    #     if swap == Swap.DOWN:
    #         return Signal(
    #             SignalType.SELL,
    #             df["time"].iloc[i - 1],
    #             cur_price,
    #             cur_price - take_profit_diff,
    #             cur_price + stop_loss_diff,
    #         )
    # CLOSE SHORT
    # if swap == Swap.UP:
    #     return Signal(
    #         SignalType.BUY,
    #         df["time"].iloc[i - 1],
    #         cur_price,
    #         cur_price + take_profit_diff,
    #         cur_price - stop_loss_diff,
    #     )
    return Signal()
