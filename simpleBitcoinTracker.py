import cryptocompare
import time
from datetime import datetime
from matplotlib import pyplot as plt

def startTrading():
    # adjustable variables
    ticker = "BTC"
    coinsToBuy = 5
    buyingFrequency = 3               # in seconds
    totalRuntime = 3600              # in seconds
    startingCashReserve = 10000000


    # tracking variables
    cash = startingCashReserve
    coinsOwned = 0
    timeSpent = 0
    previousPrice = cryptocompare.get_price(ticker, curr="USD", full = False)['BTC']['USD']
    valueOfInvestment = 0
    costOfInvestment = 0
    unrealizedGains = 0
    profit = 0
    openingPrice = cryptocompare.get_price(ticker, curr="USD", full = False)['BTC']['USD']
    closingPrice = 0
    startTime = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    # graphing data
    prices = []
    profitOrLoss = []
    percentPriceChange = []

    while(timeSpent < totalRuntime):
        time.sleep(buyingFrequency)
        currentPrice = cryptocompare.get_price(ticker, curr="USD", full = False)['BTC']['USD']
        
        # if share price increases or remains the same, buy more
        # only calculated profits if buying, otherwise record as unrealized gains
        if (currentPrice >= previousPrice):
            cash -= coinsToBuy * currentPrice
            coinsOwned += coinsToBuy
            costOfInvestment += coinsToBuy * currentPrice
            valueOfInvestment = coinsOwned * currentPrice
            unrealizedGains += valueOfInvestment - costOfInvestment
            # profit += valueOfInvestment - costOfInvestment

            timeSpent += buyingFrequency

        # if share price decreases, sell all shares
        # convert unrealized gains into profits / loss
        if (currentPrice < previousPrice):

            valueOfInvestment = coinsOwned * currentPrice
            profit += valueOfInvestment - costOfInvestment
            
            # reset tracking variables 
            unrealizedGains = 0
            costOfInvestment = 0
            valueOfInvestment = 0
            coinsOwned = 0


            timeSpent += buyingFrequency
    

        prices.append(currentPrice)
        profitOrLoss.append(profit)
        percentPriceChange.append(((currentPrice - previousPrice) / previousPrice) * 100)

        previousPrice = currentPrice
        
        # calculate current net income & shares owned
        print("Current Price: $" + str(currentPrice))
        print("Value of Investment: $" + str(valueOfInvestment))
        print("Cost of Posistion: $" + str(costOfInvestment))
        print("Profit: $" + str(profit))
        print("Coins Owned: " + str(coinsOwned))
        print("*****************\n")
        
    # close posistion at end of trading
    cash = cash + (coinsOwned * currentPrice)
    coinsOwned = 0
    timeSpent += buyingFrequency

    closingPrice = currentPrice
    closingTime = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    totalPercentPriceChange = (((closingPrice - openingPrice) / openingPrice) * 100)
    truncatedTotalPercentPriceChange = '%.4f'%(totalPercentPriceChange)

    # calculate final profit/loss
    print("Opening Price: $" + str(openingPrice))
    print("Closing Price: $" + str(closingPrice))
    print("Stock Price Change: " + str(totalPercentPriceChange))
    print("Profit / Loss: $" + str(profit))


    # write results to appropriate txt file
    tradeDetails = [startTime, closingTime, ticker, openingPrice, closingPrice, truncatedTotalPercentPriceChange, buyingFrequency, totalRuntime, coinsToBuy, profit]
    writeTradeDetails(tradeDetails)
    writeGraphingDetails(prices, profitOrLoss, percentPriceChange)


    return prices, profitOrLoss, percentPriceChange

    

def writeTradeDetails(tradeDetails):
    f = open("bitcoinTrades.txt", "a")
    for i in range(len(tradeDetails)):
        f.write(str(tradeDetails[i]))
        if (i + 1 != len(tradeDetails)):
            f.write(", ")
    f.write("\n")
    f.close()

def writeGraphingDetails(prices, profitOrLoss, percentPriceChange):
    f = open("graphingData.txt", "a")
    # write each array on one line with a header
    f.write("Prices: ")
    for i in range(len(prices)):
        f.write(str(prices[i]))
        if (i + 1 != len(prices)):
            f.write(", ")
    f.write("\n")

    f.write("Profit: ")
    for i in range(len(profitOrLoss)):
        f.write(str(profitOrLoss[i]))
        if (i + 1 != len(profitOrLoss)):
            f.write(", ")
    f.write("\n")

    f.write("Percent Price Change: ")
    for i in range(len(percentPriceChange)):
        f.write(str(percentPriceChange[i]))
        if (i + 1 != len(percentPriceChange)):
            f.write(", ")
    f.write("\n")

    # write new line to seperate trade
    # then close write
    f.write("\n")
    f.close()

prices, profits, percentPriceChange = startTrading()

plt.plot(prices, label = "Price")
plt.plot(profits, label = "Profit / Loss")
plt.plot(percentPriceChange, label = "Percent Price Change")
plt.legend()
plt.xlabel("time")
plt.ylabel("$")
plt.title("Stock Price vs. Model Performance")
plt.show()