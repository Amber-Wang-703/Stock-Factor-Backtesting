import pandas as pd


def backtest_strategy(data, top_n=10):

    data = data.copy()


    # sort by date and factor score

    data = data.sort_values(
        [
            "Date",
            "Composite_Factor_Score"
        ],
        ascending=[
            True,
            False
        ]
    )


    dates = (
        data["Date"]
        .drop_duplicates()
        .sort_values()
        .tolist()
    )


    portfolio_returns = []


    for i in range(len(dates)-1):

        today = dates[i]
        tomorrow = dates[i+1]


        # today's universe

        today_data = data[
            data["Date"] == today
        ]


        if len(today_data) < top_n:
            continue


        # select top stocks

        selected = (
            today_data
            .sort_values(
                "Composite_Factor_Score",
                ascending=False
            )
            .head(top_n)
        )


        selected_tickers = (
            selected["Ticker"]
            .tolist()
        )


        # next day returns

        next_day = data[
            (data["Date"] == tomorrow)
            &
            (data["Ticker"].isin(selected_tickers))
        ]


        if len(next_day) < 3:
            continue


        # equal weighted return

        daily_return = (
            next_day["Daily_Return"]
            .mean()
        )


        portfolio_returns.append(
            {
                "Date": tomorrow,
                "Return": daily_return,
                "Num_Stocks": len(next_day)
            }
        )


    result = pd.DataFrame(
        portfolio_returns
    )


    if len(result) == 0:

        print(
            "Warning: No backtest results generated."
        )

        return pd.DataFrame(
            columns=[
                "Date",
                "Return",
                "Num_Stocks"
            ]
        )


    result = result.sort_values(
        "Date"
    )


    return result