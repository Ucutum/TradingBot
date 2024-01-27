import pandas as pd
import mplfinance as mpf
from csv_parser import request_stocks
from datetime import date
from stock_ai import generate, load_model, grounding, ungrounding_one, grounding_one
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import csv


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
    d = data.index[-6]
    print("!!!", d)
    mpf.plot(
        data, type='candle',
        savefig=f"static/graph/{company_token}_graph.png",
        vlines=dict(vlines=d,
                    linewidths=1, alpha=0.5))


def main():
    with open("all.csv") as f:
        companies = [e[1] for e in csv.reader(f, delimiter=";")]
    print(companies)

    for company in companies:
        data = request_stocks(date(2020, 1, 1), date(2024, 1, 26), company)
        # data = read_data("models/YNDX_000101_240101.csv", delimiter=';')
        x = np.array([np.array(data[["open", "close"]].mean(axis=1))[-100:]])
        x, mxx = grounding_one(x)
        model = load_model(f"models/{company}_model.h5")
        p = model.predict(x)
        p = ungrounding_one(p, mxx)[0]

        last = data['close'][-1]
        for i in range(5):
            last_date = data.index[-1]
            next_day = last_date + timedelta(days=1)
            prow = {
                # 'begin': last_date,
                'open': last,
                'high': max(last, p[i]) + 1,
                'low': min(last, p[i]) - 1,
                'close': p[i],
                'value': 0,
                'quantity': 0,
                'end': 0
            }
            last = p[i]
            data.loc[next_day] = prow
        craete_graph(data[-100:], company)


if __name__ == '__main__':
    main()
