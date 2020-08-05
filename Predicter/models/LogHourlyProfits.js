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

let arrStartOfHour = {
    'h10': [],
    'h11': [],
    'h12': [],
    'h1': [],
    'h2': [],
    'h3': [],
    'h4': [],
    'h5': []
};

// This function logs the average loss/gain per day of the week for all days supplied
module.exports = function LogHourlyProfits() {
    let dateOfHourChange = '2020-03-09'; // if (element.date.substr(0, 10) < dateOfHourChange)
    let dayOpenPrice = null;
    let hourProfit = null;
    let hourCorrector = 0;
    let hourIndicator = null;

    for (stock in stocks) {
        stocks[stock].data.hourly.forEach((element, index) => {
            if (new Date(element.date) > new Date('2020-03-01')) return;
            
            // Get the first hour of the day (because it changed at a certain date)
            if (element.date.substr(0, 10) < dateOfHourChange) {
                firstHour = '02:00:00';
                hourCorrector = 1;
            } else {
                firstHour = '03:00:00';
                hourCorrector = 0;
            }

            // Get the day's open price
            if (element.date.indexOf(firstHour) > -1) {
                dayOpenPrice = element.open;
            };

            // Get hour's profit(%) based on the hour close & day's open price
            hourProfit = Number(100 - (dayOpenPrice / element.close * 100));

            // Push the result to the correct hour array
            hourIndicator = +element.date.substr(12, 1) + hourCorrector;
            if (hourIndicator == 3) arrStartOfHour['h10'].push(hourProfit);
            if (hourIndicator == 4) arrStartOfHour['h11'].push(hourProfit);
            if (hourIndicator == 5) arrStartOfHour['h12'].push(hourProfit);
            if (hourIndicator == 6) arrStartOfHour['h1'].push(hourProfit);
            if (hourIndicator == 7) arrStartOfHour['h2'].push(hourProfit);
            if (hourIndicator == 8) arrStartOfHour['h3'].push(hourProfit);
            if (hourIndicator == 9) arrStartOfHour['h4'].push(hourProfit);
            if (hourIndicator == 0) arrStartOfHour['h5'].push(hourProfit);
        });
    }

    for (hour in arrStartOfHour) {
        let total = 0;
        for(var i = 0; i < arrStartOfHour[hour].length; i++) {
            total += arrStartOfHour[hour][i];
        }
        const avg = (total / arrStartOfHour[hour].length).toFixed(2);
        console.log(hour + ':\t' + avg);
    }
};