import datetime
import sqlite3
import sys
import time
from re import T
from threading import Thread

from selenium import webdriver

import config

UK_list = ["CUKX.L", "ISF.L", "IUSA.L", "IWRD.L",
           "SWDA.L", "IWDP.L", "VMIG.L", "VMID.L", "VUSA.L"]

UK_list_FT_website = ["https://markets.ft.com/data/etfs/tearsheet/historical?s=CUKX:LSE:GBX",
"https://markets.ft.com/data/etfs/tearsheet/historical?s=ISF:LSE:GBX",
"https://markets.ft.com/data/etfs/tearsheet/historical?s=IUSA:LSE:GBX",
"https://markets.ft.com/data/etfs/tearsheet/historical?s=IWRD:LSE:GBX",
"https://markets.ft.com/data/etfs/tearsheet/historical?s=SWDA:LSE:GBX",
"https://markets.ft.com/data/etfs/tearsheet/historical?s=IWDP:LSE:GBX",
"https://markets.ft.com/data/etfs/tearsheet/historical?s=VMIG:LSE:GBP",
"https://markets.ft.com/data/etfs/tearsheet/historical?s=VMID:LSE:GBP",
"https://markets.ft.com/data/etfs/tearsheet/historical?s=VUSA:LSE:GBP"
]
UK_stock_buy_date = '2022-02-17'

# today = datetime.date.today()
# todayaddone = today + datetime.timedelta(days=1)
# print(todayaddone)


# * connecting to database

connection = sqlite3.connect(config.DB_File_address)

connection.row_factory = sqlite3.Row

cursor = connection.cursor()


# * getting the UK_stock price date with only specify stock 
stock_data_list = []
convert = "%A, %B %d, %Y"


def fetch_data(UK_list_FT_website,stock_id,lastest_day):

    current_time = datetime.datetime.now().time()
    # print(current_time)

    market_close_time = datetime.time(18,0,0)
    # print(market_close_time)

    today = datetime.date.today()

    sql =[]

    # * connecting the selenium webdriver

    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.get(UK_list_FT_website)

    try:
        for y in range(1,20):
            for x in range(1,7):

                line = "/html/body/div[3]/div[2]/section[3]/div[1]/div/div/div[2]/div[2]/table/tbody/tr["+str(y)+"]/td["+str(x)+"]"
                # print(line)
                search = driver.find_element_by_xpath(line)
                data = search.text
                if x == 1:
                    date = data
                    # print("date : "+str(date))
                    date = datetime.datetime.strptime(str(date), convert)

                if x == 2:
                    open = data
                    # print("open : "+str(open))
                    open = (str(open).replace(",",""))
                    

                if x == 3:
                    high = data
                    # print("high : "+str(high))
                    high = (str(high).replace(",",""))

                if x == 4:
                    low = data
                    # print("low : "+str(low))
                    low = (str(low).replace(",",""))

                if x == 5:
                    close = data
                    # print("close : "+str(close))
                    close = (str(close).replace(",",""))

                if x == 6:
                    volume = data
                    volume = (str(volume).replace(",",""))
                    # print("volume : "+str(volume))

            # * filter out the data we already have in database 
            if date.date() > lastest_day:
                # * filter out the date if the market still open
                if date.date() == today and current_time < market_close_time :
                    print("market still open so take one day before")
                else:
                    stock_price_for_one_day =[date,open,high,low,close,volume]
                    stock_data_list.append(stock_price_for_one_day)
                    line = "INSERT INTO UK_stock_price(UK_stock_id,date,open,high,low,close,volume) VALUES (" + str(stock_id)+" , '"+str(date)+"' , "+str(open)+" , "+str(high)+" , "+str(low)+" , "+str(close)+" , "+str(volume)+");"
                    sql.append(line) 

            else:
                print("already in database !!! ")
            
            
       
        driver.quit()
    except :
        print("error")
        driver.quit()
        quit()

    return sql

# -------------------------------------------------------------------------

cursor.execute("""
    SELECT MAX(date) from UK_stock_price;
""")

lastest_day = cursor.fetchone()
# print(lastest_day[0])

lastest_day = datetime.datetime.strptime(lastest_day[0], "%Y-%m-%d %H:%M:%S")
lastest_day = lastest_day.date()


all_sql = []

# * This is how u make a single stock ---------------------------- 
# CUKX_sql = fetch_data(UK_list_FT_website[0],1,lastest_day)
# all_sql.extend(CUKX_sql)

# * getting all the market date ---------------------------------- 
for i in range(len(UK_list_FT_website)):
    stock_sql = fetch_data(UK_list_FT_website[i],i+1,lastest_day)
    all_sql.extend(stock_sql)




print(all_sql)

for length in range(0,len(all_sql)):
    print(all_sql[length])
    cursor.execute(all_sql[length])


connection.commit()





