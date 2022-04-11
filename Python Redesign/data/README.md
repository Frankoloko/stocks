https://www.alphavantage.co/documentation/
You are only allowed to make 5 API calls within each 1min. So making a loop to fetch data etc is pointless. Therefore, just take this string and paste it in your browser (filling in the STOCK value):

https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=STOCK&apikey=5719SGI5O6BMNFGM&outputsize=full
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey=5719SGI5O6BMNFGM&outputsize=full

Then copy-paste the data to a json file in this "data" folder.