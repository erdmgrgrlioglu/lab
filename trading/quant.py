import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

start_time='2020-01-01' #editable
end_time='2025-01-01' #editable
animation=False #editable

## strategy
buyAfterPercentage=2 #editable
sellAfterPercentage=2 #editable
buyAfterIteration=20 #editable
###

balance=1000 #editable
position=0

dates, values = [], []
df = pd.DataFrame(pd.read_csv("data/data.csv")) ## historic data from FED
df['Date'] = pd.to_datetime(df['Date'])

buyMarketValue=0
buyPoints = [], [] # [date], [value]
def buy(value, index):
    global balance
    global position
    position = balance/value # +(-0.15/value) buying operation cost
    balance = 0
    
    global buyMarketValue
    buyMarketValue = value
    
    buyPoints[0].append(df.iloc[index][0])
    buyPoints[1].append(df.iloc[index][1])
    print(f"Bought on Value: {value}, Your Position: {position}, Balance: {value*position}, Date:{df.iloc[index][0]}")

lastSellMarketValue=0
sellPoints = [], [] # [date], [value]
def sell(value, index):
    global balance
    global position
    balance = value*position # -0.15 selling operation cost
    position = 0

    global lastSellMarketValue
    lastSellMarketValue = value

    sellPoints[0].append(df.iloc[index][0])
    sellPoints[1].append(df.iloc[index][1])
    print(f"Sold on Value: {value}, Your Position: {position}, Balance: {balance}, Date:{df.iloc[index][0]}")

lastSellindex=0
strategyPoints = [], []
def strategy(value, index):
    global lastSellindex
    if position != 0:
        if(value-buyMarketValue)/value*100 > sellAfterPercentage: #percent
            sell(value,index)
            lastSellindex=index
    else:
        if index-lastSellindex == buyAfterIteration or (lastSellMarketValue-value)/value*100 > buyAfterPercentage: #percent
            buy(value,index)

initialPoints= [],[]
startPosition=0
iteration=0
def calac_at_index(index):
    marketValue = df.iloc[index][1]
    date = df.iloc[index][0].date()

    # iteration
    global iteration
    global startPosition
    if iteration == 0: 
        startPosition = balance/marketValue
        buy(marketValue,index)
    else: strategy(marketValue,index) # strategy
    iteration += 1
    
    # logs
    if position != 0:
        print(f"Date: {date}, Value: {marketValue}, Balance: {marketValue*position}")
        strategyPoints[1].append(marketValue*position)
    else:
        print(f"Date: {date}, Value: {marketValue}, Balance: {balance}")
        strategyPoints[1].append(balance)
    initialPoints[0].append(df.iloc[index][0]) # no strategy: never sell
    initialPoints[1].append(marketValue*startPosition)
    strategyPoints[0].append(df.iloc[index][0])
    dates.append(df.iloc[index][0])
    values.append(df.iloc[index][1])
    
def plot():
    plt.cla()
    plt.plot(dates,values)
    plt.scatter(buyPoints[0], buyPoints[1], color='green', zorder=5)
    plt.scatter(sellPoints[0], sellPoints[1], color='red', zorder=5)
    plt.plot(initialPoints[0], initialPoints[1], color='purple')
    plt.plot(strategyPoints[0], strategyPoints[1], color='orange')


## main
for row in df.iterrows():
    if  datetime.fromisoformat(start_time) <= row[1][0] and row[1][0] <= datetime.fromisoformat(end_time):
        calac_at_index(row[0])
        if animation: 
            plot()
            plt.draw()
            plt.pause(0.1)
plot()
plt.show()
