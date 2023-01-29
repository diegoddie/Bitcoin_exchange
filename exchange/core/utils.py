import requests
import json 
import os

def get_btc_data():
    URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    API_KEY = os.environ.get('API_KEY')
    
    params = {
        "start":"1",
        "limit":"1",
        "convert": "USD"
    }

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": API_KEY
    }

    data_usd = requests.get(url=URL, headers=headers, params=params).json()

    btc_usd_price = round(data_usd['data'][0]['quote']['USD']['price'], 2)
    btc_usd_change = round(data_usd['data'][0]['quote']['USD']['percent_change_24h'],2)

    return btc_usd_price, btc_usd_change


    

