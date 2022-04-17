import requests
import os
import time
from datetime import datetime

# How to work out what you bought something at:
# stock_current_value + (your_current_percentage / 100 * stock_current_value)
#                     ^ this must be + if you are in the negative, - if you are in the positive


# 115+(0.44*115)

# 100-(115/208*100)=44
# -(115/208*100)=44-100
# 115/208*100=(44-100)*-1
# 115/208=((44-100)*-1)/100
# 208=115/(((44-100)*-1)/100)
# current_value/(((your_current_percentage-100)*-1)/100)
# 115/(((44-100)*-1)/100)

INTERVAL = '1min' # '1min', '5min', '15min', '30min', '60min'
STOCKS = [
    { 'name': 'Etsy', 'symbol': 'ETSY', 'bought_at': 208, 'sell_percentage': '10%' },
    { 'name': 'Google', 'symbol': 'GOOGL', 'bought_at': 2704, 'sell_percentage': '10%' },
    { 'name': 'Netflix', 'symbol': 'NFLX', 'bought_at': 542, 'sell_percentage': '10%' },
    { 'name': 'Pinterest', 'symbol': 'PINS', 'bought_at': 84, 'sell_percentage': '10%' },
    { 'name': 'Spotify', 'symbol': 'SPOT', 'bought_at': 285, 'sell_percentage': '10%' },
    { 'name': 'Uber', 'symbol': 'UBER', 'bought_at': 59, 'sell_percentage': '10%' },
    { 'name': 'Unity', 'symbol': 'U', 'bought_at': 97, 'sell_percentage': '10%' },
    { 'name': 'Vanguard S&P 500 ETF', 'symbol': 'VOO', 'bought_at': 405, 'sell_percentage': '10%' },
    { 'name': 'Wix.com', 'symbol': 'WIX', 'bought_at': 303, 'sell_percentage': '10%' },
    { 'name': 'Zoom', 'symbol': 'ZM', 'bought_at': 328, 'sell_percentage': '10%' },
]

def notify(title, description, subtext):
    os.system(f"osascript -e 'display notification \"{subtext}\" with title \"{title}\" subtitle \"{description}\" sound name \"Submarine\"'")

def run():
    for stock in STOCKS:

        # Get the stock data from the API
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock['symbol']}&interval={INTERVAL}&apikey=5719SGI5O6BMNFGM"
        print(f"Fetching {stock['name']}...")
        request = requests.get(url=url)
        response_data = request.json()
        time.sleep(13) # Alpha Vantage API only allows 5 calls per minute. So here we wait for a 5th of a minute

        # Check the response data
        if f'Time Series ({INTERVAL})' in response_data:
            data = response_data[f'Time Series ({INTERVAL})']
        else:
            print(url)
            print(response_data)
            raise Exception(f"'Time Series ({INTERVAL})' was not found in the response object (see above)")

        # Get the stock's current value
        first_key = next(iter(data))
        stock_current_value = float(data[first_key]['4. close'])

        # Get the sell percentage
        sell_percentage = stock['sell_percentage']
        if '%' in sell_percentage:
            sell_percentage = sell_percentage.replace('%', '')
        sell_percentage = int(sell_percentage)

        # Work out if we need to sell
        sell_price = ((sell_percentage / 100) * stock['bought_at']) + stock['bought_at']

        # Get the current date and time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S %d/%m/%Y")

        # Work out what our current % holding is
        current_percentage_value = stock_current_value / stock['bought_at'] * 100
        if current_percentage_value > 100:
            current_percentage_value = current_percentage_value - 100
        else:
            current_percentage_value = (100 - current_percentage_value) * -1

        # Print out info
        print(current_time)
        print(f"Bought At:\t\t\t{stock['bought_at']}")
        print(f"Current Value:\t\t{stock_current_value}")
        print(f"Sell Price:\t\t\t{sell_price}")
        print(f"Current Percentage:\t{round(current_percentage_value)}%")
        if stock_current_value > sell_price:
            print('*'*16)
            print('!!! SELL NOW !!!')
            notify(
                title="SELL STOCK",
                description=f"{stock['name']}",
                subtext=f"Current value: +{round(current_percentage_value)}%"
            )
            print('*'*16)
        print('-'*30)

run()
# while True:
#     run()
#     time.sleep(60 * 5) # Run every (* min)