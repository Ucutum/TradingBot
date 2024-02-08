import pandas as pd
import mplfinance as mpf
import requests
import datetime
import yfinance as yf
import csv
from moexalgo import Ticker

def request_stocks_ru(date_from: datetime.date, symbol: str):
    sber = Ticker(symbol)

    data = pd.DataFrame(sber.candles(date=date_from.strftime('%Y-%m-%d'), period = 'D', till_date=datetime.date.today()))
    data = data[['begin', 'open', 'close', 'high', 'low', 'value', 'volume', 'end']]
    data.drop(columns=['value', 'end'], inplace=True)
    data.rename(columns={'begin' : 'Date', 'open' : 'Open', 'close' : 'Close', 'high' : 'High', 'low' : 'Low', 'volume' : 'Volume'}, inplace=True)
    data = data.reindex(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    return data

def request_stocks(start: datetime.datetime, symbol: str):
    data = yf.download(symbol, period="1d", start=start.strftime("%Y-%m-%d"))
    data.reset_index(inplace=True)
    data.drop(columns=['Adj Close'], inplace=True)
    return data

def read_data(filename: str) -> pd.DataFrame:
    data = pd.read_csv(filename, delimiter=';', index_col=False)
    return data

def write_data(df: pd.DataFrame, filename):
    df.to_csv(filename, sep=';', index=False)
    

def parse(path):
    # write_data(request_stocks(datetime.datetime(2000, 1, 1), "GOOG"), path + "GOOG.csv")
    # write_data(request_stocks(datetime.datetime(2000, 1, 1), "AAPL"), path + "AAPL.csv")

    with open('all.csv', newline='', encoding="utf-8") as f:
       spamreader = csv.reader(f, delimiter=';')
       for row in spamreader:
           print(f"Downloadding data {row[1]}")
           if row[2] == "NASDAQ": 
               write_data(request_stocks(datetime.datetime(2000, 1, 1), row[1]), path + f"{row[1]}.csv")
           else:
               write_data(request_stocks_ru(datetime.datetime(2000, 1, 1), row[1]), path + f"{row[1]}.csv")

if __name__ == "__main__":
    parse("graphs/")