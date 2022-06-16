import datetime
import sqlite3
from tokenize import String

import pandas as pd
import yfinance as yf

import config

today = datetime.date.today()

# * connecting to database

connection = sqlite3.connect(config.DB_File_address)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()


def get_market_data(connection,lastest_day):

    US_list = ["JETS", "VTI", "VTV", "VT", "VGT", "VOO", "TSM", "ITA"]

    today = datetime.date.today()
    
    todayaddone = today + datetime.timedelta(days=1)


    # * connecting to database

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()


    cursor.execute("""
        SELECT id,symbol ,name FROM US_stock
    """)

    rows = cursor.fetchall()

    print(rows)

    symbols = []
    stock_id = []
    for row in rows:
        symbols.append(row['symbol'])
        stock_id.append(row['id'])

    print(symbols)
    print(stock_id)


    # * UK stock----------------------------------------------------
    # cukx = yf.Ticker('CUKX.L')

    # * Getting info ----------------------------------------------------
    # for x in US_list:
    #     # print(x)
    #     test = yf.Ticker(x)
    #     print(test.info['symbol'])
    #     print(test.info['longName'])

    # * history function----------------------------------------------------
    # isf_history = isf.history()
    # print(isf_history.columns)
    # print(isf_history)

    # * reformating the dataframe ----------------------------------------------------
    # isf_history["Date"] = isf_history.index
    # isf_history = isf_history[["Date", "Open", "High",
    #                            "Low", "Close", "Volume"]]
    # isf_history.reset_index(drop=True, inplace=True)

    # * reformating the dataframe ----------------------------------------------------
    # print(isf_history.head())
    # print(isf_history['Date'].head())

    # * A list for the dataframe columns ------------------------------------------
    columns_in_dataframe = ["Date", "Open", "High", "Low", "Close", "Volume"]

    # * using download function -> can get the data in a period ----------------
    data = yf.download(US_list, start=lastest_day, end=todayaddone)
    # print(data)
    # print(data.index)
    # print(data.index[0])

    # * reformating the dataframe ----------------------------------------------------
    # data["Stock_id"] = stock_id[0]
    data["Date"] = data.index
    data = data[columns_in_dataframe]


    # * reformating the dataframe ----------------------------------------------------
    print("after formating --------------------------------")
    print("All data")
    # print(data)

    # * drop all the nan value in the dataframe 
    # https://www.journaldev.com/33492/pandas-dropna-drop-null-na-values-from-dataframe
    data = data.dropna()
    print(data)

    # * Testing to print date
    # print("----------------------------------------------------")
    # print("Date")
    # print(data['Date'][0])

    # * Testing to print Stock open
    # print("----------------------------------------------------")
    # print("JETS Open")
    # open = data["Open"]["JETS"][1]
    # close = data["Close"]["JETS"][0]
    # print(open)
    # print(close)
    # print(open + close)

    # * print how many row in the dateframe
    len_of_the_df = len(data.index)
    # print(len_of_the_df)

    # * Getting all the date and insert to database ---------------------------------------

    for y in range(0, len(US_list)):
        for z in range(0, len_of_the_df):
            date = data["Date"][z]
            open = data["Open"][str(US_list[y])][z]
            high = data["High"][str(US_list[y])][z]
            low = data["Low"][str(US_list[y])][z]
            close = data["Close"][str(US_list[y])][z]
            volume = data["Volume"][str(US_list[y])][z]

            line = "INSERT INTO US_stock_price(US_stock_id,date,open,high,low,close,volume) VALUES (" + str(
                stock_id[y])+" , '"+str(date)+"' , "+str(open)+" , "+str(high)+" , "+str(low)+" , "+str(close)+" , "+str(volume)+");"
            cursor.execute(line)

            print(line)
            # print(date)


    connection.commit()


cursor.execute("""
    SELECT MAX(date) from US_stock_price;
""")

lastest_day = cursor.fetchone()
# print(lastest_day[0])

US_stock_buy_date = "2021-05-05"
US_stock_buy_date = datetime.datetime.strptime(US_stock_buy_date, "%Y-%m-%d")
US_stock_buy_date = US_stock_buy_date.date()
print(type(US_stock_buy_date))

lastest_day = datetime.datetime.strptime(lastest_day[0], "%Y-%m-%d %H:%M:%S")
lastest_day = lastest_day.date()
print(type(lastest_day))

lastest_day_add_one = lastest_day + datetime.timedelta(days=1)
# lastest_day_add_one = datetime.datetime(2022,3,1).date()+ datetime.timedelta(days=1)

if lastest_day <= today:
    print("getting data from :" + str(lastest_day_add_one))
    get_market_data(connection,lastest_day_add_one)
else:
    print("up to date nothing to do")
    # get_market_data(connection,US_stock_buy_date,today)

