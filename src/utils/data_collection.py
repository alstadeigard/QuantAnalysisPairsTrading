import pandas
import yfinance as yf


def fetch_data(ticker: str, start_date: str, end_date: str) -> pandas.DataFrame:
    """
    Fetches stock data for a given stock ticker symbol between start_date and end_date.

    Inputs(3):
    - ticker (str): The stock ticker symbol.
    - start_date (str): Start date in the format 'YYYY-MM-DD'.
    - end_date (str): End date in the format 'YYYY-MM-DD'.
    Outputs(1):
    - pandas.DataFrame: Dataframe of stock data.
    """

    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data['Adj Close']
