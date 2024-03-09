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

def main():
    df = get_real_time_data()
    #save it into csv file
    df.to_csv("AI_HFT_Quantum_Project/data/real-time/real-time-data.csv", index=False)
    print(df)

if __name__ == "__main__":
    main()