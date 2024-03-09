
import base64
import requests
import time
import hmac
import hashlib
import json

import os
from dotenv import load_dotenv

load_dotenv("AI_HFT_Quantum_Project/secret.env")

# Retrieve API key and secret from environment variables
API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')


# API base URL
BASE_URL = 'https://testnet.binance.vision/api'

def generate_signature(query_string):
    return hmac.new(SECRET_KEY.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def make_request(method, endpoint, params=None, add_signature=False):
    url = BASE_URL + endpoint
    headers = {'X-MBX-APIKEY': API_KEY}

    if add_signature:
        timestamp = int(time.time() * 1000)
        params['timestamp'] = timestamp
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        signature = generate_signature(query_string)
        params['signature'] = signature

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Oops: Something Else: {err}")
    except json.decoder.JSONDecodeError:
        print("Could not decode the response JSON")
    return None

def get_usdt_balance():
    endpoint = '/v3/account'
    response = make_request("GET", endpoint, {}, True)

    if response and 'balances' in response:
        for balance in response['balances']:
            if balance['asset'] == 'USDT':
                return float(balance['free'])
    return None

def get_symbol_price(symbol):
    endpoint = '/v3/ticker/price'
    response = make_request("GET", endpoint, {'symbol': symbol})

    if response and 'price' in response:
        return float(response['price'])
    return None

def execute_trade(symbol, quantity, side):
    endpoint = '/v3/order'
    params = {
        'symbol': symbol,
        'side': side,
        'type': 'MARKET',
        'quantity': quantity,
    }
    response = make_request("POST", endpoint, params, True)

    if response:
        print("Trade executed successfully:", response)
    else:
        print("Error in executing trade")

def get_symbol_balance(symbol):
    symbol = symbol.replace('USDT', '')
    endpoint = '/v3/account'
    response = make_request("GET", endpoint, {}, True)

    if response and 'balances' in response:
        for balance in response['balances']:
            if balance['asset'] == symbol:
                return float(balance['free'])
    return None

def execution(symbol, quantity, side):
    if side == 'BUY':
        if check_wallet_has_enough_balance(symbol, quantity):
            execute_trade(symbol, quantity, side)
        else:
            print("Insufficient USDT balance to buy.")
    elif side == 'SELL':
        if check_wallet_has_enough_symbol_to_sale(symbol, quantity):
            execute_trade(symbol, quantity, side)
        else:
            print(f"Insufficient {symbol} balance to sell.")

def check_wallet_has_enough_balance(symbol, quantity):
    usdt_balance = get_usdt_balance()
    symbol_price = get_symbol_price(symbol)
    if usdt_balance is not None and symbol_price is not None:
        return usdt_balance >= symbol_price * quantity
    return False

def check_wallet_has_enough_symbol_to_sale(symbol, quantity):
    symbol_balance = get_symbol_balance(symbol)
    print("Balance of ", symbol, " in wallet: ", symbol_balance)
    if symbol_balance is not None:
        return symbol_balance >= quantity
    return False

def get_account_info():
    endpoint = '/v3/account'
    response = make_request("GET", endpoint, {}, True)
    #convert response to json and save to file
    with open('AI_HFT_Quantum_Project/trading/account_info.json', 'w') as f:
        json.dump(response, f)
    return response

# signal = {'symbol': 'COMPUSDT', 'action': 'BUY', 'confidence': 0.8, 'volume': 1}
def convert_signal_to_trade_action(signal):
    symbol = signal['symbol']
    action = signal['action']
    confidence = signal['confidence']
    volume = signal['volume']

    if action == 'BUY' and confidence >= 0.8:
        execution(symbol, volume, action)
    elif action == 'SELL' and confidence >= 0.8:
        execution(symbol, volume, action)
    elif action == 'HOLD':
        print("HOLD signal received. No action taken.")
    else:
        print("Signal is not strong enough to execute trade")
def main():
    #Simulate trading environment
    get_account_info()
    print("Simulating trading environment")
    print("Amount of USDT in wallet: ", get_usdt_balance())
    execution('COMPUSDT', 1, 'BUY')
    time.sleep(1)
    execution('COMPUSDT', 1, 'SELL')
    time.sleep(1)
    execution('GNOUSDT', 1, 'BUY')
    time.sleep(1)
    execution('GNOUSDT', 1, 'SELL')
    time.sleep(1)
    print("Amount of USDT in wallet: ", get_usdt_balance())
    print("Simulated trading completed")


if __name__ == '__main__':
    main()
