from statsmodels.tsa.stattools import coint
from pandas import Series, DataFrame
from typing import Tuple, Union


def check_cointegration(stock1: Union[Series, DataFrame], stock2: Union[Series, DataFrame]) -> Tuple[bool, float]:
    """
    Checks if the two stock time series are cointegrated.

    Inputs(2):
    - stock1 (Union[Series, DataFrame]): Time series data of the first stock.
    - stock2 (Union[Series, DataFrame]): Time series data of the second stock.
    Outputs(2):
    - bool: True if the stocks are cointegrated, otherwise False.
    - float: p-value of the cointegration test.
    Note:
    The stocks are considered cointegrated if the p-value is less than 0.05.
    """

    score, pvalue, _ = coint(stock1, stock2)
    if pvalue < 0.05:
        return True, pvalue
    else:
        return False, pvalue

