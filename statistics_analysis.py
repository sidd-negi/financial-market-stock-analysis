"""Basic statistical calculations, t-test and one-way ANOVA."""

import numpy as np
from scipy.stats import ttest_ind, f_oneway


def get_summary(data):
    """Calculate common statistics for closing prices and daily returns."""
    close = data["close"]
    returns = data["daily_return"].dropna()

    return {
        "Mean closing price": round(close.mean(), 2),
        "Median closing price": round(close.median(), 2),
        "Standard deviation of closing price": round(close.std(), 2),
        "Variance of closing price": round(close.var(), 2),
        "Average daily return (%)": round(returns.mean(), 4),
        "Daily return volatility (%)": round(returns.std(), 4),
        "Total return (%)": round((close.iloc[-1] / close.iloc[0] - 1) * 100, 2),
        "Average trading volume": round(data["volume"].mean(), 0)
    }


def compare_returns(returns):
    """Compare the first and second half of returns using an independent t-test."""
    values = np.asarray(returns.dropna())
    middle = len(values) // 2
    statistic, p_value = ttest_ind(values[:middle], values[middle:], equal_var=False)
    return {"t_statistic": float(statistic), "p_value": float(p_value)}


def compare_three_periods(returns):
    """Compare average returns in three time periods using one-way ANOVA."""
    values = np.asarray(returns.dropna())
    groups = np.array_split(values, 3)
    statistic, p_value = f_oneway(*groups)
    return {"f_statistic": float(statistic), "p_value": float(p_value)}
