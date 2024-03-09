def perform_feature_engineering(historical_data: pd.DataFrame, sentiment_data: pd.DataFrame) -> pd.DataFrame:
    """
    This function is used to perform feature engineering on the historical data and sentiment data
    :param historical_data: Historical data of the stock
    :param sentiment_data: Sentiment data of the stock
    :return: A dataframe with the features
    """
    # Feature 1: Moving average
    historical_data['moving_average'] = historical_data['close'].rolling(window=20).mean()

    # Feature 2: Moving average convergence divergence (MACD)
    historical_data['26_ema'] = historical_data['close'].ewm(span=26).mean()
    historical_data['12_ema'] = historical_data['close'].ewm(span=12).mean()
    historical_data['macd'] = historical_data['12_ema'] - historical_data['26_ema']

    # Feature 3: Relative strength index (RSI)
    delta = historical_data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    historical_data['rsi'] = 100 - (100 / (1 + rs))

    # Feature 4: Sentiment data
    historical_data = historical_data.merge(sentiment_data, on='date', how='left')

    return historical_data