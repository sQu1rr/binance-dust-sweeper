import functools
import math

from decimal import Decimal
from operator import itemgetter

class DustCoin:
    def __init__(self, coin, balance, exchange, account):
        self.ticker = coin
        self.balance = balance
        self.exchange = exchange
        self.account = account

    def set_min_balance(self, min_balance):
        self.min_balance = min_balance

    def calc(self, primary):
        self.markets = {}

        for market in self.exchange.markets:
            result = self._calc_market(market, primary)
            self.markets[market] = result

    def _calc_market(self, market, primary):
        if market not in self.exchange.coins[self.ticker]:
            return None # no market

        result = {}
        result['dustcoin'] = self
        result['symbol'] = self.ticker + market
        result['market'] = market
        result['dust'] = self._get_dust(market)
        result['buy'] = self._calc_buy(market)
        result['sell'] = self._calc_sell(market)
        result['cost'] = self._calc_cost(market)
        result['allow'] = self._allow(result, primary)

        return result

    def _calc_buy(self, market):
        dust = self._get_dust(market)
        return Decimal(0) if dust == 0 else dust / self.account.taker

    def _calc_sell(self, market):
        buy = self._calc_buy(market)

        if self.is_dust_balance():
            return self.balance + buy - buy * self.account.taker

        coin = self.exchange.coins[self.ticker][market]
        return buy - coin['step']

    def _calc_cost(self, market):
        ask = self.exchange.coins[self.ticker][market]['ask']
        bid = self.exchange.coins[self.ticker][market]['bid']
        cost = self._calc_buy(market) * ask - self._calc_sell(market) * bid
        return self.exchange.to_usdt(market, cost)

    def _get_dust(self, market):
        coin = self.exchange.coins[self.ticker][market]
        qty = self.balance / coin['step']
        return (qty - math.floor(qty)) * coin['step']

    def has_dust(self):
        return len(self.get_dust_markets()) > 0

    def get_dust_markets(self, primary=None):
        if primary is None:
            primary = self.markets.keys()

        return [(market, str(result['dust']),) for market, result in
                self.markets.items() if result is not None
                and result['dust'] > 0 and market in primary]

    def calc_sweep(self):
        markets = []
        for market, result in self.markets.items():
            if result is not None:
                markets.append(result)

        return sorted(markets, key=functools.cmp_to_key(self._comparator))

    def _comparator(self, lhs, rhs):
        if lhs['cost'] == rhs['cost']:
            if lhs['market'] not in self.account.coins:
                return 1
            if rhs['market'] not in self.account.coins:
                return -1

        return lhs['cost'] - rhs['cost']

    def _allow(self, result, primary):
        market = result['market']
        dust_balance = self.is_dust_balance()
        coins = self.account.coins

        if result['dust'] == 0 and not dust_balance:
            result['state'] = 'SKIPPING: No dust for this market'
            return False

        if result['market'] not in primary:
            result['state'] = 'SKIPPING: Market not in PRIMARY'
            return False

        if result['market'] not in coins and result['dust'] > 0:
            result['state'] = 'SKIPPING: Account does not own any ' + market
            return False

        ask = self.exchange.coins[self.ticker][market]['ask']
        buy = result['buy'] * ask
        if market in coins and buy > coins[market]['balance']:
            req = 'REQUIRED: ' + self.print_amount(buy, market)
            result['state'] = 'SKIPPING: Not enough funds on the account ' + req
            return False

        result['state'] = 'Possible'
        return True

    def is_dust_balance(self):
        return self.balance * self.btc_price() < self.min_balance

    def btc_price(self):
        ask = self.exchange.coins[self.ticker]['BTC']['ask']
        bid = self.exchange.coins[self.ticker]['BTC']['bid']
        return (ask + bid) / 2

    def usdt_amount(self, amount):
        return self.exchange.to_usdt('BTC', amount * self.btc_price())

    def print_amount(self, amount, market=None):
        if market is not None:
            usdt = self.exchange.to_usdt(market, amount)
        else:
            usdt = self.usdt_amount(amount)
        return '{} (${})'.format(amount if amount != 0 else '0.00', usdt)

    def est_cost_usdt(self):
        costs = [result['cost'] for market, result
                in self.markets.items() if result is not None]
        return sum(costs) / len(costs)
