import csv
from datetime import date
from csv_parser import request_stocks, write_data


with open("db/all_names.csv") as f:
    companies = [e[1] for e in csv.reader(f, delimiter=";")]
print(companies)


for company in companies:
    write_data(request_stocks(date(2019, 1, 1), date(2024, 1, 26), company), f"db/{company}.csv")

