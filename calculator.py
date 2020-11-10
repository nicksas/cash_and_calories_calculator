import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.today = dt.date.today()
        self.week = self.today - dt.timedelta(7)

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        records = []
        for record in self.records:
            if record.date == self.today:
                records.append(record.amount)
        return sum(records)

    def get_week_stats(self):
        records = []
        for record in self.records:
            if self.week <= record.date <= self.today:
                records.append(record.amount)
        return sum(records)

    def get_balance_remained(self):
        balance = self.limit - self.get_today_stats()
        return balance


class CaloriesCalculator(Calculator):
    pass


class CashCalculator(Calculator):
    EURO_RATE = 90.09
    USD_RATE = 76.26
    RUB_RATE = 1

    def get_today_cash_remained(self, currency='rub'):
        currencies = {
            'eur': ('Euro', self.EURO_RATE),
            'usd': ('USD', self.USD_RATE),
            'rub': ('руб', self.RUB_RATE)
        }

        cash_remained = self.get_balance_remained()
        if cash_remained == 0:
            return 'Денег нет, держись'
        if currency not in currencies:
            return f'Валюта {currency} не поддерживается'
        name, rate = currencies[currency]
        cash_remained = round(cash_remained / rate, 2)
        if cash_remained > 0:
            message = f'На сегодня осталось {cash_remained} {name}'
        else:
            cash_remained = abs(cash_remained)
            message = (f'Денег нет, держись: твой долг - {cash_remained} '
                       f'{name}')
        return message


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


cash_calculator = CashCalculator(1000)
cash_calculator.add_record(Record(amount=999, comment="кофе"))
cash_calculator.add_record(Record(amount=145, comment="кофе", date='3.11.2020'))

print(cash_calculator.get_today_stats())
print(cash_calculator.get_week_stats())
print(cash_calculator.get_today_cash_remained('eur'))

