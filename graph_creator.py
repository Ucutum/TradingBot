import pandas as pd
import mplfinance as mpf
from csv_parser import request_stocks
from datetime import date
from stock_ai import generate, load_model, grounding, ungrounding_one, grounding_one
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import csv
from learning_ai import read_data
from csv_parser import write_data, request_stocks
import csv
import datetime
    

def craete_graph(data, company_token):
    data.rename(columns={
        'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume',
        'Date': 'date'
    }, inplace=True)
    data.set_index('date', inplace=True)
    d = data.index[-6]
    print("!!!", d)
    mpf.plot(
        data, type='candle',
        savefig=f"static/graph/{company_token}_graph.png",
        vlines=dict(vlines=d,
                    linewidths=1, alpha=0.5))


def remove_trailing_empty_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        while lines and lines[-1].isspace():
            lines.pop()
        with open(file_path, 'w') as file:
            file.writelines(lines)
        print(f"Removed trailing empty lines from {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    with open("all.csv") as f:
        companies = [e[1] for e in csv.reader(f, delimiter=";")]
    print(companies)

    for company in companies:
        print("!!!!!")
        print(company)
        write_data(request_stocks(datetime.datetime(2000, 1, 1), company), "models/" + company + ".csv")
        remove_trailing_empty_lines(f"models/{company}.csv")
        data = read_data(f"models/{company}.csv", delimiter=';')
        # data = read_data("models/YNDX_000101_240101.csv", delimiter=';')
        x = np.array([np.array(data[["Open", "Close"]].mean(axis=1))[-100:]])
        x, mxx = grounding_one(x)
        model = load_model(f"models/{company}_model.h5")
        p = model.predict(x)
        p = ungrounding_one(p, mxx)[0]
        print(data.head(5))
        print(data.columns)

        last = data['Close'][len(data) - 1]
        for i in range(5):
            print(len(data))
            print(data.iloc[-1])
            print(data.iloc[-1])
            last_date = data["Date"].iloc[-1]
            next_day = last_date + timedelta(days=1)
            # Date;Open;High;Low;Close;Adj Close;Volume
            prow = {
                'Date': last_date,
                'Open': last,
                'High': max(last, p[i]) + 1,
                'Low': min(last, p[i]) - 1,
                'Close': p[i],
                'Volume': 0,
            }
            last = p[i]
            data.loc[next_day] = prow
        craete_graph(data[-100:], company)


if __name__ == '__main__':
    main()
