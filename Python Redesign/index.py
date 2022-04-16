import os
import pprint
pprint = pprint.PrettyPrinter().pprint
import json
from matplotlib import pyplot
import datetime
import requests
from time import sleep

##############################################################################################################################
# SETTINGS

root_folder = os.path.dirname(__file__)
TIME_SERIES_DAILY_FOLDER = os.path.join(root_folder, 'data', 'TIME_SERIES_DAILY')

DATA_FROM = 'internet'
# DATA_FROM = 'jsons'

SHOW_GRAPHS = False
MINIMAL_OUTPUT = True

STOCKS = [
    { 'name': 'Adobe', 'symbol': 'ADBE' },
    { 'name': 'Airbnb', 'symbol': 'ABNB' },
    { 'name': 'AMD', 'symbol': 'AMD' },
    { 'name': 'Apple', 'symbol': 'AAPL' },
    { 'name': 'Asana', 'symbol': 'ASAN' },
    { 'name': 'Atlassian', 'symbol': 'TEAM' },
    { 'name': 'Autodesk', 'symbol': 'ADSK' },
    { 'name': 'Beyond Meat', 'symbol': 'BYND' },
    { 'name': 'BP', 'symbol': 'BP' },
    { 'name': 'Bumble', 'symbol': 'BMBL' },
    { 'name': 'Callaway', 'symbol': 'ELY' },
    { 'name': 'CAT', 'symbol': 'CAT' },
    { 'name': 'Chipolte', 'symbol': 'CMG' },
    { 'name': 'Coca Cola', 'symbol': 'KO' },
    { 'name': 'Dropbox', 'symbol': 'DBX' },
    { 'name': 'EA', 'symbol': 'EA' },
    { 'name': 'Ebay', 'symbol': 'EBAY' },
    { 'name': 'Etsy', 'symbol': 'ETSY' },
    { 'name': 'Facebook/Meta', 'symbol': 'FB' },
    { 'name': 'FedEx', 'symbol': 'FDX' },
    { 'name': 'Ferrari', 'symbol': 'RACE' },
    { 'name': 'Fiverr', 'symbol': 'FVRR' },
    { 'name': 'Ford', 'symbol': 'F' },
    { 'name': 'Garmin', 'symbol': 'GRMN' },
    { 'name': 'GM', 'symbol': 'GM' },
    { 'name': 'GoPro', 'symbol': 'GPRO' },
    { 'name': 'Hasbro', 'symbol': 'HAS' },
    { 'name': 'Honda', 'symbol': 'HMC' },
    { 'name': 'IBM', 'symbol': 'IBM' },
    { 'name': 'Intel', 'symbol': 'INTC' },
    { 'name': 'John Deere', 'symbol': 'DE' },
    { 'name': 'Johnson & Johnson', 'symbol': 'JNJ' },
    { 'name': 'Kelloggs', 'symbol': 'K' },
    { 'name': 'Kodak', 'symbol': 'KODK' },
    { 'name': 'Logitec', 'symbol': 'LOGI' },
    { 'name': 'Manchester United', 'symbol': 'MANU' },
    { 'name': 'MasterCard', 'symbol': 'MA' },
    { 'name': 'McDonalds', 'symbol': 'MCD' },
    { 'name': 'Microsoft', 'symbol': 'MSFT' },
    { 'name': 'MongoDB', 'symbol': 'MDB' },
    { 'name': 'Monster', 'symbol': 'MNST' },
    { 'name': 'Netflix', 'symbol': 'NFLX' },
    { 'name': 'Nike', 'symbol': 'NKE' },
    { 'name': 'Nokia', 'symbol': 'NOK' },
    { 'name': 'Norton', 'symbol': 'NLOK' },
    { 'name': 'Nvidia', 'symbol': 'NVDA' },
    { 'name': 'PayPal', 'symbol': 'PYPL' },
    { 'name': 'Pfizer', 'symbol': 'PFE' },
    { 'name': 'Pinterest', 'symbol': 'PINS' },
    { 'name': 'Sony', 'symbol': 'SONY' },
    { 'name': 'Spotify', 'symbol': 'SPOT' },
    { 'name': 'Squarespace', 'symbol': 'SQSP' },
    { 'name': 'Tesla', 'symbol': 'TSLA' },
    { 'name': 'Toyota', 'symbol': 'TM' },
    { 'name': 'Trip Advisor', 'symbol': 'TRIP' },
    { 'name': 'Uber', 'symbol': 'UBER' },
    { 'name': 'Unity', 'symbol': 'U' },
    { 'name': 'UPS', 'symbol': 'UPS' },
    { 'name': 'Visa', 'symbol': 'V' },
    { 'name': 'Vodafone', 'symbol': 'VOD' },
    { 'name': 'Walmart', 'symbol': 'WMT' },
    { 'name': 'Walt Disney', 'symbol': 'DIS' },
    { 'name': 'Wish', 'symbol': 'WISH' },
    { 'name': 'Wix.com', 'symbol': 'WIX' },
    { 'name': 'WWE', 'symbol': 'WWE' },
    { 'name': 'Zoom', 'symbol': 'ZM' },
    { 'name': 'Zynga', 'symbol': 'ZNGA' },
]

