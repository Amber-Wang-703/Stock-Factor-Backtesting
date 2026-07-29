from pathlib import Path

import yfinance as yf


def download_stock_data(
    ticker: str,
    start_date: str,
    end_date: str,
) -> None:
    """Download historical stock data and save it as a CSV file."""

    data = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=False,
        progress=False,
    )

    if data.empty:
        raise ValueError(f"No data downloaded for {ticker}")

    project_root = Path(__file__).resolve().parent.parent
    data_folder = project_root / "data"
    data_folder.mkdir(exist_ok=True)

    output_path = data_folder / f"{ticker}.csv"
    data.to_csv(output_path)

    print(data.head())
    print(f"\nSaved {ticker} data to: {output_path}")


if __name__ == "__main__":
    download_stock_data(
        ticker="AAPL",
        start_date="2015-01-01",
        end_date="2025-01-01",
    )