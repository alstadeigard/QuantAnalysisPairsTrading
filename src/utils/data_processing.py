def preprocess_data(data):
    data.fillna(method='ffill', inplace=True)  # Fill missing data
    return data.pct_change().dropna()  # Compute daily returns and drop the first NaN value
