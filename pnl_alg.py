from datetime import datetime


H = 5
W = 2
D = 1

data = ['timestap: 2000-01-01 06:00:01.123, price: 100.45', 'timestap: 2000-01-01 06:00:05.561, price: 100.21', 'timestap: 2000-01-01 06:00:08.468, price: 102.68', 'timestap: 2000-01-01 06:00:12.359, price: 105.97', 'timestap: 2000-01-01 06:00:13.497, price: 103.85', 'timestap: 2000-01-01 06:00:16.525, price: 101.73', 'timestap: 2000-01-01 06:00:20.965, price: 101.67']
data_2 = ['timestap: 2000-01-01 06:00:01.123, price: 121.45', 'timestap: 2000-01-01 06:00:04.561, price: 120.21', 'timestap: 2000-01-01 06:00:08.468, price: 100.68', 'timestap: 2000-01-01 06:00:09.359, price: 95.97', 'timestap: 2000-01-01 06:00:11.497, price: 99.85', 'timestap: 2000-01-01 06:00:14.525, price: 150.73', 'timestap: 2000-01-01 06:00:17.965, price: 200.67']



def total_pnl(H,W,D,data):
    times = []    
    all_prices = []
    for i in data:
        timestamp = i.split(', ')[0]
        times.append(timestamp)
    
        price = i.split(', ')[1]
        all_prices.append(price)
    

    prices = []
    for price in all_prices:
        new_price = float(price.strip('price: '))
        prices.append(new_price)


    all_times = []
    for timestamp in times:
        new_time = timestamp.strip('timestap: ')
        all_times.append(new_time)
    

    dates = []
    for date in all_times:
        YYYY = int(date[0:4])
        MNTH = int(date[5:7])
        DD = int(date[8:10])
        HH = int(date[11:13])
        MM = int(date[14:16])
        SS = int(date[17:19])
        MS = int(date[20:23])
        date_with_ms = datetime(YYYY, MNTH, DD, HH, MM, SS, MS*1000)
        dates.append(date_with_ms)
    

    pnl = 0
    last_trade_time = 0
    
    for i in range(len(dates) - 1):
    #remember we are at timestamp i+1 as we compare with the previous timestamp
    
        d = ((prices[i+1] - prices[i])/(prices[i])) * 100
        
        if d >= D:
        #we should buy a stock here
            if last_trade_time == 0:
                pnl = pnl - prices[i+1]
                last_trade_time = dates[i+1]
                for j in range(len(dates)):
                    H_secs = (dates[j] - dates[i+1]).total_seconds()
                    if j > i and H_secs >= H:
                        pnl = pnl + prices[j-1]
                        break
                    elif H_secs == (dates[len(dates) -1] - dates[i+1]).total_seconds():
                            pnl = pnl + prices[len(prices) - 1]
                            break
            
            elif last_trade_time != 0:
                W_secs = (dates[i+1] - last_trade_time).total_seconds()
                if W_secs >= W:
                    pnl = pnl - prices[i+1]
                    last_trade_time = dates[i+1]
                    for j in range(len(dates)):
                        H_secs = (dates[j] - dates[i+1]).total_seconds()
                        if j > i and H_secs >= H:
                            pnl = pnl + prices[j-1]
                            break
                        elif H_secs == (dates[len(dates) -1] - dates[i+1]).total_seconds():
                            pnl = pnl + prices[len(prices) - 1]
                            break
        
        
        if d <= -D: 
            if last_trade_time == 0:
                pnl = pnl + prices[i+1]
                last_trade_time = dates[i+1]
                for j in range(len(dates)):
                    H_secs = (dates[j] - dates[i+1]).total_seconds()
                    if j > i and H_secs >= H:
                        pnl = pnl - prices[j-1]
                        break
                    elif H_secs == (dates[len(dates) -1] - dates[i+1]).total_seconds():
                        pnl = pnl - prices[len(prices) - 1]
                        break
            
            elif last_trade_time != 0:
                W_secs = (dates[i+1] - last_trade_time).total_seconds()
                if W_secs >= W:
                    pnl = pnl + prices[i+1]
                    last_trade_time = dates[i+1]
                    for j in range(len(dates)):
                        H_secs = (dates[j] - dates[i+1]).total_seconds()
                        if j > i and H_secs >= H:
                            pnl = pnl - prices[j-1]
                            break
                        elif H_secs == (dates[len(dates) -1] - dates[i+1]).total_seconds():
                            pnl = pnl - prices[len(prices) - 1]
                            break
        
    return round(pnl,2)


print('total pnl:' , total_pnl(H,W,D,data_2))
