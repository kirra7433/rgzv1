import pandas as pd
import datetime, locale
import numpy
from prettytable import PrettyTable

locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")

def tb(x):
    table = PrettyTable()
    table.add_column("Дата", [x[i][0] for i in range(len(x))])
    table.add_column("1 пара 08:00-09:30", [x[i][1] for i in range(len(x))])
    table.add_column("2 пара 09:40-11:10", [x[i][2] for i in range(len(x))])
    table.add_column("3 пара 11:20-12:50", [x[i][3] for i in range(len(x))])
    table.add_column("4 пара 13:20-14:50", [x[i][4] for i in range(len(x))])
    table.add_column("5 пара 15:00-16:30", [x[i][5] for i in range(len(x))])
    print(table)


def today(df):
    today = datetime.date.today()
    return df.values[df['Дата'] == today.strftime("%d.%m.%Y(%A)").lower()]


def week(df):
    week = [datetime.date.today() + datetime.timedelta(days=i) for i in range(7+1)]
    sp = []
    for date in week:
        sp += [df.values[df['Дата'] == date.strftime("%d.%m.%Y(%A)").lower()][0].tolist()]
    return sp


def semestr(df):
    sp = []
    def daterange(date1, date2):
        for n in range(int ((date2-date1).days)+1):
            yield date1 + datetime.timedelta(n)
    for date in daterange(datetime.date(2017,9,1), datetime.date(2017,12,31)):
        sp += [df.values[df['Дата'] == date.strftime("%d.%m.%Y(%A)").lower()][0].tolist()]
    return sp


def main():
    calls_df, = pd.read_html("http://www.osu.ru/pages/schedule/?who=1&what=1&facult=5683&potok=2013&group=6861&mode=full",header=0)

    for index in range(calls_df.index.argmax()):
        if index <= calls_df.index.argmax():
            if calls_df.values[index][0] == 'Дата':
                calls_df.drop(calls_df.index[index], inplace=True)
                calls_df.reset_index(drop=True, inplace=True)

    calls_df = calls_df.replace(numpy.nan, ' ', regex=True)

    query = input("День, неделя, семестр? ")
    if query == "день":
        res = today(calls_df)
    elif query == "неделя":
        res = week(calls_df)
    elif query == "семестр":
        res = semestr(calls_df)
    else:
        print("И всё таки?")

    tb(res)


if __name__ in "__main__":
    main()
