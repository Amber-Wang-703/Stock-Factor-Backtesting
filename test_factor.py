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