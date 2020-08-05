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
        arrProfits = [];
    }
//endregion Setups

// This model looks if the previous consecutive X days were higher/lower than today, if so, it will buy today, and sell the next day

module.exports = function BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay(pTimeframe, pDays, pLowerOrHigher) {
    let plotArray = [];

    for (stock in stocks) {
        Reset();
        stocks[stock].data[pTimeframe].forEach((element, index) => {
            element = element.close;
            if (index < pDays) return;
    
            // Sell shares
            if (capital == 0) {
                Sell(stocks[stock].data[pTimeframe][index]);
                return;
            }
    
            let ifString = '';
    
            if (pLowerOrHigher == 'lower') {
                ifString = 'element < stocks[stock].data[pTimeframe][index - 1].close';
                for (let x = 0; x < pDays; x++) {
                    if (x == 0) continue;
                    ifString += ` && stocks[stock].data[pTimeframe][index - ${x}].close < stocks[stock].data[pTimeframe][index - ${x + 1}].close`
                }
            }
    
            if (pLowerOrHigher == 'higher') {
                ifString = 'element > stocks[stock].data[pTimeframe][index - 1].close';
                for (let x = 0; x < pDays; x++) {
                    if (x == 0) continue;
                    ifString += ` && stocks[stock].data[pTimeframe][index - ${x}].close > stocks[stock].data[pTimeframe][index - ${x + 1}].close`
                }
            }
    
            if (eval(ifString)) {
                Buy(stocks[stock].data[pTimeframe][index]);
            }
        });
    
        plotArray.push({...Finish(stocks[stock].data[pTimeframe]), name: `${stock} ${pTimeframe} ${pLowerOrHigher} ${pDays}days`});
    }

    plot(plotArray);
    LogAverageProfit();
};