# CryptoPriceNotifier

CryptoPriceNotifier is a simple Python script that fetches the current prices of Bitcoin and Ethereum from the CoinGecko API and sends them to a Discord webhook every hour. The script uses `schedule` for task scheduling and `requests` for HTTP requests.

## Features

- Fetches Bitcoin and Ethereum prices from CoinGecko API
- Sends the prices to a Discord webhook as an embed message
- Runs the task every hour

## Requirements

- Python 3.x
- `pip install requests` 
- `pip install schedule` 
