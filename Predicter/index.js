//region Imports
const BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay = require('./models/BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay');
const BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent = require('./models/BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent');
const IfUDAtXHoursBuyAndSellAfterXHours = require('./models/IfUDAtXHoursBuyAndSellAfterXHour');
const IfUDAtXHoursAndSellAtXLossOrXProfit = require('./models/IfUDAtXHoursAndSellAtXLossOrXProfit');
const BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit = require('./models/BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit');
const LogDailyProfits = require('./models/LogDailyProfits');
const LogHourlyProfits = require('./models/LogHourlyProfits');
const BuyMondaySellFriday = require('./models/BuyMondaySellFriday');
//endregion

//region BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay
    // BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay('daily', 1, 'higher'); // 326% (11%pa)
    // BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay('daily', 1, 'lower');
    // BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay('daily', 2, 'higher');
    // BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay('daily', 2, 'lower');
    // BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay('daily', 3, 'higher');
    // BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay('daily', 3, 'lower');
    // BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay('daily', 4, 'higher');
    // BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay('daily', 4, 'lower');
    // BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay('daily', 5, 'higher');
    // BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay('daily', 5, 'lower');
    // console.log('======================')
    // BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay('hourly', 1, 'higher');
    // BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay('hourly', 1, 'lower');
    // BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay('hourly', 2, 'higher');
    // BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay('hourly', 2, 'lower');
    // BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay('hourly', 3, 'higher');
    // BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay('hourly', 3, 'lower');
    // BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay('hourly', 4, 'higher');
    // BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay('hourly', 4, 'lower');
    // BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay('hourly', 5, 'higher');
    // BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay('hourly', 5, 'lower');
//endregion BuyIfPreviousDayWasHigherOrLowerAndSellTheNextDay

//region BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent('daily', 1, 'climbed');
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent('daily', 1, 'dropped'); // 223% (6%pa)
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent('daily', 2, 'climbed');
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent('daily', 2, 'dropped');
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent('daily', 3, 'climbed');
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent('daily', 3, 'dropped');
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent('daily', 4, 'climbed');
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent('daily', 4, 'dropped');
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent('daily', 5, 'climbed');
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent('daily', 5, 'dropped');
    // console.log('======================')
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent('hourly', 1, 'climbed'); // 107%
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent('hourly', 1, 'dropped');
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent('hourly', 2, 'climbed'); // 105%
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent('hourly', 2, 'dropped');
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent('hourly', 3, 'climbed'); // 106%
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent('hourly', 3, 'dropped');
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent('hourly', 4, 'climbed'); // 105%
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent('hourly', 4, 'dropped');
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent('hourly', 5, 'climbed');
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent('hourly', 5, 'dropped');
//endregion BuyIfPreviousDayClimbedOrDroppedMoreThanXPercent

//region IfUDAtXHoursBuyAndSellAfterXHours
    // [1, 2, 3, 4, 5, 6, 7].forEach(element1 => {
    //     [1, 2, 3, 4, 5, 6, 7].forEach(element2 => {
    //         IfUDAtXHoursBuyAndSellAfterXHours(element1, element2, 'down');
    //         IfUDAtXHoursBuyAndSellAfterXHours(element1, element2, 'up');
    //     });
    // });

    // IfUDAtXHoursBuyAndSellAfterXHours(4, 7, 'up'); // 105%
//endregion IfUDAtXHoursBuyAndSellAfterXHours

//region BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 1, 'climbed', 20, 10);
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 1, 'dropped', 20, 10);
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 2, 'climbed', 20, 10);
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 2, 'dropped', 20, 10);
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 3, 'climbed', 20, 10);
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 3, 'dropped', 20, 10);
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 4, 'climbed', 20, 10);
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 4, 'dropped', 20, 10);
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 5, 'climbed', 20, 10);
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 5, 'dropped', 20, 10);

    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('hourly', 1, 'climbed', 20, 10);
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('hourly', 1, 'dropped', 20, 10);
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('hourly', 2, 'climbed', 20, 10);
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('hourly', 2, 'dropped', 20, 10);
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('hourly', 3, 'climbed', 20, 10);
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('hourly', 3, 'dropped', 20, 10);
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('hourly', 4, 'climbed', 20, 10);
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('hourly', 4, 'dropped', 20, 10);
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('hourly', 5, 'climbed', 20, 10);
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('hourly', 5, 'dropped', 20, 10);

    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 1, 'climbed', 20, 10); // 163
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 3, 'climbed', 10, 5); // 173
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 2, 'climbed', 5, 5); // 147
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 1, 'dropped', 20, 10);

    // [1, 2, 3, 4, 5].forEach(element1 => {
    //     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20].forEach(element2 => {
    //         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20].forEach(element3 => {
    //             BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('hourly', element1, 'climbed', element2, element3);
    //         });
    //     });
    // });

    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 1, 'dropped', 6, 14); // 1211%
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 1, 'dropped', 6, 20); // 1217%
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 1, 'dropped', 8, 20); // 1242%
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 1, 'dropped', 13, 20); // 1284%
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 1, 'dropped', 14, 20); // 1288%
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 2, 'dropped', 2, 20); // 1213%
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 2, 'dropped', 14, 18); // 1328%
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 2, 'dropped', 14, 19); // 1223%

    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('hourly', 3, 'climbed', 2, 1); // 109%
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('hourly', 4, 'climbed', 10, 2); // 109%
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('hourly', 4, 'climbed', 10, 3); // 108%

    // Without Capitec:
    // BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit('daily', 2, 'dropped', 14, 18); // 1328%
    // 2002 NaN
    // 2003 NaN
    // 2004 NaN
    // 2005 NaN
    // 2006 NaN
    // 2007 NaN
    // 2008 NaN
    // 2009 120%
    // 2010 NaN
    // 2011 NaN
    // 2012 NaN
    // 2013 NaN
    // 2014 117%
    // 2015 100%
    // 2016 NaN
    // 2017 NaN
    // 2018 90%
    // 2019 98%
 
//endregion BuyIfPreviousDayClimbedOrDroppedMoreThanXPercentAndSellAtXLossOrXProfit

//region IfUDAtXHoursAndSellAtXLossOrXProfit
    // [1, 2, 3, 4, 5, 6, 7].forEach(element1 => {
    //     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20].forEach(element2 => {
    //         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20].forEach(element3 => {
    //             IfUDAtXHoursAndSellAtXLossOrXProfit(element1, 'up', element2, element3);
    //         });
    //     });
    // });

    // IfUDAtXHoursAndSellAtXLossOrXProfit(2, 'down', 10, 5);
    // IfUDAtXHoursAndSellAtXLossOrXProfit(4, 'up', 2, 1);
//endregion

//region LogDailyProfits
    // LogDailyProfits();
//endregion

//region LogHourlyProfits
    // LogHourlyProfits();
//endregion

//region BuyMondaySellFriday
    BuyMondaySellFriday();
//endregion

// TRY THESE
    // When XSMA/EMA crosses XSMA/EMA
    // Look at running trail stop losses
    // When price is above XSMA/XEMA, buy and sell at end of day
    // Hold shares until you can sell for a X% profit. If you loose a whole stack then that is fine
    // Hold shares until you hit +2% or -1% (just as a ratio example)
    // If XSMA/EMA is positive (uphill) then invest