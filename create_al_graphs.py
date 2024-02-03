import mplfinance as mpf
import pandas as pd
import csv


def create_graph(token, path):
    df = pd.read_csv(path,index_col=0,parse_dates=True)

    with open(f"{token}_graph_data.csv") as f:
        reader = csv.reader(f, delimiter=';')
        seq_of_points_ = list(reader)
        seq_of_points = []
        for line in seq_of_points_:
            seq_of_points.append([(line[0], float(line[1])), (line[2], float(line[3]))])

    with open(f"{token}_graph_colors.csv") as f:
        colors = [i for i in f.readlines()]

    mpf.plot(df,alines=dict(alines=seq_of_points, colors=['b','r','g'], linewidths=5))
    mpf.savefig(f"static/graph/{token}_alggraph.png")
    mpf.close()