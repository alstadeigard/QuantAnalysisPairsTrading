import statsmodels.api as sm
import numpy as np
import pandas as pd


def compute_spread(stock1_prices, stock2_prices):
    """
    Compute the spread using the Engle-Granger two-step method.
    Returns the spread, which are the residuals of the regression.
    """

    X = sm.add_constant(stock2_prices)
    model = sm.OLS(stock1_prices, X).fit()
    spread = stock1_prices - model.predict(X)

    return spread


def calculate_z_score(spread):
    """
    Calculate the Z-Score of the spread.
    """
    mean_spread = spread.mean()
    std_spread = spread.std()
    z_score = (spread - mean_spread) / std_spread

    return z_score


def generate_signals(z_score, lower_threshold=-1.5, upper_threshold=1.5):
    """
    Generate trading signals based on Z-Score.
    Returns a DataFrame with columns: 'longs', 'shorts', 'exits'
    """

    longs = z_score < lower_threshold
    shorts = z_score > upper_threshold
    exits = np.abs(z_score) < 0.5

    signals = {
        'longs': longs,
        'shorts': shorts,
        'exits': exits
    }

    return pd.DataFrame(signals)


def calculate_daily_returns(stock_data):
    """
    Calculate the daily returns of a stock.
    """
    return stock_data.pct_change().dropna()


def compute_strategy_returns(stock1_returns, stock2_returns, signals):
    """
    Compute the daily strategy returns.
    """
    strategy_returns = signals['longs'].shift() * (stock2_returns - stock1_returns) - signals['shorts'].shift() * (
            stock2_returns - stock1_returns)

    return strategy_returns


def compute_cumulative_returns(strategy_returns):
    """
    Compute the cumulative returns of the strategy.
    """
    cumulative_strategy_returns = (1 + strategy_returns).cumprod()

    return cumulative_strategy_returns
