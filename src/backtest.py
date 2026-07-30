import pandas as pd
import numpy as np


def backtest_strategy(data, top_n=10):
    """
    Simple factor strategy backtest
    
    Every day:
    1. Select top N stocks by Factor_Score
    2. Hold for next trading day
    3. Calculate portfolio return
    """

    data = data.copy()

    # sort by date
    data = data.sort_values(["Date", "Factor_Score"], ascending=[True, False])


    portfolio_returns = []


    dates = data["Date"].unique()


    for i in range(len(dates)-1):

        today = dates[i]
        tomorrow = dates[i+1]


        # today's top stocks
        today_data = data[data["Date"] == today]

        top_stocks = (
            today_data
            .sort_values(
                "Factor_Score",
                ascending=False
            )
            .head(top_n)
        )


        # next day return
        next_day_data = data[
            (data["Date"] == tomorrow)
            &
            (data["Ticker"].isin(top_stocks["Ticker"]))
        ]


        if len(next_day_data) > 0:

            daily_return = (
                next_day_data["Daily_Return"]
                .mean()
            )

            portfolio_returns.append(
                {
                    "Date": tomorrow,
                    "Return": daily_return
                }
            )


    result = pd.DataFrame(portfolio_returns)

    return result