from datetime import datetime, timedelta


H = 5                                                                                       #holding time in seconds after making the opposite trade
W = 2                                                                                       #waiting time in seconds before making another trade
D = 1                                                                                       #precent in change of stock price

data = ['timestap: 2000-01-01 06:00:01.123, price: 100.45', 'timestap: 2000-01-01 06:00:05.561, price: 100.21', 'timestap: 2000-01-01 06:00:08.468, price: 102.68', 'timestap: 2000-01-01 06:00:12.359, price: 105.97', 'timestap: 2000-01-01 06:00:13.497, price: 103.85', 'timestap: 2000-01-01 06:00:16.525, price: 101.73', 'timestap: 2000-01-01 06:00:20.965, price: 101.67']
data_2 = ['timestap: 2000-01-01 06:00:01.123, price: 121.45', 'timestap: 2000-01-01 06:00:04.561, price: 120.21', 'timestap: 2000-01-01 06:00:08.468, price: 100.68', 'timestap: 2000-01-01 06:00:09.359, price: 95.97', 'timestap: 2000-01-01 06:00:11.497, price: 99.85', 'timestap: 2000-01-01 06:00:14.525, price: 150.73', 'timestap: 2000-01-01 06:00:17.965, price: 200.67']
          
          
def pnl(H,W,D, data):
    
    all_prices = []
    all_timestamps = []
    for i in data:                                                                          #splitting the dates and prices into seperate lists
        timestamp, price = i.split(',')
        timestamps = timestamp.strip('timestamp: ')
        prices = price.split('price: ')[1]
        
        all_timestamps.append(timestamps)
        all_prices.append(float(prices))


    dates = []
    for j in range(len(all_timestamps)):                                                    #giving the dates datetime format with ms and appending them into a new list
        date = all_timestamps[j][0:10]
        datesFormat = [date[0:4], date[5:7], date[8:10]]
        times = all_timestamps[j][11:23]
        YYYY = date[0:4]
        MTH = date[5:7]
        DD = date[8:10]
        HH = times[0:2]
        MM = times[3:5] 
        SS = times[6:8] 
        MS = times[9:12]
                        
        date_with_ms = datetime(int(YYYY), int(MTH), int(DD), int(HH), int(MM), int(SS), int(MS) * 1000)
        dates.append(date_with_ms)
        
        

    pnl = 0                                                                                 #initializing profil and loss as 0  
    last_trade_time = 0                                                                     #initializing last trade time as 0 

    #Keep in mind we are at time dates[i+1] in this loop, because we compare with the previous time

    for i in range(len(dates) - 1):                                                    

        d = ((all_prices[i+1] - all_prices[i]) / all_prices[i+1]) * 100                     #calculating the precentage in change of the stock price compared to the previous timestamp
        
        
        if d >= D: 
            #We should buy a stock here
            if last_trade_time == 0:                                                        #distinguish the cases where we have a last_trade_time because we have to wait W seconds before the next trade
                pnl = pnl - all_prices[i+1]                                                 #update pnl by buying a stock
                last_trade_time = dates[i+1]                                                #update last_trade_time to current time
                
                for j in range(len(dates)):                                                 #we sell the stock after holding it for H seconds here
                    H_secs = (dates[j] - dates[i+1]).total_seconds()
                    if j > i and H_secs > H:
                        pnl = pnl + all_prices[j-1]
                        break
                    elif H_secs == (dates[len(dates)- 1] - dates[i+1]).total_seconds():     #this is to ensure that if we waited the maximal amount of seconds and it did not pass H seconds we sell anyway, because it is the last possible price in the market
                            pnl = pnl + all_prices[len(all_prices) - 1]
                            break
                    
            elif last_trade_time != 0:                                                      #case where we have a last_trade_time so we check if we waited W seconds and do the same actions (buy and sell after holding for H seconds)
                W_secs = (dates[i+1] - last_trade_time).total_seconds()
                if W_secs >= W:
                    pnl = pnl - all_prices[i+1]
                    last_trade_time = dates[i+1]
                    for j in range(len(dates)):
                        H_secs = (dates[j] - dates[i+1]).total_seconds()
                        if j > i and H_secs > H:
                            pnl = pnl + all_prices[j-1]
                            break
                        elif H_secs == (dates[len(dates)- 1] - dates[i+1]).total_seconds():
                            pnl = pnl + all_prices[len(all_prices) - 1]
                            break
            
                            
        if d <= -D:                                                     
            #We should sell a stock here
            if last_trade_time == 0:                                                        #same principles, distinguish the cases where we have a last_trade_time because we have to wait W seconds before the next trade
                pnl = pnl + all_prices[i+1]                                                 #update pnl by selling a stock
                last_trade_time = dates[i+1]                                                #update last_trade_time to current time
                for j in range(len(dates)):                                                 #in this loop we buy the stock again after H seconds
                    H_secs = (dates[j] - dates[i+1]).total_seconds()
                    if j > i and H_secs > H: 
                        pnl = pnl - all_prices[j-1]
                        break 
                    elif H_secs == (dates[len(dates)- 1] - dates[i+1]).total_seconds():     #this elif statement is there to check if we can wait more than H seconds otherwise we sell at the final time
                            pnl = pnl - all_prices[len(all_prices)- 1]
                            break 
            
            elif last_trade_time != 0:                                                      #this is the case where we have a last_trade_time so we have to check if we waited W seconds before making a trade
                W_secs = (dates[i+1] - last_trade_time).total_seconds()
                if W_secs >= W:
                    pnl = pnl + all_prices[i+1]
                    last_trade_time = dates[i+1]
                    for j in range(len(dates)):
                        H_secs = (dates[j] - dates[i+1]).total_seconds()
                        if j >i and H_secs > H:
                            pnl = pnl - all_prices[j-1]
                            break 
                        elif H_secs == (dates[len(dates)- 1] - dates[i+1]).total_seconds():
                            pnl = pnl - all_prices[len(all_prices)- 1]
                            break 

    return round(pnl,2)

print('total pnl is:',pnl(H,W,D,data))
