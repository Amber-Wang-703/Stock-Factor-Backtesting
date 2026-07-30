import pandas as pd
import numpy as np


# ===============================
# 1. Daily Return
# ===============================
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



# ===============================
# 2. Momentum Factor
# ===============================
def calculate_momentum(data, window=60):

    data = data.copy()

    data["Momentum"] = (
        data
        .groupby("Ticker")["Close"]
        .transform(
            lambda x: x.pct_change(window)
        )
    )

    return data



# ===============================
# 3. Volatility Factor
# ===============================
def calculate_volatility(data, window=60):

    data = data.copy()

    data["Volatility"] = (
        data
        .groupby("Ticker")["Daily_Return"]
        .transform(
            lambda x: x.rolling(window).std()
        )
    )

    return data



# ===============================
# 4. Moving Average Trend Factor
# ===============================
def calculate_ma_factor(data, window=60):

    data = data.copy()

    ma = (
        data
        .groupby("Ticker")["Close"]
        .transform(
            lambda x: x.rolling(window).mean()
        )
    )

    data["MA_Factor"] = (
        data["Close"] / ma - 1
    )

    return data



# ===============================
# 5. Volume Factor
# ===============================
def calculate_volume_factor(data, window=60):

    data = data.copy()

    avg_volume = (
        data
        .groupby("Ticker")["Volume"]
        .transform(
            lambda x: x.rolling(window).mean()
        )
    )

    data["Volume_Factor"] = (
        data["Volume"] / avg_volume
    )

    return data



# ===============================
# Combine All Factors
# ===============================
def calculate_factors(data):

    data = calculate_returns(data)

    data = calculate_momentum(data)

    data = calculate_volatility(data)

    data = calculate_ma_factor(data)

    data = calculate_volume_factor(data)


    return data