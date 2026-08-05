import pandas as pd


def rank_stocks(data, top_n=20):
    """
    Rank stocks by Composite Factor Score every day.

    Parameters:
    data:
        dataframe containing:
        Date
        Ticker
        Composite_Factor_Score

    top_n:
        number of stocks selected each day

    Returns:
        dataframe containing top ranked stocks
    """


    ranked_data = (
        data
        .sort_values(
            [
                "Date",
                "Composite_Factor_Score"
            ],
            ascending=[
                True,
                False
            ]
        )
        .groupby("Date")
        .head(top_n)
    )


    return ranked_data
