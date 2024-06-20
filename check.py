import requests
import json
import argparse
import logging
from prettytable import PrettyTable


class CryptoPriceFetcher:
    def __init__(self, config):
        self.api_url = "https://api.coingecko.com/api/v3/simple/price"
        self.cryptos = config['cryptos']
        self.currency = config['currency']
        self.output_file = config['output_file']

    def fetch_prices(self):
        try:
            response = requests.get(self.api_url, params={'ids': ','.join(self.cryptos), 'vs_currencies': self.currency})
            response.raise_for_status()
            data = response.json()
            return self.parse_prices(data)
        except requests.RequestException as e:
            logging.error(f"Error fetching prices: {e}")
            return None

    def parse_prices(self, data):
        prices = {}
        for crypto in self.cryptos:
            prices[crypto.upper()] = data.get(crypto, {}).get(self.currency, 'N/A')
        return prices

    def display_prices(self, prices):
        if not prices:
            logging.warning("No prices available to display.")
            return
        
        table = PrettyTable()
        table.field_names = ["Cryptocurrency", "Price (USD)"]
        
        for crypto, price in prices.items():
            table.add_row([crypto, f"${price}"])
        
        print(table)

    def save_prices(self, prices):
        try:
            with open(self.output_file, 'w') as file:
                json.dump(prices, file, indent=4)
            logging.info(f"Prices saved to {self.output_file}")
        except IOError as e:
            logging.error(f"Error saving prices to file: {e}")

def load_config(config_file):
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
        return config
    except IOError as e:
        logging.error(f"Error reading configuration file: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Fetch and display cryptocurrency prices.')
    parser.add_argument('--config', type=str, default='config.json', help='Path to the configuration file.')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    config = load_config(args.config)
    if not config:
        logging.error("Configuration not found or invalid.")
        return

    fetcher = CryptoPriceFetcher(config)
    prices = fetcher.fetch_prices()
    if prices:
        fetcher.display_prices(prices)
        fetcher.save_prices(prices)

if __name__ == "__main__":
    main()
