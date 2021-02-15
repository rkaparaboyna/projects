# using yahoo_fin
import pandas
from datetime import datetime
from pytz import timezone
import yfinance as yf
import yahoo_fin.stock_info as si


def get_time():
    return datetime.now(timezone('EST'))


def trading_hours():
    current_time = get_time()
    if current_time.strftime("%A") == "Saturday" or current_time.strftime("%A") == "Sunday":
        return False
    market_open = current_time.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close = current_time.replace(hour=16, minute=0, second=0, microsecond=0)
    if current_time < market_open or current_time > market_close:
        return False
    return True


def check_ticker(ticker):
    try:
        return yf.Ticker(ticker).info
    except KeyError:
        print("Invalid Ticker! " + str(ticker) + " does not exist.")


def check_positive(price):
    try:
        assert (isinstance(price, float) or isinstance(price, int)) and price > 0
    except AssertionError:
        print("Invalid attempt! Target price must be a postive number.")
        return False
    return True


def get_name(ticker):
    # returns the official company name corresponding to the ticker
    if not check_ticker(ticker):
        return
    return yf.Ticker(ticker).info['longName']


def get_price(ticker):
    if not check_ticker(ticker):
        return
    return si.get_live_price(ticker)


def get_data(ticker):
    if not check_ticker(ticker):
        return
    return si.get_data(ticker)


def get_previous_close(ticker):
    if not check_ticker(ticker):
        return
    if not trading_hours():
        return get_data(ticker)['adjclose'][-2]
    return get_data(ticker)['adjclose'][-1]


def price_alert(ticker, target_price):
    if check_positive(target_price):
        name = get_name(ticker)
        if not name:
            return
        while True:
            current_price = get_price(ticker)
            if current_price >= target_price:
                print(name + " has reached the target price!")
                break


def daily_change(ticker):
    previous_close = get_previous_close(ticker)
    if not previous_close:
        return
    price = get_price(ticker)
    return round((price - previous_close) / previous_close * 100, 2)


def period_change(ticker, start, end):
    if not check_ticker(ticker):
        return
    try:
        data = si.get_data(ticker, start_date=start, end_date=end)
    except (AssertionError, ValueError):
        print("Please input valid dates for start and end in the form of a string in the format month-day-year represented by numerals.")
    start_price = data['open'][0]
    end_price = data['adjclose'][-1]
    return round((end_price - start_price) / start_price * 100, 2)


def print_change(ticker, start, end):
    name = get_name(ticker)
    if not name:
        return
    change = period_change(ticker, start, end)
    if change < 0:
        print(name + " has decreased by " + str(abs(change)) + "% from " + start + " to " + end + ".")
    else:
        print(name + " has increased by " + str(change) + "% from " + start + " to " + end + ".")


def percentage_alert(ticker, amount=5):
    name = get_name(ticker)
    if not name:
        return
    while True:
        change = daily_change(ticker)
        if abs(change) > amount:
            if change < 0:
                print(name + " has decreased by " + str(abs(change)) + "%.")
            else:
                print(name + " has increased by " + str(change) + "%.")
            break


def get_date(ticker):
    if not check_ticker(ticker):
        return
    return get_data(ticker)[''][-1]


class Portfolio:
    def __init__(self, *args):
        self.items = []
        self.target = []
        for arg in args:
            self.add_item(arg)

    def __str__(self):
        if not self.items:
            return "This portfolio is empty."
        names = "This portfolio contains "
        for item in self.items[:-1]:
            names += get_name(item) + ", "
        names += get_name(self.items[-1]) + "."
        return names

    def add_item(self, ticker):
        name = get_name(ticker)
        if not name:
            return
        if ticker not in self.items:
            self.items.append(ticker)
            self.target.append(0)
            print(name + " has successfully been added to the portfolio.")
        else:
            print(name + " is already in the portfolio.")

    def remove_item(self, ticker):
        name = get_name(ticker)
        if not name:
            return
        if ticker in self.items:
            self.target.pop(self.items.index(ticker))
            self.items.remove(ticker)
            print(name + " has successfully been removed from the portfolio.")
        else:
            print(name + " was not in portfolio.")

    def add_multiple(self, *args):
        for arg in args:
            self.add_item(arg)

    def remove_multiple(self, *args):
        for arg in args:
            self.remove_item(arg)

    def all_prices(self):
        for item in self.items:
            print(get_name(item) + " has price $" + str(get_price(item)))

    def set_target(self, ticker, target_price):
        if ticker not in self.items:
            print("Please input a valid ticker that is in the portfolio.")
            return
        name = get_name(ticker)
        if check_positive(target_price):
            self.target[self.items.index(ticker)] = target_price
            print("Target price for " + name + " has been updated.")

    def target_update(self):
        for i in range(len(self.items)):
            if self.target[i]:
                name = get_name(self.items[i])
                if get_price(self.items[i]) >= self.target[i]:
                    print(name + " has reached the target price!")
                else:
                    print(name + " has not reached the target price.")

    def daily_update(self):
        for item in self.items:
            change = daily_change(item)
            name = get_name(item)
            if change < 0:
                print(name + " has decreased by " + str(abs(change)) + "% today.")
            else:
                print(name + " has increased by " + str(change) + "% today.")
