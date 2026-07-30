import pandas as pd
import numpy as np


def calculate_returns(data):

    data = data.copy()

    data = data.sort_values(
        ["Ticker", "Date"]
    )

    data["Daily_Return"] = (
        data
        .groupby("Ticker")["Close"]
        .pct_change()
    )

    return data



def calculate_momentum(data):

    data = data.copy()

    close = (
        data
        .groupby("Ticker")["Close"]
    )

    # 12 month momentum
    data["Momentum_12M"] = (
        close
        .pct_change(252)
    )

    # 6 month momentum
    data["Momentum_6M"] = (
        close
        .pct_change(126)
    )

    # short term reversal
    data["Reversal_5D"] = (
        close
        .pct_change(5)
    )

    return data



def calculate_risk(data):

    data = data.copy()


    returns = (
        data
        .groupby("Ticker")["Daily_Return"]
    )


    # 60 day volatility
    data["Volatility"] = (
        returns
        .transform(
            lambda x:
            x.rolling(60).std()
        )
    )


    # downside volatility
    data["Downside_Volatility"] = (
        returns
        .transform(
            lambda x:
            x.where(x < 0)
             .rolling(60)
             .std()
        )
    )


    return data



def calculate_trend(data):

    data = data.copy()


    close = (
        data
        .groupby("Ticker")["Close"]
    )


    for window in [20, 60, 200]:

        ma = (
            close
            .transform(
                lambda x:
                x.rolling(window).mean()
            )
        )


        data[f"MA{window}_Distance"] = (
            data["Close"] / ma - 1
        )


    return data



def calculate_liquidity(data):

    data = data.copy()


    # dollar volume
    data["Dollar_Volume"] = (
        data["Close"] *
        data["Volume"]
    )


    avg_volume = (
        data
        .groupby("Ticker")["Volume"]
        .transform(
            lambda x:
            x.rolling(20).mean()
        )
    )


    data["Volume_Change"] = (
        data["Volume"] /
        avg_volume - 1
    )


    return data



def calculate_factors(data):

    data = calculate_returns(data)

    data = calculate_momentum(data)

    data = calculate_risk(data)

    data = calculate_trend(data)

    data = calculate_liquidity(data)


    return data
