from src.utils.data_collection import fetch_data
from src.utils.data_processing import preprocess_data
from src.utils.data_visualization import plot_data
from src.utils.data_analysis import check_cointegration

# Fetch data
start_date = "2015-01-01"
end_date = "2020-01-01"
orcl_data = fetch_data('ORCL', start_date, end_date)
sap_data = fetch_data('SAP', start_date, end_date)

# Preprocess data
orcl_returns = preprocess_data(orcl_data)
sap_returns = preprocess_data(sap_data)

# Visualize stock prices and returns
plot_data(orcl_data, "Oracle Adjusted Close Prices", "Price ($)")
plot_data(sap_data, "SAP Adjusted Close Prices", "Price ($)")
plot_data(orcl_returns, "Oracle Daily Returns", "Return")
plot_data(sap_returns, "Sap Daily Returns", "Return")

# Check cointegration
are_cointegrated, p_value = check_cointegration(orcl_data, sap_data)
if are_cointegrated:
    print(f"ORCL and SAP are cointegrated. P-value: {p_value}")
else:
    print(f"ORCL and SAP are not cointegrated. P-value: {p_value}")

