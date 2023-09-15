from src.utils.data_collection import fetch_data
from src.utils.data_processing import preprocess_data
from src.utils.data_analysis import check_cointegration
from src.utils.trading_strategy_utils import compute_spread, compute_z_score, generate_trading_signals, \
    compute_strategy_returns, calculate_total_returns
from src.utils.risk_assessment_utils import calculate_sharpe_ratio, calculate_max_drawdown
import numpy as np


def backtest_pairs_trading(stock1_ticker, stock2_ticker, start_date, end_date, z_score_threshold):
    print(f'Running trading with {stock1_ticker}, {stock2_ticker}, {start_date}, {end_date}, {z_score_threshold}')
    # Fetch data
    stock1_data = fetch_data(stock1_ticker, start_date, end_date)
    stock2_data = fetch_data(stock2_ticker, start_date, end_date)


    # Preprocess data
    stock1_returns = preprocess_data(stock1_data)
    stock2_returns = preprocess_data(stock2_data)

    # Check cointegration
    are_cointegrated, p_value = check_cointegration(stock1_data, stock2_data)
    if are_cointegrated:
        print(f"{stock1_ticker} and {stock2_ticker} are cointegrated. P-value: {p_value}")
    else:
        print(f"{stock1_ticker} and {stock2_ticker} are not cointegrated. P-value: {p_value}")

    # Compute spread and Z-score
    spread = compute_spread(stock1_data, stock2_data)
    z_score = compute_z_score(spread)

    # Generate trading signals
    signals = generate_trading_signals(z_score, z_score_threshold)

    # Compute strategy returns
    cumulative_strategy_returns = compute_strategy_returns(stock1_returns, stock2_returns, signals)

    daily_returns = cumulative_strategy_returns.pct_change().dropna()

    max_drawdown = calculate_max_drawdown(cumulative_strategy_returns)
    sharpe_ratio = calculate_sharpe_ratio(daily_returns)
    total_returns = calculate_total_returns(cumulative_strategy_returns)

    return stock1_data, stock2_data, are_cointegrated, p_value, cumulative_strategy_returns, max_drawdown, sharpe_ratio, total_returns
