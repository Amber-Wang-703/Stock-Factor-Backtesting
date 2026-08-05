import pandas as pd
import numpy as np



def calculate_performance(returns):

    result = returns.copy()


    # =========================
    # Cumulative Return
    # =========================

    result["Cumulative_Return"] = (
        1 + result["Return"]
    ).cumprod()



    # =========================
    # Total Return
    # =========================

    total_return = (
        result["Cumulative_Return"]
        .iloc[-1]
        - 1
    )



    # =========================
    # Annual Return
    # =========================

    total_days = len(result)


    annual_return = (
        result["Cumulative_Return"]
        .iloc[-1]
        **
        (252 / total_days)
        - 1
    )



    # =========================
    # Annual Volatility
    # =========================

    annual_volatility = (
        result["Return"]
        .std()
        *
        np.sqrt(252)
    )



    # =========================
    # Sharpe Ratio
    # =========================

    risk_free_rate = 0


    sharpe = (

        (
            result["Return"]
            .mean()
            -
            risk_free_rate / 252
        )

        /

        result["Return"]
        .std()

        *

        np.sqrt(252)

    )



    # =========================
    # Maximum Drawdown
    # =========================


    cumulative = (
        result["Cumulative_Return"]
    )


    peak = (
        cumulative
        .cummax()
    )


    drawdown = (
        cumulative - peak
    ) / peak


    max_drawdown = (
        drawdown.min()
    )



    return {

        "Total Return": total_return,

        "Annual Return": annual_return,

        "Annual Volatility": annual_volatility,

        "Sharpe Ratio": sharpe,

        "Max Drawdown": max_drawdown

    }