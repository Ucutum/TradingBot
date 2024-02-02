import pandas as pd
import mplfinance as mpf
import requests
import datetime
import yfinance as yf
import csv
from moeximporter import MoexImporter, MoexSecurity, MoexCandlePeriods

mi = MoexImporter()

def request_stocks_ru(date_from: datetime.date, date_to: datetime.date, symbol: str):
    sec = MoexSecurity(symbol, mi)
    data = sec.getCandleQuotesAsDataFrame(date_from, date_to, interval=MoexCandlePeriods.Period1Day)
    data.reset_index(inplace=True)
    data.drop(columns=['end', 'value'], inplace=True)
    data.rename(columns={'begin' : 'Date', 'open' : 'Open', 'close' : 'Close', 'high' : 'High', 'low' : 'Low', 'quantity' : 'Volume'}, inplace=True)

    data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%y')
    data['Open'] = pd.to_numeric(data['Open'])
    data['High'] = pd.to_numeric(data['High'])
    data['Low'] = pd.to_numeric(data['Low'])
    data['Close'] = pd.to_numeric(data['Close'])
    data['Volume'] = pd.to_numeric(data['Volume'])
    
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
    with open('all.csv', newline='', encoding="utf-8") as f:
        spamreader = csv.reader(f, delimiter=';')

        for row in spamreader:
            print(f"Downloadding data {row[1]}")
            if row[2] == "NASDAQ": 
                write_data(request_stocks(datetime.datetime(2000, 1, 1), row[1]), path + f"{row[1]}.csv")
            else:
                write_data(request_stocks_ru(datetime.date(2023, 1, 1), datetime.date.today(), row[1]), path + f"{row[1]}.csv")


if __name__ == "__main__":
    parse("graphs/")