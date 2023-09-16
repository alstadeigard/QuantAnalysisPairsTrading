import numpy as np
import pandas as pd


def calculate_max_drawdown(cumulative_returns: pd.Series) -> float:
    """
    Calculates the maximum drawdown of a strategy based on its cumulative returns.

    Inputs(1):
    - cumulative_returns (pd.Series): A pandas Series of cumulative returns.
    Outputs(1):
    - float: The maximum drawdown of the strategy.
    """

    rolling_max = cumulative_returns.cummax()
    daily_drawdown = cumulative_returns / rolling_max - 1.0
    return daily_drawdown.cummin().iloc[-1]


def calculate_sharpe_ratio(daily_returns: pd.Series) -> float:
    """
    Calculates the annualized Sharpe ratio of a strategy based on its daily returns.
    Assumes a risk-free rate of 0.

    Inputs(1):
    - daily_returns (pd.Series): A pandas Series of daily returns.
    Outputs(1):
    - float: The annualized Sharpe ratio of the strategy.
    """

    return daily_returns.mean() / daily_returns.std() * np.sqrt(252)

