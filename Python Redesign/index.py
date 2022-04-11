import os
import pprint
pprint = pprint.PrettyPrinter().pprint
import json
import matplotlib.pyplot as plt

##################### GET THE DATA INTO VARIABLES #####################
 
stocks = []
data = {}
root_folder = os.path.dirname(__file__)
TIME_SERIES_DAILY_folder = os.path.join(root_folder, 'data', 'TIME_SERIES_DAILY')
for file in os.listdir(TIME_SERIES_DAILY_folder):
    file_path = os.path.join(TIME_SERIES_DAILY_folder, file)
    stock = file.replace('.json', '')

    # Test only certain stocks
    if stock != 'TSLA':
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

# Buy at the start of each month
# start_date = '2021-01-01'
# for stock in data:
#     month = '01'
#     for date in reversed(data[stock]):
#         if date > start_date:
#             if month != date[5:7]:
#                 graph_data[stock][date] = data[stock][date]
#                 month = date[5:7]

# Graph all daily values
start_date = '2021-04-01'
for stock in data:
    for date in data[stock]:
        if date > start_date:
            graph_data[stock][date] = data[stock][date]

########################################## GRAPH THE RESULTS ##########################################

for stock in graph_data:
    x_values = []
    y_values = []
    for date in reversed(graph_data[stock]): # You need to use reversed here since the dates are in the wrong order
        x_values.append(date)
        y_values.append(int(graph_data[stock][date].split('.')[0]))

    plt.plot(x_values, y_values, label=stock)

# Labels x, y and title
plt.xlabel('Date')
plt.xticks(rotation=90)
plt.ylabel('Stock Value')
plt.title('Two lines on same graph!')
plt.legend() # Show a legend on the plot
plt.show() # Show the plot