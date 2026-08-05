import pandas as pd
import numpy as np


# =====================================================
# Daily Returns
# =====================================================

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



# =====================================================
# Momentum Factors
# =====================================================

def calculate_momentum(data):

    data = data.copy()

    close = (
        data
        .groupby("Ticker")["Close"]
    )


    # 12-1 Momentum
    data["Momentum_12M"] = (
        close.shift(21)
        /
        close.shift(252)
        - 1
    )


    # 6-1 Momentum
    data["Momentum_6M"] = (
        close.shift(21)
        /
        close.shift(126)
        - 1
    )


    # Short-term reversal
    data["Reversal_5D"] = (
        close
        .pct_change(5)
    )


    return data



# =====================================================
# Risk Factors
# =====================================================

def calculate_risk(data):

    data = data.copy()


    returns = (
        data
        .groupby("Ticker")["Daily_Return"]
    )


    # Total volatility

    data["Volatility"] = (
        returns
        .transform(
            lambda x:
            x.rolling(60)
            .std()
        )
    )


    # Downside volatility

    data["Downside_Volatility"] = (
        returns
        .transform(
            lambda x:
            x.where(x < 0)
             .rolling(60)
             .std()
        )
    )


    # Fix missing downside volatility

    data["Downside_Volatility"] = (
        data["Downside_Volatility"]
        .fillna(
            data["Volatility"]
        )
    )


    return data



# =====================================================
# Trend Factors
# =====================================================

def calculate_trend(data):

    data = data.copy()


    close = (
        data
        .groupby("Ticker")["Close"]
    )


    for window in [20,60,200]:

        ma = (
            close
            .transform(
                lambda x:
                x.rolling(window)
                .mean()
            )
        )


        data[f"MA{window}_Distance"] = (
            data["Close"]
            /
            ma
            - 1
        )


    return data



# =====================================================
# Liquidity Factors
# =====================================================

def calculate_liquidity(data):

    data = data.copy()


    data["Dollar_Volume"] = (
        data["Close"]
        *
        data["Volume"]
    )


    avg_volume = (
        data
        .groupby("Ticker")["Volume"]
        .transform(
            lambda x:
            x.rolling(20)
            .mean()
        )
    )


    data["Volume_Change"] = (
        data["Volume"]
        /
        avg_volume
        - 1
    )


    return data



# =====================================================
# Z-score
# =====================================================

def zscore(series):

    std = series.std()


    if std == 0 or np.isnan(std):

        return series * 0


    return (
        series - series.mean()
    ) / std



# =====================================================
# Factor Scoring
# =====================================================

def calculate_factor_scores(data):

    data = data.copy()


    # -------------------------
    # Momentum
    # -------------------------

    data["Momentum_Raw"] = (

        0.5 *
        data["Momentum_12M"]

        +

        0.5 *
        data["Momentum_6M"]

    )


    data["Momentum_Score"] = (
        data
        .groupby("Date")
        ["Momentum_Raw"]
        .transform(zscore)
    )


    # -------------------------
    # Risk
    # -------------------------

    data["Risk_Raw"] = (

        -0.7 *
        data["Volatility"]

        -

        0.3 *
        data["Downside_Volatility"]

    )


    data["Risk_Score"] = (
        data
        .groupby("Date")
        ["Risk_Raw"]
        .transform(zscore)
    )



    # -------------------------
    # Trend
    # -------------------------

    data["Trend_Raw"] = (

        0.3 *
        data["MA20_Distance"]

        +

        0.3 *
        data["MA60_Distance"]

        +

        0.4 *
        data["MA200_Distance"]

    )


    data["Trend_Score"] = (
        data
        .groupby("Date")
        ["Trend_Raw"]
        .transform(zscore)
    )



    # -------------------------
    # Liquidity
    # -------------------------

    data["Liquidity_Score"] = (
        data
        .groupby("Date")
        ["Dollar_Volume"]
        .transform(zscore)
    )



    # -------------------------
    # Composite Score
    # -------------------------

    score_columns = [
        "Momentum_Score",
        "Trend_Score",
        "Risk_Score",
        "Liquidity_Score"
    ]


    data["Composite_Factor_Score"] = (
        data[score_columns]
        .mean(axis=1)
    )


    return data



# =====================================================
# Main Pipeline
# =====================================================

def calculate_factors(data):


    data = calculate_returns(data)

    data = calculate_momentum(data)

    data = calculate_risk(data)

    data = calculate_trend(data)

    data = calculate_liquidity(data)

    data = calculate_factor_scores(data)


    return data