"""Functions used to download and clean stock market data."""

import pandas as pd
import yfinance as yf


def download_stock_data(symbol, period):
    """Download historical stock prices from Yahoo Finance."""
    try:
        data = yf.download(
            symbol,
            period=period,
            auto_adjust=True,
            progress=False
        )
        if data.empty:
            return pd.DataFrame()

        # yfinance can sometimes return multi-level column names.
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        return data.reset_index()
    except Exception:
        return pd.DataFrame()


def clean_stock_data(data):
    """Keep useful columns and remove missing or duplicate rows."""
    if data.empty:
        return pd.DataFrame()

    data = data.copy()
    data.columns = [str(name).lower().replace(" ", "_") for name in data.columns]

    if "date" not in data.columns and "datetime" in data.columns:
        data = data.rename(columns={"datetime": "date"})

    needed_columns = ["date", "open", "high", "low", "close", "volume"]
    data = data[needed_columns]

    data["date"] = pd.to_datetime(data["date"], errors="coerce")

    for column in needed_columns[1:]:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    data = data.dropna()
    data = data.drop_duplicates(subset="date")
    data = data.sort_values("date").reset_index(drop=True)

    return data
