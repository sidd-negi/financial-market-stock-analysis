import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from data_utils import download_stock_data, clean_stock_data
from statistics_analysis import get_summary, compare_returns, compare_three_periods
from correlation_analysis import get_correlation
from prediction import make_prediction

st.set_page_config(page_title="Stock Analysis System", page_icon="📈", layout="wide")

st.title("Financial Market & Stock Analysis System")
st.write("This project studies historical stock prices using basic data analysis and statistics.")
st.caption("For academic learning only. This is not investment advice.")

# Sidebar: user chooses the stock and the time period.
with st.sidebar:
    st.header("Choose stock")
    stock = st.selectbox(
        "Stock symbol",
        ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "ITC.NS", "SBIN.NS", "^NSEI"]
    )
    period = st.selectbox("Data period", ["1y", "2y", "5y"], index=2)
    st.write("Indian shares use .NS. ^NSEI represents NIFTY 50.")

# Download and prepare data.
with st.spinner("Getting stock data..."):
    raw_data = download_stock_data(stock, period)

if raw_data.empty:
    st.error("No data found. Check your internet connection or select another stock.")
    st.stop()

data = clean_stock_data(raw_data)

if len(data) < 30:
    st.warning("There are not enough records for all the analysis.")
    st.stop()

data["daily_return"] = data["close"].pct_change() * 100
data["moving_average"] = data["close"].rolling(window=20).mean()

st.subheader(stock + " - Stock Overview")
latest_price = data["close"].iloc[-1]
first_price = data["close"].iloc[0]
total_return = (latest_price / first_price - 1) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Latest closing price", f"₹{latest_price:,.2f}")
col2.metric("Average closing price", f"₹{data['close'].mean():,.2f}")
col3.metric("Return during selected period", f"{total_return:.2f}%")

price_tab, stats_tab, tests_tab, corr_tab, prediction_tab, data_tab = st.tabs(
    ["Price Chart", "Statistics", "Statistical Tests", "Correlation", "Prediction", "Data"]
)

with price_tab:
    st.subheader("Closing Price")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(data["date"], data["close"], label="Closing price")
    ax.plot(data["date"], data["moving_average"], label="20-day moving average")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (₹)")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    st.pyplot(fig)

with stats_tab:
    st.subheader("Basic Statistical Measures")
    summary = get_summary(data)
    summary_table = pd.DataFrame(
        {"Measure": list(summary.keys()), "Value": list(summary.values())}
    )
    st.dataframe(summary_table, width="stretch", hide_index=True)

    st.subheader("Daily Return Distribution")
    fig, ax = plt.subplots(figsize=(9, 3))
    ax.hist(data["daily_return"].dropna(), bins=30)
    ax.set_xlabel("Daily return (%)")
    ax.set_ylabel("Number of days")
    ax.grid(alpha=0.2)
    fig.tight_layout()
    st.pyplot(fig)

with tests_tab:
    st.subheader("Compare the first and second half of daily returns")
    st.write(
        "A two-sample t-test checks whether the average daily returns in the two periods "
        "are statistically different. The test does not prove that one period caused the other."
    )
    result = compare_returns(data["daily_return"].dropna())
    st.write(f"**T-statistic:** {result['t_statistic']:.4f}")
    st.write(f"**P-value:** {result['p_value']:.4f}")
    if result["p_value"] < 0.05:
        st.info("At the 5% significance level, the two average returns are statistically different.")
    else:
        st.info("At the 5% significance level, there is not enough evidence of a difference.")

    st.subheader("One-way ANOVA: compare three time periods")
    anova_result = compare_three_periods(data["daily_return"].dropna())
    st.write(f"**F-statistic:** {anova_result['f_statistic']:.4f}")
    st.write(f"**P-value:** {anova_result['p_value']:.4f}")
    if anova_result["p_value"] < 0.05:
        st.info("At least one period has a different average return.")
    else:
        st.info("There is not enough evidence that the three average returns differ.")

with corr_tab:
    st.subheader("Correlation between stocks")
    symbols = st.multiselect(
        "Select at least two stocks",
        ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "ITC.NS", "SBIN.NS"],
        default=["RELIANCE.NS", "TCS.NS", "INFY.NS"]
    )
    if len(symbols) < 2:
        st.write("Please select at least two stocks.")
    else:
        with st.spinner("Downloading selected stocks..."):
            corr_data = {}
            for symbol in symbols:
                stock_data = clean_stock_data(download_stock_data(symbol, period))
                if not stock_data.empty:
                    daily = stock_data.set_index("date")["close"].pct_change()
                    corr_data[symbol] = daily
        if len(corr_data) >= 2:
            method = st.selectbox("Correlation method", ["pearson", "spearman", "kendall"])
            correlation = get_correlation(pd.DataFrame(corr_data), method)
            st.write(method.title() + " correlation of daily returns")
            st.dataframe(correlation.round(3), width="stretch")
            st.caption("Values near +1 indicate positive association; values near -1 indicate negative association.")
        else:
            st.warning("Not enough stock data was available.")

with prediction_tab:
    st.subheader("Simple Price Prediction")
    st.write("Linear Regression is used as a basic classroom example to estimate the next closing price.")
    result = make_prediction(data)
    st.metric("Estimated next closing price", f"₹{result['next_price']:,.2f}")
    st.write(f"**Mean Absolute Error (test data):** ₹{result['mae']:,.2f}")
    st.write(f"**R-squared (test data):** {result['r2']:.3f}")
    st.caption("This simple model uses the previous 5 closing prices. It is not suitable for making trading decisions.")

with data_tab:
    st.subheader("Cleaned Stock Data")
    st.dataframe(data.tail(20), width="stretch", hide_index=True)
    csv_data = data.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download data as CSV",
        data=csv_data,
        file_name=stock.replace("^", "") + "_data.csv",
        mime="text/csv"
    )
