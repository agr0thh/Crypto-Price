import requests
import json

def get_prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        prices = {
            'BTC': data['bitcoin']['usd'],
            'ETH': data['ethereum']['usd']
        }
        print(f"Prices fetched: {prices}")
        return prices
    except requests.RequestException as e:
        print(f"Error fetching prices: {e}")
        return None

def main():
    prices = get_prices()
    if prices:
        print(f"Bitcoin (BTC): ${prices['BTC']}")
        print(f"Ethereum (ETH): ${prices['ETH']}")

if __name__ == "__main__":
    main()