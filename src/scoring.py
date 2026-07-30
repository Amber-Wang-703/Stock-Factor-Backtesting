import pandas as pd


def zscore(series):

    return (
        series - series.mean()
    ) / series.std()



def calculate_factor_score(data):

    data = data.copy()


    # Momentum 越高越好
    data["Momentum_Score"] = (
        data
        .groupby("Date")["Momentum"]
        .transform(zscore)
    )


    # MA 趋势 越高越好
    data["MA_Score"] = (
        data
        .groupby("Date")["MA_Factor"]
        .transform(zscore)
    )


    # Volatility 越低越好
    # 所以取负数
    data["Volatility_Score"] = (
        data
        .groupby("Date")["Volatility"]
        .transform(
            lambda x: -zscore(x)
        )
    )


    # Volume 越高越好
    data["Volume_Score"] = (
        data
        .groupby("Date")["Volume_Factor"]
        .transform(zscore)
    )


    # 综合评分
    data["Factor_Score"] = (
        0.4 * data["Momentum_Score"]
        +
        0.3 * data["MA_Score"]
        +
        0.2 * data["Volatility_Score"]
        +
        0.1 * data["Volume_Score"]
    )


    return data