from statsmodels.tsa.stattools import coint

def check_cointegration(stock1, stock2):
    score, pvalue, _ = coint(stock1, stock2)
    if pvalue < 0.05:
        return True, pvalue
    else:
        return False, pvalue
