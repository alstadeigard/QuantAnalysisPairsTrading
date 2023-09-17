import pandas as pd
import statsmodels.api as sm


def compute_spread(stock1_data: pd.DataFrame, stock2_data: pd.DataFrame) -> pd.Series:
    """
    Computes the spread between two stocks based on a linear regression.

    Inputs(2):
    - stock1_data (pd.DataFrame): Dataframe with 'Adj Close' column for stock 1.
    - stock2_data (pd.DataFrame): Dataframe with 'Adj Close' column for stock 2.
    Outputs(1):
    - pd.Series: The spread between the two stocks.
    """

    stock1_data = sm.add_constant(stock1_data)
    model = sm.OLS(stock2_data, stock1_data).fit()
    spread = stock2_data['Adj Close'] - (model.params[1] * stock1_data['Adj Close'] + model.params[0])
    return spread


def compute_z_score(spread: pd.Series) -> pd.Series:
    """
    Computes the Z-score for the given spread.

    Inputs(1):
    - spread (pd.Series): Spread values.
    Outputs(1):
    - pd.Series: The Z-score for the spread.
    """

    return (spread - spread.mean()) / spread.std()


def generate_trading_signals(z_score: pd.Series, threshold: float) -> dict:
    """
    Generates trading signals based on z-score and given threshold.

    Inputs(2):
    - z_score (pd.Series): The Z-score values.
    - threshold (float): Threshold for generating signals.
    Outputs(1):
    - dict: Dictionary containing boolean values for 'long_entry', 'short_entry', 'long_exit', and 'short_exit'.
    """

    signals = {}
    signals['long_entry'] = z_score < -threshold
    signals['short_entry'] = z_score > threshold
    signals['long_exit'] = z_score >= -0.5
    signals['short_exit'] = z_score <= 0.5
    return signals


def compute_strategy_returns(stock1_returns: pd.DataFrame, stock2_returns: pd.DataFrame, signals: dict) -> pd.Series:
    """
    Computes the cumulative strategy returns based on provided signals and returns.

    Inputs(3):
    - stock1_returns (pd.DataFrame): DataFrame containing daily returns for stock 1.
    - stock2_returns (pd.DataFrame): DataFrame containing daily returns for stock 2.
    - signals (dict): Dictionary containing trading signals.
    Outputs(1):
    - pd.Series: Cumulative strategy returns.
    """

    # Use the 'Adj Close' column for calculations (or another appropriate column name if it's different)
    returns = stock1_returns['Adj Close'] - stock2_returns['Adj Close']

    # Assuming signals are still Series and not part of a DataFrame
    strategy = returns * signals['long_entry'].shift().fillna(0) - returns * signals['short_entry'].shift().fillna(0)

    cumulative_strategy_returns = (1 + strategy).cumprod()
    return cumulative_strategy_returns


def calculate_total_returns(cumulative_returns: pd.Series) -> float:
    """
    Calculate total returns based on the cumulative returns.

    Inputs(1):
    - cumulative_returns (pd.Series): Cumulative strategy returns.
    Outputs(1):
    - float: Total returns as a proportion.
    """

    return cumulative_returns.iloc[-1] - 1
