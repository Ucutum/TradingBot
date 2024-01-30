import pandas as pd
import mplfinance as mpf
import requests
import datetime
import yfinance as yf
import csv

def request_stocks(start: datetime.datetime, symbol: str):
    data = yf.download(symbol, period="1d", start=start.strftime("%Y-%m-%d"))
    return data

def read_data(filename: str) -> pd.DataFrame:
    data = pd.read_csv(filename, delimiter=';')
    return data

def write_data(df: pd.DataFrame, filename):
    df.to_csv(filename, sep=';')
    

if __name__ == '__main__':
    write_data(request_stocks(datetime.datetime(2000, 1, 1), "GOOG"), "graphs/GOOG.csv")
    write_data(request_stocks(datetime.datetime(2000, 1, 1), "AAPL"), "graphs/AAPL.csv")

    with open('all.csv', newline='', encoding="utf-8") as f:
        spamreader = csv.reader(f, delimiter=';')

        for row in spamreader:
            write_data(request_stocks(datetime.datetime(2000, 1, 1), row[1]), f"graphs/{row[1]}.csv")

