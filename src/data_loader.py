import pandas as pd
import os
import glob


DATA_PATH = "data/raw/SP500_Data_10Y"


def load_stock_data():

    all_files = glob.glob(
        os.path.join(DATA_PATH, "*.csv")
    )

    stock_list = []

    for file in all_files:

        ticker = os.path.basename(file).replace(".csv", "")

        try:
            df = pd.read_csv(file, header=[0,1])

            # flatten multi-index columns
            df.columns = [
                col[0] if col[0] != "Price" else col[1]
                for col in df.columns
            ]

            # reset first column name
            df = df.rename(columns={
                df.columns[0]: "Date"
            })

            df["Ticker"] = ticker


            # remove wrong rows
            df = df[df["Date"] != "Date"]


            # convert date
            df["Date"] = pd.to_datetime(
                df["Date"],
                errors="coerce"
            )


            # convert numbers
            cols = [
                "Close",
                "High",
                "Low",
                "Open",
                "Volume"
            ]

            for c in cols:
                df[c] = pd.to_numeric(
                    df[c],
                    errors="coerce"
                )


            df = df.dropna()


            stock_list.append(df)


            print("Loaded", ticker)


        except Exception as e:
            print(
                "Error:",
                ticker,
                e
            )


    data = pd.concat(
        stock_list,
        ignore_index=True
    )


    data = data.sort_values(
        ["Ticker","Date"]
    )


    return data



if __name__ == "__main__":

    data = load_stock_data()

    print("\nFinished!")
    print(data.head())
    print(data.columns)
    print(data.shape)