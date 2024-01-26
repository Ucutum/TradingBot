import pandas as pd
import mplfinance as mpf
import requests
from datetime import date
from moeximporter import MoexImporter, MoexSecurity, MoexCandlePeriods

mi = MoexImporter()

def request_stocks(date_from: date, date_to: date, symbol: str):
    sec = MoexSecurity(symbol, mi)
    return sec.getCandleQuotesAsDataFrame(date_from, date_to, interval=MoexCandlePeriods.Period1Day)

def read_data(filename: str) -> pd.DataFrame:
    data = pd.read_csv(filename, delimiter=';')
    data = data[['<DATE>', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<VOL>']]
    data['<DATE>'] = pd.to_datetime(data['<DATE>'], format='%d/%m/%y')
    data['<OPEN>'] = pd.to_numeric(data['<OPEN>'])
    data['<HIGH>'] = pd.to_numeric(data['<HIGH>'])
    data['<LOW>'] = pd.to_numeric(data['<LOW>'])
    data['<CLOSE>'] = pd.to_numeric(data['<CLOSE>'])
    data['<VOL>'] = pd.to_numeric(data['<VOL>'])
    data.set_index('<DATE>', inplace=True)
    data.rename(columns={
        '<OPEN>': 'Open', '<HIGH>': 'High', '<LOW>': 'Low', '<CLOSE>': 'Close',
        '<VOL>': 'Volume'}, inplace=True)
    return data

def write_data(df: pd.DataFrame, filename):
    df.to_csv(filename, sep=';')
    

if __name__ == '__main__':
    write_data(request_stocks(date(2019, 1, 1), date(2024, 1, 26), "GAZP"), "GAZP.csv")