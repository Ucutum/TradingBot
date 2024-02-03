import os
import csv


def get_graphs_paths():
    '''дает ссылки на графики прогы Артема'''
    with open("all.csv") as f:
        companies = [e[1] for e in csv.reader(f, delimiter=";")]
    return list(filter(lambda x: x is not None, [(
            f"graph/{i}_alggraph.png" if
         os.path.exists(f"static/graph/{i}_alggraph.png"
                        ) else None) for i in companies]))