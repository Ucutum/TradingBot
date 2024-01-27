import pandas as pd
import mplfinance as mpf
from csv_parser import request_stocks
from datetime import date


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
    mpf.plot(data, type='candle', savefig=f"static/graph/{company_token}_graph.png")


def main():
    paid_companies = [
        {"title": "Сбербанк", "active": False, "token": "SBER"},
        {"title": "Тинькофф", "active": False, "token": "TCSG"},
        {"title": "Яндекс", "active": False, "token": "YNDX"},
        {"title": "Газпром", "active": False, "token": "GAZP"},
        {"title": "Татнефть", "active": False, "token": "TATN"},
        {"title": "Мечел", "active": False, "token": "MTLR"},
        {"title": "Лукойл", "active": False, "token": "LKOH"},
        {"title": "Аэрофлот", "active": False, "token": "AFLT"},
        {"title": "Сургутнефтегаз", "active": False, "token": "SNGS"},
        {"title": "МТС", "active": False, "token": "MTSS"},
        {"title": "Магнит", "active": False, "token": "MGNT"},
        {"title": "Новатэк", "active": False, "token": "NVTK"},
        {"title": "М.Видео", "active": False, "token": "MVID"},
        {"title": "Татнефть", "active": False, "token": "TATN"},
        {"title": "НЛМК", "active": False, "token": "NLMK"},
        {"title": "Эн+", "active": False, "token": "ENPG"},
        {"title": "ММК", "active": False, "token": "MAGN"},
        {"title": "Северсталь", "active": False, "token": "CHMF"},
        {"title": "АФК Система", "active": False, "token": "AFKS"},
        {"title": "Трубная Металлургическая Компания", "active": False, "token": "TRMK"},
        {"title": "Мосэнерго", "active": False, "token": "MSNG"},
        {"title": "ФосАгро", "active": False, "token": "PHOR"},
        {"title": "РусГидро", "active": False, "token": "HYDR"},
        {"title": "Полюс", "active": False, "token": "PLZL"},
        {"title": "АЛРОСА", "active": False, "token": "ALRS"},
        {"title": "РосНефть", "active": False, "token": "RNFT"},
        {"title": "КАМАЗ", "active": False, "token": "KMAZ"},
        {"title": "Россети Московский Регион", "active": False, "token": "MSRS"},
        {"title": "Детский Мир", "active": False, "token": "DSKY"},
        {"title": "Группа Черкизово", "active": False, "token": "GCHE"},
        {"title": "Совкомфлот", "active": False, "token": "FLOT"},
        {"title": "СОЛЛЕРС", "active": False, "token": "SVAV"},
        {"title": "Юнипро", "active": False, "token": "UPRO"},
    ]
    for company in paid_companies:
        print(company['token'])
        data = request_stocks(date(2020, 1, 1), date(2024, 1, 26), company['token'])
        craete_graph(data, company['token'])


if __name__ == '__main__':
    main()
