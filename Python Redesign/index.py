import pprint
pprint = pprint.PrettyPrinter().pprint
import json
import matplotlib.pyplot as plt

##################### GET THE DATA INTO VARIABLES #####################
 
stocks = [
    'TSLA',
    'AAPL',
    'ETSY',
    'NFLX',
    'PINS',
    'SPOT',
    'TSLA',
    'UBER',
    'U',
    'WIX',
    'ZM'
]

data = {}
root_folder = __file__.replace('/index.py', '')
for stock in stocks:
    # Get the data
    with open(f'{root_folder}/data/TIME_SERIES_DAILY/{stock}.json') as json_file:
        file_data = json.load(json_file)

    data[stock] = file_data['Time Series (Daily)']
    # Remove all the other money values, we only want the "close" value
    for date in data[stock]:
        data[stock][date] = data[stock][date]['4. close']

    # Reverse the dates order
    # data[stock] = dict(sorted(data[stock].items(), key=lambda x: x[1], reverse=True))

##################### RUN THE TESTS #####################

pprint(data)

##################### GRAPH THE RESULTS #####################

for stock in data:
    x_values = []
    y_values = []
    for date in reversed(data[stock]): # You need to use reversed here since the dates are in the wrong order
        if date > '2021-01-01':
            x_values.append(date)
            y_values.append(int(data[stock][date].split('.')[0]))

    plt.plot(x_values, y_values, label=stock)

# Labels x, y and title
plt.xlabel('Date')
plt.xticks(rotation=90)
plt.ylabel('Stock Value')
plt.title('Two lines on same graph!')
plt.legend() # Show a legend on the plot
plt.show() # Show the plot