# tasks.py
from celery import Celery
import subprocess
import datetime
from csv_parser import parse
from create_al_graphs import create_all
import graph_creator
import json

celery = Celery(__name__, broker='pyamqp://guest:guest@localhost//')


with open('settings.json', 'r') as f:
    settings = json.load(f)
if settings["system"] == "Windows":
    run_command = ["./TradingBot.exe"] 
elif settings["system"] == "Linux":
    run_command = ["./TradingBot"]
else:
    run_command = ["./TradingBot"]


@celery.task
def data_updating():
    parse("graphs/")
    result = subprocess.run(run_command, stdout=subprocess.PIPE, text=True)

    create_all()
    graph_creator.main()