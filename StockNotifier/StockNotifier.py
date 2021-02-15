import pandas
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries  # 5 requests per minute, 500 requests per day limit
ts = TimeSeries(key='Q38Z3AM6PKFYOFXJ', output_format='pandas')


def get_name(ticker):
    # returns the official company name corresponding to the ticker
    try:
        return yf.Ticker(ticker).info['longName']
    except KeyError:
        print("Invalid Ticker! " + str(ticker) + " does not exist.")
        return


def get_price(ticker):
    name = get_name(ticker)
    if not name:
        return
    data, meta_data = ts.get_intraday(symbol=ticker, interval='1min', outputsize='full')
    return data['4. close'][0]


def inquire(ticker):
    # used to access methods from yf
    try:
        return yf.Ticker(ticker)
    except KeyError:
        print("Invalid Ticker! " + str(ticker) + "Information cannot be retrieved.")


def check_positive(price):
    try:
        assert (isinstance(price, float) or isinstance(price, int)) and price > 0
    except AssertionError:
        print("Invalid attempt! Target price must be a postive number.")
        return False
    return True


def price_alert(ticker, target_price):
    if check_positive(target_price):
        current_price = get_price(ticker)
        if not current_price:
            return
        name = get_name(ticker)
        if current_price >= target_price:
            print(name + " has reached the target price!")
        else:
            print(name + " has not reached the target price.")


def daily_output(ticker):
    if not get_name(ticker):
        return
    return ts.get_intraday(symbol=ticker, interval='60min', outputsize='full')


def daily_data(ticker):
    # do not use; limited api calls
    if not get_name(ticker):
        return
    return daily_output(ticker)[0]


def daily_meta_data(ticker):
    # do not use; limited api calls
    if not get_name(ticker):
        return
    return daily_output(ticker)[1]


def daily_display(ticker):
    name = get_name(ticker)
    if not name:
        return
    print(daily_data(ticker).head(16))


def percentage_change(ticker):
    name = get_name(ticker)
    if not name:
        return
    data, meta_data = daily_output(ticker)
    open = data['1. open'][15]
    close = data['4. close'][0]
    change = round((close - open) / open * 100, 2)
    date = meta_data['3. Last Refreshed'][:10]
    return change, date


def print_change(name, change, date):
    if change < 0:
        print(name + " has decreased by " + str(abs(change)) + "% overall on " + date + ".")
    else:
        print(name + " has increased by " + str(change) + "% overall on " + date + ".")


class Portfolio:
    def __init__(self, type=""):
        self.type = type
        self.items = []
        self.target = []

    def __str__(self):
        return str(self.type)

    def add_item(self, ticker):
        name = get_name(ticker)
        if not name:
            return
        if ticker not in self.items:
            self.items.append(ticker)
            print(name + " has successfully been added to the portfolio.")
        else:
            print(name + " is already in the portfolio.")
        self.target.append(0)

    def remove_item(self, ticker):
        name = get_name(ticker)
        if not name:
            return
        if ticker in self.items:
            index = self.items.index(ticker)
            self.items.remove(ticker)
            print(name + " has successfully been removed from the portfolio.")
        else:
            print(name + " was not in portfolio.")
        self.target.pop(index)

    def all_prices(self):
        for item in self.items:
            print(get_name(item) + " has price $" + str(get_price(item)))

    def set_target(self, ticker, target_price):
        name = get_name(ticker)
        if not name:
            return
        if check_positive(target_price):
            self.target[self.items.index(ticker)] = target_price
            print("Target price for " + name + " has been updated.")

    def target_update(self):
        # will only work with portfolio of size 5 or less due to limited number of free api requests
        for i in range(len(self.items)):
            if self.target[i]:
                price_alert(self.items[i], self.target[i])

    def percentage_update(self):
        # will only work with portfolio of size 5 or less due to limited number of free api requests
        for item in self.items:
            change, date = percentage_change(item)
            name = get_name(item)
            print_change(name, change, date)

    def large_update(self, amount=5):
        # will only work with portfolio of size 5 or less due to limited number of free api requests
        count = 0
        for item in self.items:
            change, date = percentage_change(item)
            name = get_name(item)
            if abs(change) >= amount:
                count += 1
                print_change(name, change, date)
        if not count:
            print("There was no update as large as the specified amount.")
