import os
import pandas as pd

from src.data_loader import load_stock_data
from src.factors import calculate_factors
from src.ranking import rank_stocks
from src.backtest import backtest_strategy
from src.performance import calculate_performance



# ==========================
# 1. Load Data
# ==========================

print("Loading data...")


data = load_stock_data()


print("\nRaw Data:")

print(data.head())

print(
    "Shape:",
    data.shape
)



# ==========================
# 2. Calculate Factors
# ==========================

print("\nCalculating factors...")


data = calculate_factors(
    data
)


print("\nFactor Columns:")

print(data.columns)



# ==========================
# 3. Clean Data
# ==========================

print("\nCleaning data...")


data = data.dropna(
    subset=[
        "Composite_Factor_Score"
    ]
)


print(
    "Clean Data Shape:",
    data.shape
)


print(
    "Number of Stocks:",
    data["Ticker"].nunique()
)


print(
    "Date Range:",
    data["Date"].min(),
    "to",
    data["Date"].max()
)



# ==========================
# 4. Ranking
# ==========================

print("\nRanking stocks...")


ranked_data = rank_stocks(
    data,
    top_n=10
)


print(
    "\nTop Stocks:"
)


print(
    ranked_data[
        [
            "Date",
            "Ticker",
            "Composite_Factor_Score"
        ]
    ]
    .head(30)
)



# ==========================
# 5. Backtest
# ==========================

print("\nRunning Backtest...")


returns = backtest_strategy(
    data,
    top_n=10
)


print(
    "\nBacktest Result:"
)


print(
    returns.head()
)


print(
    "Backtest Shape:",
    returns.shape
)



# ==========================
# 6. Performance
# ==========================

if len(returns) > 0:


    print(
        "\nPerformance:"
    )


    performance = calculate_performance(
        returns
    )


    print(
        performance
    )



    # ======================
    # Save Results
    # ======================


    print(
        "\nSaving results..."
    )


    os.makedirs(
        "results",
        exist_ok=True
    )


    # Performance summary

    pd.DataFrame(
        [performance]
    ).to_csv(
        "results/performance_summary.csv",
        index=False
    )


    # Daily strategy returns

    returns.to_csv(
        "results/strategy_returns.csv",
        index=False
    )


    # Selected stocks

    ranked_data.to_csv(
        "results/top_stocks.csv",
        index=False
    )


    print(
        "Results saved successfully."
    )



else:


    print(
        "No backtest results generated."
    )
    