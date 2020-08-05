// Setup
    // This file's object will dictate all the calls that are run, therefore, comment out any stocks that you don't want want to watch any more
    // The calls we make need an API key, every API key can only make 5 calls per minutes, therefore you need your own API key
    // Get your own API key here: https://www.alphavantage.co/support/#api-key
    // YOU CAN ONLY HAVE A MAX OF 5 STOCKS (The API limits this)

// Stocks have to look like this
    // "CPI": {
    //     "max": 99000, // optional
    //     "min": 1825, // optional
    //     "purchase": 96111 // optional
    //     "upPercent": 1, // optional, requires a purchase value!
    //     "downPercent": 1 // optional, requires a purchase value!
    // }

module.exports = {
    "apiKey": "5719SGI5O6BMNFGM", // The API key aquired above (check the Setup section)
    "interval": "1min", // "1min", "5min", "15min", "30min", "60min"
    "easyEquitiesUrl": "`https://platform.easyequities.co.za/Sell/Confirm?ContractCode=EQU.ZA.${stock}`", // This is the URL you are taken to when the alert popup asks you. Use ${stock} if you want to make use of the stock's symbol
    // "CPI": {
        // "max": 99000,
        // "min": 1825,
    //     "purchase": 96111,
    //     "upPercent": 5,
    //     "downPercent": 10
    // },
    // "SOL": {
    //     "max": 99000,
    //     "min": 1825,
    //     "purchase": 96111,
    //     "upPercent": 1,
    //     "downPercent": 1
    // },
    // "LHC": {
    //     "max": 1900,
    //     "min": 1800,
    //     // "purchase": 1822,
    //     // "upPercent": 5,
    //     // "downPercent": 10
    // },
    "SHP": {
        "max": 11100,
        // "min": 1800,
        "purchase": 10980,
        "upPercent": 1,
        // "upPercent": 2, 11152
        "downPercent": 3
    },
}