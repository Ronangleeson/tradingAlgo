from yahoo_fin import stock_info as si
import time
from datetime import datetime
from matplotlib import pyplot as plt

def startTrading():
    # adjustable variables
    stock = "amd"
    sharesToBuy = 50
    buyingFrequency = 3               # in seconds
    totalRuntime = 1800               # in seconds
    startingCashReserve = 10000000


    # tracking variables
    cash = startingCashReserve
    sharesOwned = 0
    timeSpent = 0
    previousStockPrice = si.get_live_price(stock)
    valueOfInvestment = 0
    costOfInvestment = 0
    profit = 0
    openingPrice = si.get_live_price(stock)
    closingPrice = 0
    percentPriceChange = 0

    # graphing data
    stockPrices = []
    profitOrLoss = []


    while(timeSpent < totalRuntime):
        time.sleep(buyingFrequency)
        currentStockPrice = si.get_live_price(stock)
        # if share price decreases, sell
        if (currentStockPrice < previousStockPrice):
            cash += (sharesOwned * currentStockPrice)
            sharesOwned = 0

            # find profit & reset cost/value of investment
            profit = cash - startingCashReserve
            valueOfInvestment = 0
            costOfInvestment = 0

            timeSpent += buyingFrequency

        # else, continue to buy (if there is enough cash in reserve to do so)
        else:
            if (cash > (sharesToBuy * currentStockPrice)):
                cash = cash - (sharesToBuy * currentStockPrice)
                sharesOwned += sharesToBuy

                # find the cost, value & profit of investment
                valueOfInvestment = sharesOwned * currentStockPrice
                costOfInvestment = costOfInvestment + (sharesToBuy * currentStockPrice)
                profit = valueOfInvestment - costOfInvestment
                
                timeSpent += buyingFrequency
                
            else: 
                timeSpent += buyingFrequency
                continue

        stockPrices.append(currentStockPrice)
        profitOrLoss.append(profit)
        
        previousStockPrice = currentStockPrice
        
        # calculate current net income & shares owned
        print("Current Share Price: $" + str(currentStockPrice))
        print("Value of Investment: $" + str(valueOfInvestment))
        print("Cost of Posistion: $" + str(costOfInvestment))
        print("Profit: $" + str(profit))
        print("Shares Owned: " + str(sharesOwned))
        print("*****************\n")
        
    # close posistion (convert all remaining equity to cash)
    cash = cash + (sharesOwned * currentStockPrice)
    sharesOwned = 0
    timeSpent += buyingFrequency

    closingPrice = currentStockPrice
    percentPriceChange = ((closingPrice - openingPrice) / openingPrice) * 100

    # calculate final profit/loss
    print("Stock Price Change: " + str(percentPriceChange))
    print("Profit / Loss: $" + str(profit))
    return stockPrices, profitOrLoss

stockPrices, profits = startTrading()

plt.plot(stockPrices, label = "Stock Price")
plt.plot(profits, label = "Profit / Loss")
plt.legend()
plt.xlabel("time")
plt.ylabel("$")
plt.title("Stock Price vs. Model Performance")
plt.show()