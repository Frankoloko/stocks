//region Setups
    const { plot } = require('nodeplotlib');
    const stocks = require('../data');
    const originalCapital = 10000;
    let xArray = null;
    let yArray = null;
    let Logs = [];
    let capital = null;
    let arrProfits = [];

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
        console.log('TOTAL PROFIT: ' + profit + '%');
        // Reset();
        arrProfits = [];
    }
//endregion Setups

/**
 * This model checks if the time at X for the day is in a positive, if so, it will buy, and sell X hours later
 * @param pBuyHourOfDay - Buy at 1:10am - 2:11am - 3:12am - 4:1pm - 5:2pm - 6:3pm - 7:4pm
 * @param pSellHourOfDay - Buy at 1:11am - 2:12am - 3:1pm - 4:2pm - 5:3pm - 6:4pm - 7:5pm
 * @param pUpOrDown - 'up' or 'down'
 * @example if (!this.usefultools.isValidResponse(url, response, ['utPrepareSQL_response', 'RESPONSE'])) return;
*/
module.exports = function IfUDAtXHoursBuyAndSellAfterXHours(pBuyHourOfDay, pSellHourOfDay, pUpOrDown) {
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
            let sellHour = '';

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
                switch (pSellHourOfDay) {
                    case 1:
                        sellHour = '03';
                        break;
                    case 2:
                        sellHour = '04';
                        break;
                    case 3:
                        sellHour = '05';
                        break;
                    case 4:
                        sellHour = '06';
                        break;
                    case 5:
                        sellHour = '07';
                        break;
                    case 6:
                        sellHour = '08';
                        break;
                    case 7:
                        sellHour = '09';
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
                switch (pSellHourOfDay) {
                    case 1:
                        sellHour = '04';
                        break;
                    case 2:
                        sellHour = '05';
                        break;
                    case 3:
                        sellHour = '06';
                        break;
                    case 4:
                        sellHour = '07';
                        break;
                    case 5:
                        sellHour = '08';
                        break;
                    case 6:
                        sellHour = '09';
                        break;
                    case 7:
                        sellHour = '10';
                        break;
                }
            };

            // Get day's starting amount
            if (element.date.substr(11, 2) == firstDayHour) {
                dailyStartAmount = element.close;
                return;
            };

            // Check if the hour matches buyHour
            if (element.date.substr(11, 2) == buyHour) {
                let ifString = '';
                if (pUpOrDown == 'up') ifString = 'element.close > dailyStartAmount';
                if (pUpOrDown == 'down') ifString = 'element.close < dailyStartAmount';
                if (eval(ifString)) {
                    Logs.push('dailyStartAmount: ' + dailyStartAmount);
                    Buy(stocks[stock].data.hourly[index]);
                }
            }

            // Check if the hour matches sellHour
            if (element.date.substr(11, 2) == sellHour) {
                if (capital == 0) Sell(stocks[stock].data.hourly[index]);
            };
        });
    
        // console.log(Logs);
        plotArray.push({...Finish(stocks[stock].data.daily), name: `${stock} ${pUpOrDown}`});
    }
    
    plot(plotArray);
    LogAverageProfit();
};