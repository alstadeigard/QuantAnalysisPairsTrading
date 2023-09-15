import numpy as np

def calculate_max_drawdown(cumulative_returns):
    rolling_max = cumulative_returns.cummax()
    daily_drawdown = cumulative_returns/rolling_max - 1.0
    return daily_drawdown.cummin().iloc[-1]

def calculate_sharpe_ratio(daily_returns):
    """Assuming a risk-free rate of 0"""
    return daily_returns.mean() / daily_returns.std() * np.sqrt(252)  # Annualized
