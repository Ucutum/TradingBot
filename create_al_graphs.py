import mplfinance as mpf
import pandas as pd
import csv
from graph_creator import remove_trailing_empty_lines
import os


def create_graph(token):
    remove_trailing_empty_lines(f"graphs/{token}.csv")
    print(f"Creage graph, {token}")
    # df = pd.read_csv(f"graphs/{token}.csv")
    df = pd.read_csv(f"graphs/{token}.csv", delimiter=";")
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, inplace=True)
    df.set_index('date', inplace=True)

    if os.path.exists(f"gdata/{token}_graph_data.csv"):
        with open(f"gdata/{token}_graph_data.csv") as f:
            reader = csv.reader(f, delimiter=';')
            seq_of_points_ = list(reader)
            seq_of_points = []
            r = max(df[['close']].values)[0] - min(df[['close']].values)[0]
            print("RRR", r)
            r /= 100
            print(r)
            for line in seq_of_points_:
                print(line)
                seq_of_points.append([(line[0], float(line[1])), (line[0], float(line[1]) + r)])

        with open(f"gdata/{token}_graph_colors.txt") as f:
            colors = [i.strip() for i in f.readlines()]

        print(colors)
        r = len(df[['close']].values) / 100
        mpf.plot(df,alines=dict(alines=seq_of_points, colors=colors, linewidths=r), savefig=f"static/graph/{token}_alggraph.png")


def create_all():
    with open("all.csv") as f:
        companies = [e[1] for e in csv.reader(f, delimiter=";")]
    for company in companies:
        create_graph(company)


def main():
    create_all()


if __name__ == '__main__':
    main()