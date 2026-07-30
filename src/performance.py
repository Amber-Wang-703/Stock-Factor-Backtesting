import pandas as pd
import numpy as np


def calculate_performance(returns):

    result = returns.copy()

    # cumulative return
    result["Cumulative_Return"] = (
        1 + result["Return"]
    ).cumprod()


    # annual return
    total_days = len(result)

    annual_return = (
        result["Cumulative_Return"].iloc[-1]
        **
        (252 / total_days)
        - 1
    )


    # Sharpe Ratio

    sharpe = (
        result["Return"].mean()
        /
        result["Return"].std()
        *
        np.sqrt(252)
    )


    # Maximum Drawdown

    cumulative = result["Cumulative_Return"]

    peak = cumulative.cummax()

    drawdown = (
        cumulative - peak
    ) / peak


    max_drawdown = drawdown.min()


    return {
        "Annual Return": annual_return,
        "Sharpe Ratio": sharpe,
        "Max Drawdown": max_drawdown
    }