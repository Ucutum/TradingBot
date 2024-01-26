import pandas as pd
import mplfinance as mpf


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
    

data = read_data('SBER_000101_240101.csv')
data = data[-30:]
print(data)

mpf.plot(data,type='candle')