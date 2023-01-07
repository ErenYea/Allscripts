import requests
import time
import pymysql
import logging
import os
import datetime


# os.chdir(r'C:\Users\Administrator\Desktop\DB2')
logging.basicConfig(filename="france.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.debug("This is new debug info ")

equity_comp = ['BTC', 'ETH']

for a in equity_comp:
    try:
        url = f'https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol={a}&market=USD&interval=30min&apikey=PJEBBJNC5XGIIA9J&outputsize=compact'
        r = requests.get(url)
        data = r.json()

        datas = []
        for i, j in data["Time Series Crypto (30min)"].items():
            timee, opan, high, low, close, vol = i, j['1. open'], j[
                '2. high'], j['3. low'], j['4. close'], j['5. volume']
            datas.append([a, timee, opan, high, low, close, vol])

        datas = datas[:96]
        print(datas)
        print('------------------------------------------------------------------------------------------')
        print()
        connection = pymysql.connect(host='database1-instance-1.crydakzjfkez.ap-southeast-2.rds.amazonaws.com',
                                     user='admin',
                                     password='sadwyr-sobbun-6tuRzo',
                                     )
        cursor = connection.cursor()
        cursor.execute('use Script')
        for i in range(1, len(datas)):
            x = datetime.datetime.strptime(datas[i][1], '%Y-%m-%d %H:%M:%S')
            query = f'''INSERT INTO Currencies (`Name`, `Date`, `Time`, `Open`,`High`, `Low`, `Close`,`Volume`, `Currency`)
        VALUES ('{datas[i][0]}','{x.date()}','{x.time()}','{datas[i][2]}','{datas[i][3]}','{datas[i][4]}','{datas[i][5]}','{datas[i][6]}','USD');'''
        #     print(query)
            cursor.execute(query)
            cursor.connection.commit()
    except:
        continue
time.sleep(60)


equity_comp = ['BHP', 'RIO', 'GOLD', 'FCX',
               'VALE', 'ARKK', 'GS', 'AAPL', 'GOOG']
for a in equity_comp:
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={a}&interval=30min&apikey=PJEBBJNC5XGIIA9J&outputsize=compact'
    r = requests.get(url)
    data = r.json()

    datas = []
    time.sleep(12)
    for i, j in data["Time Series (30min)"].items():
        timee, opan, high, low, close, vol = i, j['1. open'], j[
            '2. high'], j['3. low'], j['4. close'], j['5. volume']
        datas.append([a, timee, opan, high, low, close, vol])

    datas = datas[:96]
    print(datas)
    print('------------------------------------------------------------------------------------------')
    print()
    connection = pymysql.connect(host='database1-instance-1.crydakzjfkez.ap-southeast-2.rds.amazonaws.com',
                                 user='admin',
                                 password='sadwyr-sobbun-6tuRzo',
                                 )
    cursor = connection.cursor()
    cursor.execute('use Script')
    all_dates = list(set(list(map(lambda x: x[1].split(' ')[0], datas))))
    all_dates_data = {}
    for dat in all_dates:
        x = datetime.datetime.strptime(dat, '%Y-%m-%d')
        date_inside_query = f'{x.date().year}-{x.date().month}-{x.date().day}'
        query = f'''SELECT * from ForeignEquities WHERE DATE(Date)="{date_inside_query}" AND Name="{a}";'''
        cursor.execute(query)
        da = cursor.fetchall()
        all_dates_data[dat] = list(da)

    def checkduplication(x):
        if x[4] == first[4] and x[5] == first[5] and x[6] == first[6] and x[7] == first[7] and x[8] == first[8]:
            return True
        else:
            return False
    for i in range(1, len(datas)):
        x = datetime.datetime.strptime(datas[i][1], '%Y-%m-%d %H:%M:%S')
        date_inside_query = f'{x.date().year}-{x.date().month if len(str(x.date().month))>1 else "0"+str(x.date().month)}-{x.date().day if len(str(x.date().day))>1 else "0"+str(x.date().day)}'
        first = datas[i]
        if len(list(filter(checkduplication, all_dates_data[date_inside_query]))) > 0:
            continue
        query = f'''INSERT INTO ForeignEquities (`Name`, `Date`,`Time`, `Open`,`High`, `Low`, `Close`,`Volume`, `Currency`)
    VALUES ('{datas[i][0]}','{x.date()}','{x.time()}','{datas[i][2]}','{datas[i][3]}','{datas[i][4]}','{datas[i][5]}','{datas[i][6]}','USD');'''
    #     print(query)
        cursor.execute(query)
        cursor.connection.commit()
time.sleep(60)
equity_comp = ['USD', 'EUR', 'GBP', 'NZD', 'CNY']
for a in equity_comp:
    try:
        url = f'https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol={a}&to_symbol=AUD&interval=30min&apikey=PJEBBJNC5XGIIA9J&outputsize=compact'
        r = requests.get(url)
        data = r.json()

        datas = []
        for i, j in data["Time Series FX (30min)"].items():
            timee, opan, high, low, close, vol = i, j['1. open'], j['2. high'], j['3. low'], j['4. close'], '-'
            datas.append([a, timee, opan, high, low, close, vol])

        datas = datas[:96]
        print(datas)
        print('------------------------------------------------------------------------------------------')
        print()
        connection = pymysql.connect(host='database1-instance-1.crydakzjfkez.ap-southeast-2.rds.amazonaws.com',
                                     user='admin',
                                     password='sadwyr-sobbun-6tuRzo',
                                     )
        cursor = connection.cursor()
        cursor.execute('use Script')
        for i in range(1, len(datas)):
            x = datetime.datetime.strptime(datas[i][1], '%Y-%m-%d %H:%M:%S')
            query = f'''INSERT INTO Currencies (`Name`, `Date`, `Time`, `Open`,`High`, `Low`, `Close`,`Volume`, `Currency`)
        VALUES ('{datas[i][0]}','{x.date()}','{x.time()}','{datas[i][2]}','{datas[i][3]}','{datas[i][4]}','{datas[i][5]}','{datas[i][6]}','AUD');'''
        #     print(query)
            cursor.execute(query)
            cursor.connection.commit()
    except:
        continue
