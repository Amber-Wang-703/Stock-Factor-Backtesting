from src.performance import calculate_performance
from src.backtest import backtest_strategy
from src.ranking import rank_stocks
from src.data_loader import load_stock_data
from src.factors import calculate_factors
from src.scoring import calculate_factor_score


data = load_stock_data()

data = calculate_factors(data)


# remove NaN
data = data.dropna()


data = calculate_factor_score(data)


print(data.head())


print(
    data[
        [
            "Ticker",
            "Factor_Score"
        ]
    ].head()
)

ranked_data = rank_stocks(data, top_n=10)

print("\nTop Stocks:")
print(
    ranked_data[
        [
            "Date",
            "Ticker",
            "Factor_Score"
        ]
    ].head(50)
)
returns = backtest_strategy(data, top_n=10)

print("\nBacktest Result:")
print(returns.head())

print(returns["Return"].describe())

performance = calculate_performance(returns)

print("\nPerformance:")
print(performance)