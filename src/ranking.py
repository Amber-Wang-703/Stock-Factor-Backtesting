import pandas as pd


def rank_stocks(data, top_n=20):
    """
    Rank stocks by Factor Score every day
    
    Parameters:
    data: dataframe with Date, Ticker, Factor_Score
    top_n: number of stocks selected each day
    
    Returns:
    dataframe containing top ranked stocks
    """

    ranked_data = (
        data
        .sort_values(
            ["Date", "Factor_Score"],
            ascending=[True, False]
        )
        .groupby("Date")
        .head(top_n)
    )

    return ranked_data