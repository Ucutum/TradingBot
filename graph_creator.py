import pandas as pd
import mplfinance as mpf
from csv_parser import request_stocks
from datetime import date


def read_data(filename):
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
    

def craete_graph(data, company_token):
    mpf.plot(data, type='candle', savefig=f"static/graph/{company_token}_graph.png")


def main():
    for company in ["SBER", "GAZP", "YNDX"]:
        data = request_stocks(date(2020, 1, 1), date(2024, 1, 26), "GAZP")
        craete_graph(data[-100:], 'SBER')


if __name__ == '__main__':
    main()