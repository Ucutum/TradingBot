import pandas as pd
import mplfinance as mpf
import requests
import datetime
import yfinance as yf

def request_stocks(start: datetime.datetime, symbol: str):
    data = yf.download(symbol, period="1d", start=start.strftime("%Y-%m-%d"))
    return data

def read_data(filename: str) -> pd.DataFrame:
    data = pd.read_csv(filename, delimiter=';')
    return data

def write_data(df: pd.DataFrame, filename):
    df.to_csv(filename, sep=';')
    

if __name__ == '__main__':
    # request_stocks(datetime.datetime(2020, 1, 1), "NVDA")
    # write_data(request_stocks(datetime.datetime(2019, 1, 1), "AAPL"), "AAPL.csv")
    # print(read_data("AAPL.csv"))