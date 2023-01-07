from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import pymysql
import logging
import os
import datetime

from selenium.webdriver.chrome.service import Service

# os.chdir(r'C:\Users\Administrator\Desktop\DB1')
logging.basicConfig(filename="france.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.debug("This is new debug info ")


try:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("window-size=1200x600")
    options.headless = False
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    lst = list(set(['BHP', 'RIO', 'FMG', 'MIN', 'HIO', 'MGT', 'WHC', 'VMS', 'CIA', 'WPL', 'ANZ', 'CBA', 'WBC', 'NAB', 'MQG', 'BEN', 'BOQ', 'CHN', 'OZL', 'MZZ', 'RDS', 'AGL', 'ORG', 'MEZ', 'STO', 'QAN', 'BPT', 'WOR', 'NEW', 'GNX', 'OSH', 'NCM', 'SLR', 'EVN', 'SVL', 'PDI', 'TMZ', 'MZZ', 'SYR', 'CXO',
               'AZL', 'MNS', 'PLS', 'EUR', 'SYA', 'LKE', 'WSA', 'ADD', 'TLS', 'CSL', 'CWN', 'FLT', 'TWE', 'QBE', 'CWY', 'NUF', 'EMD', 'AIZ', 'A2M', 'IXR', 'MRD', 'WOW', 'MYR', 'WES', 'HVN', 'COL', 'RBL', 'APX', 'HUM', 'ZIP', 'ERA', '92E', '29M', 'SFR', 'KAR', 'S32', 'IGO', 'BVR', 'QAN', 'LYC', 'WOR', 'PX1']))

    data = [['COMPANY', 'PRICE', "VOLUME", 'P/E RATIO', 'PRICE/FREE CASH FLOW',
             'ANNUAL YIELD', 'PREVIOUS CLOSE', 'LOW PRICE', 'HIGH PRICE']]

    for i in lst:

        driver.get("https://www2.asx.com.au/markets/company/"+f'{i}')
        driver.implicitly_wait(3)
        time.sleep(3)
        price = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Last Price')]/../*[2]"))).text.split(' ')[0]
        volume = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//*[@id='company_header']/div/div[1]/div/div[2]/dl[2]/dd"))).text
        pe = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'P/E ratio')]/../*[2]"))).text
        pf = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Price/free cash flow')]/../*[2]"))).text
        an_yield = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Annual yield')]/../*[2]"))).text
        prev_close = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Previous close')]/../*[2]"))).text
        day_range = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Day range')]/../*[2]"))).text
        lowPrice, highPrice = day_range.split('-')[0], day_range.split('-')[1]

        print(i, price, volume, pe, pf, an_yield,
              prev_close, lowPrice, highPrice)
        data.append([i, price, volume, pe, pf, an_yield,
                    prev_close, lowPrice, highPrice])

    driver.close()
    x = datetime.datetime.now()
    connection = pymysql.connect(
        host='database1-instance-1.crydakzjfkez.ap-southeast-2.rds.amazonaws.com', user='admin', password='sadwyr-sobbun-6tuRzo')
    cursor = connection.cursor()
    cursor.execute('use Script')
    # previous_date = x - datetime.timedelta(days=1)
    # previous_week_date = x - datetime.timedelta(days=7)
    # previous_month_date = x - datetime.timedelta(days=28)
    # previous_three_month_date = x - datetime.timedelta(days=90)
    # query1 = f'''SELECT * FROM EquityTargets WHERE Date="{previous_date.date()}"'''
    # query2 = f'''SELECT * FROM EquityTargets WHERE Date="{previous_week_date.date()}"'''
    # query3 = f'''SELECT * FROM EquityTargets WHERE Date="{previous_month_date.date()}"'''
    # query4 = f'''SELECT * FROM EquityTargets WHERE Date="{previous_three_month_date.date()}"'''
    # cursor.execute(query1)
    # dat1 = cursor.fetchall()
    # cursor.execute(query2)
    # dat2 = cursor.fetchall()
    # cursor.execute(query3)
    # dat3 = cursor.fetchall()
    # cursor.execute(query4)
    # dat4 = cursor.fetchall()
    # dat1 = list(dat1)
    # dat2 = list(dat2)
    # dat3 = list(dat3)
    # dat4 = list(dat4)
    # wantedtime = datetime.timedelta(hours=previous_date.time().hour, minutes=previous_date.time().minute)
    # def getthedata(value):
    #     if value[1] == wantedtime:
    #         return True
    #     else:
    #         return False
    # dat1 = list(filter(getthedata,dat1))
    # dat2 = list(filter(getthedata,dat2))
    # dat3 = list(filter(getthedata,dat3))
    # dat4 = list(filter(getthedata,dat4))
    # # inde = len(dat)
    # def findvalue(value):
    #     if value[0] == wantedvalue:
    #         return True
    #     else:
    #         return False
    for i in range(1, len(data)):
        # performanceT1 = None
        # performanceT7 = None
        # performanceT28 = None
        # performanceT90 = None
        # if '--' in data[i][1]:
        #     pass
        # else:
        #     today_price = float(data[i][1].replace('$',''))
        #     wantedvalue = data[i][0]
        #     if len(dat1) > 0:
        #         filtereddata = filter(findvalue, dat1)
        #         if len(filtereddata) > 0:
        #             if ('--' in filtereddata[0][1]):
        #                 pass
        #             else:
        #                 previous_price = float(filtereddata[0][1].replace('$',''))
        #                 performanceT1 = (today_price-previous_price)/previous_price
        #     if len(dat2) > 0:
        #         filtereddata = filter(findvalue, dat2)
        #         if len(filtereddata) > 0:
        #             if ('--' in filtereddata[0][1]):
        #                 pass
        #             else:
        #                 previous_price = float(filtereddata[0][1].replace('$',''))
        #                 performanceT1 = (today_price-previous_price)/previous_price
        #     if len(dat3) > 0:
        #         filtereddata = filter(findvalue, dat3)
        #         if len(filtereddata) > 0:
        #             if ('--' in filtereddata[0][1]):
        #                 pass
        #             else:
        #                 previous_price = float(filtereddata[0][1].replace('$',''))
        #                 performanceT1 = (today_price-previous_price)/previous_price
        #     if len(dat4) > 0:
        #         filtereddata = filter(findvalue, dat4)
        #         if len(filtereddata) > 0:
        #             if ('--' in filtereddata[0][1]):
        #                 pass
        #             else:
        #                 previous_price = float(filtereddata[0][1].replace('$',''))
        #                 performanceT1 = (today_price-previous_price)/previous_price
        query = f'''INSERT INTO EquityTargets (`Name`, `Price`, `Volume`,`PERatio`, `PriceFreeCashFlow`, `AnnualYield`, `Currency`, `Date`,`Time`,`PrevClose`,`LowPrice`,`HighPrice`) VALUES ('{data[i][0]}','{data[i][1]}','{data[i][2]}','{data[i][3]}','{data[i][4]}','{data[i][5]}','AUD','{x.date()}','{x.time()}','{data[i][6]}','{data[1][7]}','{data[i][8]}');'''
        cursor.execute(query)
        # query = f'''INSERT INTO EquityTargetEvaluation (`Name`, `T-1`, `T-7`,`T-28`, `T-90`, `Date`, `Time`) VALUES ('{data[i][0]}','{performanceT1}','{performanceT7}','{performanceT28}','{performanceT90}','{x.date()}','{x.time()}');'''
        # cursor.execute(query)
        cursor.connection.commit()
    print("Fineshed the script")
except Exception as e:
    logger.error(e)
# with xlsxwriter.Workbook('test.xlsx') as workbook:
#     worksheet = workbook.add_worksheet()

#     for row_num, dat in enumerate(data):
#         worksheet.write_row(row_num, 0, dat)
