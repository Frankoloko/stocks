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

let arrDailyProfits = {
    Monday: [],
    Tuesday: [],
    Wednesday: [],
    Thursday: [],
    Friday: []
}

// This function logs the average loss/gain per day of the week for all days supplied
module.exports = function LogDailyProfits() {
    let dayProfit = 0;

    for (stock in stocks) {
        stocks[stock].data.daily.forEach((element, index) => {
            // if (new Date(element.date) < new Date('2015')) return;

            dayProfit = Number(100 - (element.open / element.close * 100));
            if (dayProfit != 0) {
                switch (new Date(element.date).getDay()) {
                    case 1: // Monday
                        arrDailyProfits.Monday.push(dayProfit);
                        break
                    case 2: // Tuesday
                        arrDailyProfits.Tuesday.push(dayProfit);
                        break
                    case 3: // Wednesday
                        arrDailyProfits.Wednesday.push(dayProfit);
                        break
                    case 4: // Thursday
                        arrDailyProfits.Thursday.push(dayProfit);
                        break
                    case 5: // Friday
                        arrDailyProfits.Friday.push(dayProfit);
                        break
                }
            }
        });
    }

    for (day in arrDailyProfits) {
        let total = 0;
        for(var i = 0; i < arrDailyProfits[day].length; i++) {
            total += arrDailyProfits[day][i];
        }
        const avg = (total / arrDailyProfits[day].length).toFixed(2);
        console.log(day + ': ' + avg);
    }
};