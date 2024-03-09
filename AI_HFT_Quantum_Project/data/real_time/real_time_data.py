#Get real time trading data from market via api
import requests
import json
import pandas as pd

def get_real_time_data():
    #Get real time crypto trading data from binance
    url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.get(url)
    data = response.json()
    #convert json to dataframe
    df = pd.DataFrame(data)
    return df

#function to get last 3 days low , high , open and close price of crypto based on symbol
def get_historical_data(symbol):
    #Get historical data of crypto trading from binance
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1d&limit=4"
    response = requests.get(url)
    data = response.json()
    #convert json to dataframe
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df.drop(columns=['timestamp', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'], inplace=True)
    df.to_csv("AI_HFT_Quantum_Project/data/real-time/historical-data.csv", index=False)
    return df

#function to compare the real time data with the historical data based on threshold
def compare_data_with_historical_data(historical_data, real_time_data, threshold):
    """
    Compare real-time data with historical data based on a specified threshold.
    
    Parameters:
    historical_data (pd.DataFrame): A DataFrame containing historical data with columns ['symbol', 'price'].
    real_time_data (pd.DataFrame): A DataFrame containing real-time data with columns ['symbol', 'price'].
    threshold (float): The threshold value for determining significant change.
    
    Returns:
    list of tuples: Each tuple contains (symbol, real_time_price, historical_price)
                    for symbols that have a change greater than the threshold.
    """
    # Ensure data is in float format
    historical_data['price'] = historical_data['price'].astype(float)
    real_time_data['price'] = real_time_data['price'].astype(float)

    # Merge dataframes on 'symbol' to align historical and real-time prices
    merged_data = pd.merge(real_time_data, historical_data, on='symbol', suffixes=('_real', '_hist'))

    # Calculate the price difference and compare with threshold
    merged_data['price_diff'] = abs(merged_data['price_real'] - merged_data['price_hist'])
    significant_changes = merged_data[merged_data['price_diff'] > threshold]

    return significant_changes[['symbol', 'price_real', 'price_hist']].values.tolist()


def main():
    # real_time_data = get_real_time_data()
    # #read csv file
    # historical_data = pd.read_csv("AI_HFT_Quantum_Project/data/real_time/real-time-data.csv")
    # significant_change = compare_data_with_historical_data(historical_data, real_time_data, 0.1)
    # print(significant_change)
    # #save it into csv file
    # real_time_data.to_csv("AI_HFT_Quantum_Project/data/real_time/real-time-data.csv", index=False)
    print(get_historical_data('BTCUSDT'))

if __name__ == "__main__":
    main()