import requests

URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=5719SGI5O6BMNFGM&outputsize=full"
request = requests.get(url=URL)
data = request.json()
  
print(data)