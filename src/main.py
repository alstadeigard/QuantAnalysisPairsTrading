from src.utils.data_collection import fetch_data
from src.utils.data_processing import preprocess_data
from src.utils.data_visualization import plot_data
from src.utils.data_analysis import check_cointegration
from src.utils.trading_strategy_utils import compute_spread, calculate_z_score, generate_signals, \
    compute_strategy_returns, compute_cumulative_returns
from src.utils.risk_assessment_utils import calculate_drawdowns, calculate_sharpe_ratio
import numpy as np


def backtest_pairs_trading(stock1_ticker, stock2_ticker, start_date, end_date, lower_threshold, upper_threshold):
    # Fetch data
    stock1_data = fetch_data(stock1_ticker, start_date, end_date)
    stock2_data = fetch_data(stock2_ticker, start_date, end_date)

    # Preprocess data
    stock1_returns = preprocess_data(stock1_data)
    stock2_returns = preprocess_data(stock2_data)

    # Visualize stock prices and returns
    #plot_data(stock1_data, f"{stock1_ticker} Adjusted Close Prices", "Price ($)")
    #plot_data(stock2_data, f"{stock2_ticker} Adjusted Close Prices", "Price ($)")
    #plot_data(stock1_returns, f"{stock1_ticker} Daily Returns", "Return")
    #plot_data(stock2_returns, f"{stock2_ticker} Daily Returns", "Return")

    # Check cointegration
    are_cointegrated, p_value = check_cointegration(stock1_data, stock2_data)
    if are_cointegrated:
        print(f"{stock1_ticker} and {stock2_ticker} are cointegrated. P-value: {p_value}")
    else:
        print(f"{stock1_ticker} and {stock2_ticker} are not cointegrated. P-value: {p_value}")

    # Spread analysis
    spread = compute_spread(stock1_data, stock2_data)

    # Signal generation
    z_scores = calculate_z_score(spread)
    signals = generate_signals(z_scores, lower_threshold, upper_threshold)

    # Calculate strategy returns
    daily_strategy_returns = compute_strategy_returns(stock1_returns, stock2_returns, signals)
    cumulative_strategy_returns = compute_cumulative_returns(daily_strategy_returns)

    drawdowns = calculate_drawdowns(daily_strategy_returns)
    max_drawdown = drawdowns.min()

    sharpe_ratio = calculate_sharpe_ratio(daily_strategy_returns)

    print(f"Cumulative Strategy Returns: {cumulative_strategy_returns}")
    print(f"Maximum Drawdown: {max_drawdown:.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")

    return cumulative_strategy_returns, max_drawdown, sharpe_ratio


# ... [previous code]

def optimize_z_scores(stock1_ticker, stock2_ticker, start_date, end_date, z_score_range):
    best_sharpe = float('-inf')
    best_z = None
    best_max_drawdown = None
    best_cumulative_return = None

    for z in z_score_range:
        print(f"\nTesting with Z-score threshold: {z}")
        cumulative_returns, max_dd, sharpe = backtest_pairs_trading(stock1_ticker, stock2_ticker, start_date, end_date,
                                                                    -z, z)

        if sharpe > best_sharpe:
            best_sharpe = sharpe
            best_z = z
            best_max_drawdown = max_dd
            best_cumulative_return = cumulative_returns

    print(f"\nBest Z-score threshold for {stock1_ticker} and {stock2_ticker}: {best_z}")
    print(f"Corresponding Sharpe Ratio: {best_sharpe:.2f}")
    print(f"Corresponding Maximum Drawdown: {best_max_drawdown:.2%}")
    print(f"Corresponding Cumulative Return: {best_cumulative_return}")

    return best_z, best_sharpe, best_max_drawdown, best_cumulative_return


# Optimize Z-scores for stock pairs
start_date = "2015-01-01"
end_date = "2020-01-01"
z_score_range = np.arange(0.5, 3.1, 0.5)  # testing z-scores from 0.5 to 3 in increments of 0.5

print("Optimizing for PEP and KO:")
optimize_z_scores('PEP', 'KO', start_date, end_date, z_score_range)

print("\nOptimizing for ORCL and SAP:")
optimize_z_scores('ORCL', 'SAP', start_date, end_date, z_score_range)
