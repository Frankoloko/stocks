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
        // Logs.push(`BUY | ${pElement.close} | ${pElement.date}`);
    }
    function Sell(pElement) {
        capital = Math.round(shares * pElement.close);
        // xArray.push(pElement.date);
        // yArray.push(capital);
        // Logs.push(`SELL | ${pElement.close} | ${pElement.date} | ${capital}`);
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

// This function logs the average loss/gain per day of the week for all days supplied
module.exports = function BuyMondaySellFriday() {
    let weeks = get_weeks()
    capital = 10000

    // Put data into weeks array
    for (stock in stocks) {
        stocks[stock].data.daily.forEach((stock_record, index) => {
            let stock_date = new Date(stock_record.date)
            // Just skip everything after Corona crash
            if (stock_date > new Date('2020-03-01')) return;
            
            // Add the Monday & Friday amounts
            weeks.forEach((week, index) => {
                if (index == 0) return

                // Check if this stock should be in this week
                if (stock_date >= weeks[index].date && stock_date < weeks[index + 1].date) {

                    // Check if the [stock] key exists, otherwise create it
                    if (!week[stock]) {
                        week[stock] = {}
                    }

                    // Check for the Monday date
                    if (!week[stock].hasOwnProperty('monday')) {
                        week[stock].monday = {
                            date: stock_date,
                            price: stock_record.close
                        }
                    } else {
                        if (week[stock].monday.date > stock_date) {
                            week[stock].monday = {
                                date: stock_date,
                                price: stock_record.close
                            }
                        }
                    }

                    // Check for the Friday date
                    if (!week[stock].hasOwnProperty('friday')) {
                        week[stock].friday = {
                            date: stock_date,
                            price: stock_record.close
                        }
                    } else {
                        if (week[stock].friday.date < stock_date) {
                            week[stock].friday = {
                                date: stock_date,
                                price: stock_record.close
                            }
                        }
                    }
                }
            })

            // Work out the weekly total/change
            weeks.forEach(week => {
                let highest_gain = 0
                let highest_gain_stock = ''

                for (const key in week) {
                    if (key != 'date' && key != 'highest_gain' && key != 'highest_gain_stock') {
                        let amount_changed = week[key].friday.price - week[key].monday.price
                        week[key].change = Math.round(amount_changed / week[key].friday.price * 100)
                        if (week[key].change > highest_gain) {
                            highest_gain_stock = key
                            highest_gain = week[key].change
                        }
                    }
                }

                week.highest_gain_stock = highest_gain_stock
                week.highest_gain = highest_gain
            })
        })
    }

    // Buy/Sell stocks
    weeks.forEach((element, index) => {
        if (index < 2) return

        let previous_week_highest_gainer = weeks[index - 1].highest_gain_stock
        if (previous_week_highest_gainer) {   
            // Buy
            let shares = capital / element[previous_week_highest_gainer].monday.price;
            // Sell
            capital = Math.round(shares * element[previous_week_highest_gainer].friday.price);
            console.log(capital)
        }
    });
};

function get_weeks() {
    let first_sunday = new Date('2002-01-06')

    let weeks = [{
        date: first_sunday
    }]

    today = new Date()
    current_date = new Date('2002-01-06')
    while (current_date < today) {
        weeks.push({
            date: new Date(current_date.setDate(current_date.getDate() + 7))
        })
    }
    
    return weeks
}