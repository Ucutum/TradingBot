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
import os
    

def craete_graph(data, company_token):
    data.rename(columns={
        'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume',
        'Date': 'date'
    }, inplace=True)
    data.set_index('date', inplace=True)
    d = data.index[-1]
    # print("!!!", d)
    # print(data)
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
    # companies = ["QIWI"]
    companies = ["AMD"]

    for company in companies:
        if not os.path.exists(f"models/{company}_model.h5"):
            continue
        write_data(request_stocks(datetime.datetime(2000, 1, 1), company), "models/" + company + ".csv")
        remove_trailing_empty_lines(f"graphs/{company}.csv")
        data = read_data(f"graphs/{company}.csv", delimiter=';')
        # x = np.array([np.array(data[["Open", "Close"]].mean(axis=1))[-100:]])
        x = data[["Close"]].to_numpy()
        x = np.array([x[:, 0][-100:]])
        # x = np.array(x)
        print("X1", x)
        x, mxx = grounding_one(x)
        model = load_model(f"models/{company}_model.h5")
        print("X2", x)
        p = model.predict(x)
        p = ungrounding_one(p, mxx)[0].tolist()

        # print(data[-100:].tail(6))
        print("P", p)

        last = data['Close'][len(data) - 1]
        for i in range(1):
            last_date = data["Date"].iloc[-1]
            next_day = last_date + timedelta(days=1)
            # Date;Open;High;Low;Close;Adj Close;Volume
            if str(p[i]) == "nan":
                p[i] = last
                print("WARNING NAN")
            # print(p[i])
            prow = {
                'Date': next_day,
                'Open': last,
                'High': max(last, p[i]) + 1,
                'Low': min(last, p[i]) - 1,
                'Close': p[i],
                'Volume': 0,
            }
            last = p[i]
            data.loc[len(data)] = prow
            # data[len(data)] = prow
        # print(data[-100:].tail(6))
        craete_graph(data[-100:], company)
        print("Done", company)


if __name__ == '__main__':
    main()
