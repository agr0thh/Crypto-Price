import requests
import schedule
import time
import json

WEBHOOK_URL = 'WEBHOOK-HERE'

def get_prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
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

def send_webhook(prices):
    if not prices:
        print("No prices to send.")
        return
    
    payload = {
        "embeds": [{
            "title": "Crypto Prices Update",
            "description": f"**Bitcoin (BTC)**: ${prices['BTC']}\n**Ethereum (ETH)**: ${prices['ETH']}",
            "color": 3447003  # Blue color
        }]
    }
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers=headers)
        response.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
        print(f"Webhook sent: {response.status_code} with payload: {payload}")
    except requests.RequestException as e:
        print(f"Error sending webhook: {e}")

def job():
    prices = get_prices()
    if prices:
        print(f"Fetched prices: BTC: {prices['BTC']}, ETH: {prices['ETH']}")
    send_webhook(prices)

# Schedule the job every hour
schedule.every().hour.do(job)

# Run the job immediately for the first time
job()

while True:
    schedule.run_pending()
    time.sleep(1)