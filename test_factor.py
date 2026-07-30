from src.data_loader import load_stock_data
from src.factors import calculate_factors
from src.scoring import calculate_factor_score
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
print(data.shape)


# ==========================
# 2. Calculate Factors
# ==========================

print("\nCalculating factors...")

data = calculate_factors(data)

print("\nFactor Columns:")
print(data.columns)


# ==========================
# 3. Calculate Factor Score
# ==========================

print("\nCalculating factor score...")

data = calculate_factor_score(data)


print("\nAfter Scoring:")
print(
    data[
        [
            "Date",
            "Ticker",
            "Factor_Score"
        ]
    ].head()
)


# ==========================
# 4. Clean Data
# ==========================

print("\nCleaning data...")


factor_columns = [
    "Factor_Score"
]


data = data.dropna(
    subset=factor_columns
)


print("Clean Data Shape:")
print(data.shape)


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
# 5. Ranking
# ==========================

print("\nRanking stocks...")


ranked_data = rank_stocks(
    data,
    top_n=10
)


print("\nTop Stocks:")

print(
    ranked_data[
        [
            "Date",
            "Ticker",
            "Factor_Score"
        ]
    ].head(30)
)



# ==========================
# 6. Backtest
# ==========================

print("\nRunning Backtest...")


returns = backtest_strategy(
    data,
    top_n=10
)


print("\nBacktest Result:")

print(
    returns.head()
)


print(
    "Backtest Shape:",
    returns.shape
)



# ==========================
# 7. Performance
# ==========================

if len(returns) > 0:

    print("\nPerformance:")

    performance = calculate_performance(
        returns
    )

    print(performance)


else:

    print(
        "\nNo backtest results generated."
    )
