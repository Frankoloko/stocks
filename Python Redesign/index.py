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

SHOW_GRAPHS = True
MINIMAL_OUTPUT = True

STOCKS = [
    # {
    #     'name': 'Apple',
    #     'symbol': 'AAPL'
    # },
    # {
    #     'name': 'Etsy',
    #     'symbol': 'ETSY'
    # },
    # {
    #     'name': 'Netflix',
    #     'symbol': 'NFLX'
    # },
    # {
    #     'name': 'Pinterest',
    #     'symbol': 'PINS'
    # },
    # {
    #     'name': 'Spotify',
    #     'symbol': 'SPOT'
    # },
    # {
    #     'name': 'Tesla',
    #     'symbol': 'TSLA'
    # },
    # {
    #     'name': 'Uber',
    #     'symbol': 'U'
    # },
    {
        'name': 'Wix.com',
        'symbol': 'WIX'
    },
    # {
    #     'name': 'Zoom',
    #     'symbol': 'ZM'
    # },
]

##############################################################################################################################
# GET THE DATA

def run():
    for stock in STOCKS:
        data = {}

        # Get the data from the internet
        if DATA_FROM == 'internet':
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock['symbol']}&outputsize=full&apikey=5719SGI5O6BMNFGM"
            request = requests.get(url=url)
            response_data = request.json()
            sleep(13) # Alpha Vantage API only allows 5 calls per minute. So here we wait for a 5th of a minute

            if 'Note' in response_data:
                print(response_data)
            data = response_data['Time Series (Daily)']

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
                graph_data[date] = int(data[date].split('.')[0])
                cumilative_total += graph_data[date]
                if not current:
                    current = graph_data[date]
                if float(data[date]) > max_value:
                    max_value = float(data[date])
                if float(data[date]) < min_value:
                    min_value = float(data[date])

        mid = (max_value + min_value) / 2
        average = cumilative_total / len(graph_data)
        min_to_max_percentage = (max_value - min_value) / min_value * 100
        current_to_average_percentage = int((current - min_value) / min_value * 100)
        if current > average:
            current_to_average_percentage = f'-{current_to_average_percentage}'
        else:
            current_to_average_percentage = f'{current_to_average_percentage}'

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
            print(f'Min\t\t\t\t\t{int(min_value)}')
            print(f'Max\t\t\t\t\t{int(max_value)}')
            print(f'Average\t\t\t\t{int(average)}')
            print()
            print(f'Min -> Max\t\t\t{int(min_to_max_percentage)}%')
        print(f'Current -> Average\t{current_to_average_percentage}% (you want this to be above 20% or higher)')

        # Labels x, y and title
        pyplot.xlabel('Date')
        pyplot.xticks(rotation=90)
        pyplot.ylabel('Stock Value')
        pyplot.suptitle(f"{stock['name']}")
        pyplot.legend() # Show a legend on the plot
        if SHOW_GRAPHS:
            pyplot.show() # Show the plot

run()