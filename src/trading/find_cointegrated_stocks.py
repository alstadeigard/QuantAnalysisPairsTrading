from src.utils.data_collection import fetch_data
from src.utils.data_analysis import check_cointegration

# Group stock tickers by industry
industry_groups = {
    'Mining Australia': ['BHP.AX', 'RIO.AX'],
    'Tech US': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'AMD', 'CRM', 'ORCL', 'SAP', 'ADBE'],
    'Banking UK': ['HSBC', 'BARC.L'],
    'Automobile Germany': ['VOW3.DE', 'BMW.DE'],
}

time_frames = [
    ("2010-01-01", "2015-01-01"),
    ("2015-01-01", "2020-01-01")
]


def analyze_pair(stock1, stock2, start_date, end_date):
    try:
        data1 = fetch_data(stock1, start_date, end_date)
        data2 = fetch_data(stock2, start_date, end_date)

        if data1 is None or data2 is None:
            print(f"Data fetching failed for {stock1} or {stock2} between {start_date} and {end_date}.")
            return

        are_cointegrated, p_value = check_cointegration(data1, data2)
        if are_cointegrated:
            print(f"{stock1} and {stock2} are cointegrated between {start_date} and {end_date}. P-value: {p_value}")
        else:
            pass
            print(f"{stock1} and {stock2} are not cointegrated between {start_date} and {end_date}. P-value: {p_value}")

    except Exception as e:
        pass
        print(f"Error analyzing {stock1} and {stock2} between {start_date} and {end_date}. Error: {str(e)}")


# Systematically analyze stock pairs within each industry group for each time frame
for group, stocks in industry_groups.items():
    for i in range(len(stocks)):
        for j in range(i + 1, len(stocks)):
            for start_date, end_date in time_frames:
                analyze_pair(stocks[i], stocks[j], start_date, end_date)
