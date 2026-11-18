"""Correlation calculations for stock daily returns."""


def get_correlation(price_returns, method="pearson"):
    """Calculate Pearson, Spearman or Kendall correlation."""
    return price_returns.corr(method=method)