##############################################################################################################################
# GET THE DATA

def run():
    best_current_to_average_percentage = { 'symbol': '?', 'value': -999 }
    print(f'Checking {len(STOCKS)} stocks...')

    for stock in STOCKS:
        data = {}

        # Get the data from the internet
        if DATA_FROM == 'internet':
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock['symbol']}&outputsize=full&apikey=5719SGI5O6BMNFGM"
            request = requests.get(url=url)
            response_data = request.json()
            sleep(13) # Alpha Vantage API only allows 5 calls per minute. So here we wait for a 5th of a minute

            if 'Time Series (Daily)' in response_data:
                data = response_data['Time Series (Daily)']
            else:
                print(url)
                print(response_data)
                raise Exception("'Time Series (Daily)' was not found in the response object (see above)")

            # Remove all the other money values, we only want the "close" value
            for date in data:
                data[date] = data[date]['4. close']

        # Get the data from json files
        if DATA_FROM == 'jsons':
            file_path = os.path.join(TIME_SERIES_DAILY_FOLDER, stock['symbol'] + '.json')

            # Get the data
            with open(file_path) as json_file:
                file_data = json.load(json_file)

            data = file_data['Time Series (Daily)']
            # Remove all the other money values, we only want the "close" value
            for date in data:
                data[date] = data[date]['4. close']

        # Prepare the graph data object
        graph_data = {}

        ##############################################################################################################################
        # RUN THE TESTS

        # Graph all daily values
        # start_date = '2018-01-01'
        # end_date = '2019-01-01'
        start_date = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y-%m-%d") # 1 year ago
        end_date = datetime.datetime.now().strftime("%Y-%m-%d")
        min_value = 99999
        max_value = -99999
        cumilative_total = 0
        current = None
        for date in data:
            if date > start_date and date < end_date:
                value = float(data[date])
                graph_data[date] = value
                cumilative_total += value
                if not current:
                    current = value
                if value > max_value:
                    max_value = value
                if value < min_value:
                    min_value = value

        mid = (max_value + min_value) / 2
        average = cumilative_total / len(graph_data)
        min_to_max_percentage = (max_value - min_value) / min_value * 100
        current_to_average_percentage = (current - average) / average * 100
        if current < average:
            current_to_average_percentage = current_to_average_percentage * -1
        if current_to_average_percentage > best_current_to_average_percentage['value']:
            best_current_to_average_percentage['name'] = stock['name']
            best_current_to_average_percentage['symbol'] = stock['symbol']
            best_current_to_average_percentage['value'] = current_to_average_percentage

        ##############################################################################################################################
        # GRAPH THE RESULTS

        x_values = []
        y_values = []
        start_end_dates = []
        for index, date in enumerate(reversed(graph_data)): # You need to use reversed here since the dates are in the wrong order
            x_values.append(date)
            y_values.append(graph_data[date])

            if index == 0:
                start_end_dates.append(date)
            if index == len(graph_data) - 1:
                start_end_dates.append(date)

        # Plot the main stock value
        pyplot.plot(x_values, y_values, label='Value')

        # Plot the Mid values
        y_mid_values = [mid, mid]
        pyplot.plot(start_end_dates, y_mid_values, label='Mid')

        # Plot the Avg values
        average_values = [average, average]
        pyplot.plot(start_end_dates, average_values, label='Average')

        # Just print info, since it is too much to show on the graph
        print('-'*70)
        print(f"{stock['name']}")
        if not MINIMAL_OUTPUT:
            print()
            print(f'Start\t\t\t\t{start_date}')
            print(f'End\t\t\t\t\t{end_date}')
            print()
            print(f'Current\t\t\t\t{current}')
            print(f'Min\t\t\t\t\t{round(min_value, 2)}')
            print(f'Max\t\t\t\t\t{round(max_value, 2)}')
            print(f'Average\t\t\t\t{round(average, 2)}')
            print()
            print(f'Min -> Max\t\t\t{round(min_to_max_percentage, 2)}%')
        print(f'Current -> Average\t{round(current_to_average_percentage, 2)}% (you want this to be above 20% or higher)')

        # Labels x, y and title
        pyplot.xlabel('Date')
        pyplot.xticks(rotation=90)
        pyplot.ylabel('Stock Value')
        pyplot.suptitle(f"{stock['name']}")
        pyplot.legend() # Show a legend on the plot
        if SHOW_GRAPHS:
            pyplot.show() # Show the plot

    print('='*70)
    print(f"BEST CURRENT -> AVERGAGE:\n{best_current_to_average_percentage['name']}: {round(best_current_to_average_percentage['value'], 2)}%" )

run()