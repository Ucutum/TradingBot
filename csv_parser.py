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
    return sec.getCandleQuotesAsDataFrame(date_from, date_to, interval=MoexCandlePeriods.Period1Day)

def request_stocks(start: datetime.datetime, symbol: str):
    data = yf.download(symbol, period="1d", start=start.strftime("%Y-%m-%d"))
    return data

def read_data(filename: str) -> pd.DataFrame:
    data = pd.read_csv(filename, delimiter=';')
    return data

def write_data(df: pd.DataFrame, filename):
    df.to_csv(filename, sep=';')
    

def main():
    if __name__ == '__main__':
        write_data(request_stocks(datetime.datetime(2000, 1, 1), "GOOG"), "graphs/GOOG.csv")
        write_data(request_stocks(datetime.datetime(2000, 1, 1), "AAPL"), "graphs/AAPL.csv")

        with open('all.csv', newline='', encoding="utf-8") as f:
            spamreader = csv.reader(f, delimiter=';')

            for row in spamreader:
                if row[2] == "NASDAQ": 
                    write_data(request_stocks(datetime.datetime(2000, 1, 1), row[1]), f"graphs/{row[1]}.csv")
                else:
                    write_data(request_stocks_ru(datetime.date(2022, 1, 1), datetime.date.today(), row[1]), f"graphs/{row[1]}.csv")


if __name__ == "__main__":
    main()