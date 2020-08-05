//region Setups
    const { plot } = require('nodeplotlib');
    const stocks = require('../data');
    const originalCapital = 10000;
    let xArray = null;
    let yArray = null;
    let Logs = [];
    let capital = null;
    let arrProfits = [];
    let buyPrice = 0;
    let parameters = '';

    function Buy(pElement) {
        shares = capital / pElement.close;
        capital = 0;
        Logs.push(`BUY | ${pElement.close} | ${pElement.date}`);
    }
    function Sell(pElement) {
        capital = Math.round(shares * pElement.close);
        xArray.push(pElement.date);
        yArray.push(capital);
        Logs.push(`SELL | ${pElement.close} | ${pElement.date} | ${capital}`);
    }
    function Reset() {
        xArray = [];
        yArray = [];
        capital = originalCapital;
        shares = 0;
        buyPrice = 0;
    }
    function Finish(pData) {
        if (capital == 0) Sell(pData[pData.length - 1]);
        arrProfits.push(yArray[yArray.length - 1]);
        return {x: xArray, y: yArray};
    }
    function LogAverageProfit() {
        let total = 0;
        arrProfits.forEach(element => {
            total += element;
        });
        const average = total / arrProfits.length;
        const profit = Math.round(average / originalCapital * 100);
        if (profit > 90) {
            console.log(parameters);
            console.log('TOTAL PROFIT: ' + profit + '%');
        }
        arrProfits = [];
    }
//endregion Setups

/**
 * This model checks if the time at X for the day is in a positive, if so, it will buy, and sell X hours later
 * @param pBuyHourOfDay - Buy at 1:10am - 2:11am - 3:12am - 4:1pm - 5:2pm - 6:3pm - 7:4pm
 * @param pUpOrDown - 'up' or 'down'
 * @example if (!this.usefultools.isValidResponse(url, response, ['utPrepareSQL_response', 'RESPONSE'])) return;
*/
module.exports = function IfUDAtXHoursAndSellAtXLossOrXProfit(pBuyHourOfDay, pUpOrDown, pDownSellPercentage, pUpSellPercentage) {
    parameters = pBuyHourOfDay + ':' + pUpOrDown + ':' + pDownSellPercentage + ':' + pUpSellPercentage;
    let dateOfHourChange = '2020-03-09';
    let plotArray = [];

    for (stock in stocks) {
        Reset();
        let dailyStartAmount = '';

        stocks[stock].data.hourly.forEach((element, index) => {
            // if (stock != 'mrp') return;
            // if (!element.date.includes('2020-01')) return;
            // if (!element.date.includes('2020-02')) return;
            // if (!element.date.includes('2020-03')) return;

            let firstDayHour = '';
            let buyHour = '';

            // Sell shares
            if (capital == 0) {
                // If higher than pUpSellPercentage
                if (buyPrice > element.close + (element.close * (pUpSellPercentage / 100))) {
                    Sell(stocks[stock].data.hourly[index]);
                    return;
                }
                // If lower than pDownSellPercentage
                if (buyPrice < element.close - (element.close * (pDownSellPercentage / 100))) {
                    Sell(stocks[stock].data.hourly[index]);
                    return;
                }
                return;
            }

            // Set first hour of day
            if (element.date.substr(0, 10) < dateOfHourChange) {
                // 02:00 - 09:00 days
                firstDayHour = '02';
                switch (pBuyHourOfDay) {
                    case 1:
                        buyHour = '03';
                        break;
                    case 2:
                        buyHour = '04';
                        break;
                    case 3:
                        buyHour = '05';
                        break;
                    case 4:
                        buyHour = '06';
                        break;
                    case 5:
                        buyHour = '07';
                        break;
                    case 6:
                        buyHour = '08';
                        break;
                    case 7:
                        buyHour = '09';
                        break;
                }
            } else {
                // 03:00 - 10:00 days
                firstDayHour = '03';
                switch (pBuyHourOfDay) {
                    case 1:
                        buyHour = '04';
                        break;
                    case 2:
                        buyHour = '05';
                        break;
                    case 3:
                        buyHour = '06';
                        break;
                    case 4:
                        buyHour = '07';
                        break;
                    case 5:
                        buyHour = '08';
                        break;
                    case 6:
                        buyHour = '09';
                        break;
                    case 7:
                        buyHour = '10';
                        break;
                }
            };

            // Get day's starting amount
            if (element.date.substr(11, 2) == firstDayHour) {
                dailyStartAmount = element.close;
                return;
            };

            // Check if the hour matches buyHour and up/down by that hour
            if (element.date.substr(11, 2) == buyHour) {
                let ifString = '';
                if (pUpOrDown == 'up') ifString = 'element.close > dailyStartAmount';
                if (pUpOrDown == 'down') ifString = 'element.close < dailyStartAmount';
                if (eval(ifString)) {
                    Logs.push('dailyStartAmount: ' + dailyStartAmount);
                    buyPrice = element.close;
                    Buy(stocks[stock].data.hourly[index]);
                }
            }
        });
    
        // console.log(Logs);
        plotArray.push({...Finish(stocks[stock].data.daily), name: `${stock} ${pUpOrDown}`});
    }
    
    plot(plotArray);
    LogAverageProfit();
    // console.log(Logs);
};