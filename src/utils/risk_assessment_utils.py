import numpy as np

def calculate_drawdowns(returns):
    cum_rets = (1 + returns).cumprod()
    running_max = cum_rets.cummax()
    drawdowns = (cum_rets - running_max) / running_max
    return drawdowns

def calculate_sharpe_ratio(returns, risk_free_rate=0.03):
    excess_returns = returns - risk_free_rate/252  # Assuming daily data and yearly risk-free rate
    return np.sqrt(252) * excess_returns.mean() / excess_returns.std()
