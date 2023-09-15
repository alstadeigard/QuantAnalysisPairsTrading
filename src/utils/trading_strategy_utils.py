import statsmodels.api as sm
import numpy as np
import pandas as pd


def compute_spread(stock1_data, stock2_data):
    stock1_data = sm.add_constant(stock1_data)
    model = sm.OLS(stock2_data, stock1_data).fit()
    spread = stock2_data['Adj Close'] - (model.params[1] * stock1_data['Adj Close'] + model.params[0])
    return spread


def compute_z_score(spread):
    return (spread - spread.mean()) / spread.std()


def generate_trading_signals(z_score, threshold):
    signals = {}
    signals['long_entry'] = z_score < -threshold
    signals['short_entry'] = z_score > threshold
    signals['long_exit'] = z_score >= -0.5
    signals['short_exit'] = z_score <= 0.5
    return signals


def calculate_daily_returns(stock_data):
    """
    Calculate the daily returns of a stock.
    """
    return stock_data.pct_change().dropna()


def compute_strategy_returns(stock1_returns, stock2_returns, signals):
    returns = stock1_returns['Adj Close'] - stock2_returns['Adj Close']
    strategy = returns * signals['long_entry'].shift().fillna(0) - returns * signals['short_entry'].shift().fillna(0)
    cumulative_strategy_returns = (1 + strategy).cumprod()
    return cumulative_strategy_returns

def calculate_total_returns(cumulative_returns):
    return cumulative_returns.iloc[-1] - 1