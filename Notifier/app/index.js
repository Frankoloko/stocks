console.log('Money Maker is watching the stocks for you mate!');
console.log('Now just chill. Do your work. You have nothing to worry about :)');

const confirm = require('node-popup').confirm;
const open = require('open');
const http = require('request');
const config = require(`../setup.js`);

let url, timeSeries, closePrice, easyEquitiesUrl, date, time, hours, minutes, logString;

setInterval(() => {
    // Log time
    console.log('----------------------------');
    date = new Date();
    hours = date.getHours();
    minutes = date.getMinutes();
    time = (hours < 10 ? '0' + hours : hours) + ':' + (minutes < 10 ? '0' + minutes : minutes);
    console.log(time);

    for (let stock in config) {
        if (stock == 'interval' || stock == 'apiKey' || stock == 'easyEquitiesUrl') continue;

        url = `https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=${stock}.JO&interval=${config.interval}&outputsize=compact&apikey=${config.apiKey}`;

        http.get(url, async (err, res, body) => {
            if (err) return console.log(err);
            body = JSON.parse(body);
            easyEquitiesUrl = eval(config.easyEquitiesUrl);

            // Get stock close price
            timeSeries = body[`Time Series (${config.interval})`];
            if (!timeSeries) return console.log(stock + ' (Problem with HTTP call body)' + '\t' + time);
            closePrice = Number(timeSeries[Object.keys(timeSeries)[0]]['4. close']);
            logString = stock + ': ' + closePrice;

            // Check if max has been passed
            if (config[stock].hasOwnProperty('max')) {
                if (closePrice > config[stock].max) {
                    logString += ' WENT OVER MAX!';
                    try {
                        await confirm(`${stock} went over max!!! \n Proceed to Easy Equities URL?`);
                        
                        // Confirmed
                        open(easyEquitiesUrl);
                    } catch (error) {
                        // Cancelled
                    }
                }
            }

            // Check if min has been passed
            if (config[stock].hasOwnProperty('min')) {
                if (closePrice < config[stock].min) {
                    logString += ' WENT UNDER MIN!';
                    try {
                        await confirm(`${stock} went under min!!! Proceed to Easy Equities URL?`);
    
                        // Confirmed
                        open(easyEquitiesUrl);
                    } catch (error) {
                        // Cancelled
                    }
                }
            }

            // Check if upPercent has been passed
            if (config[stock].hasOwnProperty('purchase') && config[stock].hasOwnProperty('upPercent')) {
                if (closePrice > (config[stock].purchase + (config[stock].purchase * config[stock].upPercent / 100))) {
                    logString += ' WENT OVER UP PERCENTAGE!';
                    try {
                        await confirm(`${stock} went over up percentage!!! \n Proceed to Easy Equities URL?`);
                        
                        // Confirmed
                        open(easyEquitiesUrl);
                    } catch (error) {
                        // Cancelled
                    }
                }
            }

            // Check if downPercent has been passed
            if (config[stock].hasOwnProperty('purchase') && config[stock].hasOwnProperty('downPercent')) {
                if (closePrice < (config[stock].purchase - (config[stock].purchase * config[stock].downPercent / 100))) {
                    logString += ' WENT UNDER DOWN PERCENTAGE!';
                    try {
                        await confirm(`${stock} went under down percentage!!! \n Proceed to Easy Equities URL?`);
                        
                        // Confirmed
                        open(easyEquitiesUrl);
                    } catch (error) {
                        // Cancelled
                    }
                }
            }

            console.log(logString);
        });

    }
}, +config.interval.replace('min', '') * 60000);