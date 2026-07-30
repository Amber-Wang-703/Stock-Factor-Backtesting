import pandas as pd


def zscore(series):

    std = series.std()

    if std == 0:
        return series * 0

    return (
        series - series.mean()
    ) / std



def calculate_factor_score(data):

    data = data.copy()


    # =====================
    # Momentum
    # =====================

    data["Momentum_12M_Score"] = (
        data
        .groupby("Date")["Momentum_12M"]
        .transform(zscore)
    )


    data["Momentum_6M_Score"] = (
        data
        .groupby("Date")["Momentum_6M"]
        .transform(zscore)
    )


    # Short-term reversal
    # lower recent return = higher score
    data["Reversal_Score"] = (
        data
        .groupby("Date")["Reversal_5D"]
        .transform(
            lambda x: -zscore(x)
        )
    )


    # =====================
    # Risk
    # =====================

    # low volatility is better
    data["Volatility_Score"] = (
        data
        .groupby("Date")["Volatility"]
        .transform(
            lambda x: -zscore(x)
        )
    )


    data["Downside_Vol_Score"] = (
        data
        .groupby("Date")["Downside_Volatility"]
        .transform(
            lambda x: -zscore(x)
        )
    )


    # =====================
    # Trend
    # =====================

    data["MA20_Score"] = (
        data
        .groupby("Date")["MA20_Distance"]
        .transform(zscore)
    )


    data["MA60_Score"] = (
        data
        .groupby("Date")["MA60_Distance"]
        .transform(zscore)
    )


    data["MA200_Score"] = (
        data
        .groupby("Date")["MA200_Distance"]
        .transform(zscore)
    )


    # =====================
    # Liquidity
    # =====================

    data["Liquidity_Score"] = (
        data
        .groupby("Date")["Dollar_Volume"]
        .transform(zscore)
    )


    data["Volume_Change_Score"] = (
        data
        .groupby("Date")["Volume_Change"]
        .transform(zscore)
    )


    # =====================
    # Final Score
    # =====================

    score_columns = [
        "Momentum_12M_Score",
        "Momentum_6M_Score",
        "Reversal_Score",
        "Volatility_Score",
        "Downside_Vol_Score",
        "MA20_Score",
        "MA60_Score",
        "MA200_Score",
        "Liquidity_Score",
        "Volume_Change_Score"
    ]


    data["Factor_Score"] = (
        data[score_columns]
        .mean(axis=1)
    )

    return data