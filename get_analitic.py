import csv
from datetime import date
from csv_parser import request_stocks, write_data


with open("all.csv") as f:
    companies = [e[1] for e in csv.reader(f, delimiter=";")]
print(companies)

for company in companies:
    print(company)
    write_data(request_stocks(date(2019, 1, 1), date(2024, 1, 26), company), f"graphs/{company}.csv")