# Financial Market & Stock Analysis System

## About the project

This project uses historical stock market data to understand how stock prices change over time. It is made with Python. The dashboard lets the user select a stock and see its price chart, statistical values, correlation with other stocks and a simple price estimate.

## Main features

- Download historical stock data.
- Clean missing and duplicate records.
- Display closing price and 20-day moving average.
- Calculate mean, median, standard deviation, variance, returns and volatility.
- Use a t-test and one-way ANOVA to compare returns across time periods.
- Calculate Pearson, Spearman and Kendall correlation between selected stocks.
- Use Linear Regression for a basic price estimate.
- View and download the cleaned data.

## Software needed

- Python 3.10 or newer
- VS Code
- Internet connection

## Run on macOS

Open this folder in VS Code. In the terminal, run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
streamlit run app.py
```

The dashboard should open in your browser. If it does not, use the local address shown in the terminal, usually http://localhost:8501.

## Files in this project

- `app.py` - Main Streamlit dashboard.
- `data_utils.py` - Downloads and cleans stock data.
- `statistics_analysis.py` - Calculates statistical values and performs a t-test.
- `correlation_analysis.py` - Calculates correlation between stocks.
- `prediction.py` - Runs a basic Linear Regression model.
- `requirements.txt` - Lists the Python libraries used.

## Data source

Stock prices are downloaded from Yahoo Finance using the `yfinance` library. The data source may change its availability or format.

## Note

This project is for learning data analytics. Stock price estimates are not guaranteed to be correct and should not be used as investment advice.
