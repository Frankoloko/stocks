import os
import pprint
pprint = pprint.PrettyPrinter().pprint
import json
from matplotlib import pyplot
import datetime

##################### GET THE DATA INTO VARIABLES #####################
 
stocks = []
data = {}
root_folder = os.path.dirname(__file__)
TIME_SERIES_DAILY_folder = os.path.join(root_folder, 'data', 'TIME_SERIES_DAILY')
for file in os.listdir(TIME_SERIES_DAILY_folder):
    file_path = os.path.join(TIME_SERIES_DAILY_folder, file)
    stock = file.replace('.json', '')

    # Test only certain stocks
    # if stock != 'TSLA':
    if stock != 'AAPL':
        continue
        pass

    stocks.append(stock)

    # Get the data
    with open(file_path) as json_file:
        file_data = json.load(json_file)

    data[stock] = file_data['Time Series (Daily)']
    # Remove all the other money values, we only want the "close" value
    for date in data[stock]:
        data[stock][date] = data[stock][date]['4. close']

# Prepare the graph data object
graph_data = {}
for stock in stocks:
    graph_data[stock] = {}

############################################ RUN THE TESTS ############################################

# Graph all daily values
# start_date = '2018-01-01'
# end_date = '2019-01-01'
start_date = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y-%m-%d") # 1 year ago
end_date = datetime.datetime.now().strftime("%Y-%m-%d")
min_value = 99999
max_value = -99999
cumilative_total = 0
current = None
for stock in data:
    for date in data[stock]:
        if date > start_date and date < end_date:
            graph_data[stock][date] = int(data[stock][date].split('.')[0])
            cumilative_total += graph_data[stock][date]
            if not current:
                current = graph_data[stock][date]
            if float(data[stock][date]) > max_value:
                max_value = float(data[stock][date])
            if float(data[stock][date]) < min_value:
                min_value = float(data[stock][date])

mid = (max_value + min_value) / 2
average = cumilative_total / len(graph_data[stock])
min_to_max_percentage = (max_value - min_value) / min_value * 100
current_to_average_percentage = int((current - min_value) / min_value * 100)
if current > average:
    current_to_average_percentage = f'-{current_to_average_percentage}'
else:
    current_to_average_percentage = f'{current_to_average_percentage}'

########################################## GRAPH THE RESULTS ##########################################

for stock in graph_data:
    x_values = []
    y_values = []
    start_end_dates = []
    for index, date in enumerate(reversed(graph_data[stock])): # You need to use reversed here since the dates are in the wrong order
        x_values.append(date)
        y_values.append(graph_data[stock][date])

        if index == 0:
            start_end_dates.append(date)
        if index == len(graph_data[stock]) - 1:
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
print(f'Start\t\t\t\t{start_date}')
print(f'End\t\t\t\t\t{end_date}')
print()
print(f'Current\t\t\t\t{current}')
print(f'Min\t\t\t\t\t{int(min_value)}')
print(f'Max\t\t\t\t\t{int(max_value)}')
print(f'Average\t\t\t\t{int(average)}')
print()
print(f'Min -> Max\t\t\t{int(min_to_max_percentage)}%')
print(f'Current -> Average\t{current_to_average_percentage}%')

# Labels x, y and title
pyplot.xlabel('Date')
pyplot.xticks(rotation=90)
pyplot.ylabel('Stock Value')
pyplot.suptitle(f"{stock}")
pyplot.legend() # Show a legend on the plot
pyplot.show() # Show the plot