// https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=SHP.JO&outputsize=full&apikey=5719SGI5O6BMNFGM
// https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=SHP.JO&interval=60min&outputsize=full&apikey=5719SGI5O6BMNFGM

module.exports = stocks = {
    absa: {
        data: {
            daily: [],
            halfDaily: [],
            hourly: []
        }
    },
    britishTobacco: {
        data: {
            daily: [],
            halfDaily: [],
            hourly: []
        }
    },
    capitec: {
        data: {
            daily: [],
            halfDaily: [],
            hourly: []
        }
    },
    clicks: {
        data: {
            daily: [],
            halfDaily: [],
            hourly: []
        }
    },
    discovery: {
        data: {
            daily: [],
            halfDaily: [],
            hourly: []
        }
    },
    mrp: {
        data: {
            daily: [],
            halfDaily: [],
            hourly: []
        }
    },
    mtn: {
        data: {
            daily: [],
            halfDaily: [],
            hourly: []
        }
    },
    nedbank: {
        data: {
            daily: [],
            halfDaily: [],
            hourly: []
        }
    },
    pnp: {
        data: {
            daily: [],
            halfDaily: [],
            hourly: []
        }
    },
    sasol: {
        data: {
            daily: [],
            halfDaily: [],
            hourly: []
        }
    },
};

for (stock in stocks) {
    // Add daily
        data = require(`./data/daily/${stock}-daily.json`);
        for (key in data) {
            stocks[stock].data.daily.push({
                date: key,
                open: Math.round(data[key]['1. open']),
                high: Math.round(data[key]['2. high']),
                low: Math.round(data[key]['3. low']),
                close: Math.round(data[key]['4. close']),
                volume: Math.round(data[key]['5. volume'])
            });
        }

    // Add hourly
        data = require(`./data/hourly/${stock}-hourly.json`);
        for (key in data) {
            stocks[stock].data.hourly.push({
                date: key,
                open: Math.round(data[key]['1. open']),
                high: Math.round(data[key]['2. high']),
                low: Math.round(data[key]['3. low']),
                close: Math.round(data[key]['4. close']),
                volume: Math.round(data[key]['5. volume'])
            });
        }
}

for (stock in stocks) {
    stocks[stock].data.daily.reverse();
    stocks[stock].data.hourly.reverse();
}