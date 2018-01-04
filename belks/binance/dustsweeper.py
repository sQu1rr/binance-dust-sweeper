import re

from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_MARKET
from binance.exceptions import BinanceAPIException, BinanceRequestException
from decimal import Decimal

from .account import Account
from .config import Config
from .dustcoin import DustCoin
from .exchange import Exchange
from .utils import input_bool

class DustSweeper:
    def __init__(self, headless=False):
        self.config = Config(headless)

        if not self.config.ready():
            raise Exception('Invalid Configuration')

        self.primary = []
        self.regex = None
        self.bnb_prompt = True
        self.test_order = False

        self.exchange = Exchange()
        self.account = Account()

        self._init_api()

        self.exchange.load(self.client)
        self.account.load(self.client)

    def _init_api(self):
        try:
            print('Connecting to API')
            self.client = Client(self.config.key, self.config.secret)
            print('Connected')
        except (BinanceAPIException, BinanceRequestException):
            print('Cannot connect to API')
            exit(1)

    def set_primary(self, coins):
        coins = [coin.upper().strip() for coin in coins]

        for coin in coins:
            if coin not in self.exchange.markets:
                print('Invalid Primary Ticker: ' + coin)
                exit(1)

        self.primary = coins

    def set_regex(self, regex):
        try:
            self.regex = re.compile(regex, re.IGNORECASE)
        except re.error as err:
            print('Invalid Regex Filter', err)
            exit(1)

        self.coinlist = []
        for coin in self.exchange.coins:
            if self.regex.match(coin) and coin not in self.primary:
                self.coinlist.append(coin)

        if len(self.coinlist) == 0:
            print('No coins to check')
            exit(1)

    def set_bnb_prompt(self, show):
        self.bnb_prompt = bool(show) and self.account.has_bnb()

    def set_test_order(self, test):
        self.test_order = bool(test)

    def set_min_balance(self, balance):
        self.min_balance = balance

    def run(self, dry_run=False, headless=False):
        if not dry_run and not self.test_order and not self.account.trade:
            print('Trading privileges missing')
            exit(1)

        self.dry_run = dry_run
        if headless:
            self.bnb_prompt = False

        dust = self._find_dust()
        print('Found ' + str(len(dust)) + ' coins with dust:')

        total_cost = Decimal(0.0)
        for dustcoin in dust:
            cost = dustcoin.est_cost_usdt()
            total_cost = total_cost + cost
            markets = dustcoin.get_dust_markets(self.primary)
            print('\t' + dustcoin.ticker, 'for', markets)

        cc = 'Cost' if total_cost >= 0 else 'Profit'
        c = total_cost if total_cost >= 0 else -total_cost
        c = c.quantize(Decimal('1.00'))
        print('Average Estimated {}: ~${}'.format(cc, c))

        if not headless:
            res = input_bool('Sweep these coins?', True)
            if not res:
                print('Exiting')
                exit(1)

        for dustcoin in dust:
            self._sweep_coin(dustcoin, headless)

    def _find_dust(self):
        dust = [self._dustcoin(coin) for coin in self.coinlist]
        return [coin for coin in dust if coin]

    def _dustcoin(self, coin):
        if coin in self.primary or coin not in self.account.coins:
            return None

        balance = self.account.coins[coin]['balance']
        dustcoin = DustCoin(coin, balance, self.exchange, self.account)
        dustcoin.set_min_balance(self.min_balance)
        dustcoin.calc(self.primary)

        dust_balance = dustcoin.is_dust_balance()

        return dustcoin if dustcoin.has_dust() or dust_balance else None

    def _sweep_coin(self, dustcoin, headless):
        balance = dustcoin.print_amount(dustcoin.balance)

        print('')
        print('---', dustcoin.ticker, '---', 'Balance:', balance)
        print('')

        markets = dustcoin.calc_sweep()
        for market in markets:
            self._print_market(market)

        allowed = [market for market in markets if market['allow']]

        market = None
        if not headless and len(allowed) > 1:
            market = self._prompt_market(allowed)
        elif len(allowed) > 0:
            market = allowed[0]
            if not headless:
                result = input_bool('Use the only option available?', True)
                if not result:
                    market = None

        if market is None:
            print('= SKIPPING COIN =')
            return

        self._do_sweep(market)

    def _print_market(self, result):
        dustcoin = result['dustcoin']
        market = result['market']
        dust = dustcoin.print_amount(result['dust'], market)
        step = self.exchange.coins[dustcoin.ticker][market]['step']

        print(market, ':', result['state'])
        print('\tDust: {}, Step: {}'.format(dust, step))

        ask = self.exchange.coins[dustcoin.ticker][market]['ask']
        bid = self.exchange.coins[dustcoin.ticker][market]['bid']

        if result['dust'] > 0:
            quantity = result['buy']
            price = dustcoin.print_amount(ask, market)
            total = dustcoin.print_amount(quantity * ask, market)
            print('\tBuy {} @ {} = {}'.format(quantity, price, total))

        quantity = result['sell']
        price = dustcoin.print_amount(bid, market)
        total = dustcoin.print_amount(quantity * bid, market)
        print('\tSell {} @ {} = {}'.format(quantity, price, total))

        cost = result['cost']
        balance = dustcoin.balance
        new_balance = dustcoin.balance + result['buy']
        new_balance = new_balance - result['buy'] * self.account.taker
        new_balance = new_balance - result['sell']

        b = dustcoin.print_amount(balance, market)
        nb = dustcoin.print_amount(new_balance, market)
        cc = 'Cost' if cost >= 0 else 'Profit'
        c = '${}'.format(cost if cost >= 0 else -cost)

        print('\tBalance {}, New Balance: {}, {}: {}'.format(b, nb, cc, c))

        print()

    def _prompt_market(self, markets):
        print('[0] Skip coin')
        for index, market in enumerate(markets):
            print('[{}] Convert to {}'.format(index + 1, market['market']))
        value = input('Defaults to [1]: ').strip()

        try:
            if value == '0':
                return None
            elif value == '':
                return markets[0]
            elif int(value) > 0 and int(value) <= len(markets):
                return markets[int(value) - 1]
            else:
                return self._prompt_market(markets)
        except ValueError:
            return self._prompt_market(markets)

    def _do_sweep(self, market):
        if self.dry_run:
            if market['buy'] > 0:
                print('=BUY {} {} @ MARKET PRICE='.format(
                    market['symbol'], market['buy']))
            if market['sell'] > 0:
                print('=SELL {} {} @ MARKET PRICE='.format(
                    market['symbol'], market['sell']))
        else:
            # BUY
            if market['buy'] > 0:
                self._bnb_prompt(False)

                if self.test_order:
                    print('=BUY {} {} @ MARKET PRICE='.format(
                        market['symbol'], market['buy']))

                    self.client.create_test_order(
                        symbol=market['symbol'],
                        side=SIDE_BUY,
                        type=ORDER_TYPE_MARKET,
                        quantity=market['buy'])
                else:
                    order = self.client.order_market_buy(
                        symbol=market['symbol'],
                        quantity=market['buy'])
                    print(order)

            # SELL
            if market['sell'] > 0:
                self._bnb_prompt(True)

                if self.test_order:
                    print('=SELL {} {} @ MARKET PRICE='.format(
                        market['symbol'], market['sell']))

                    self.client.create_test_order(
                        symbol=market['symbol'],
                        side=SIDE_SELL,
                        type=ORDER_TYPE_MARKET,
                        quantity=market['sell'])
                else:
                    order = self.client.order_market_sell(
                        symbol=market['symbol'],
                        quantity=market['sell'])
                    print(order)

    def _bnb_prompt(self, state):
        if not self.bnb_prompt:
            return

        print()
        if state:
            print('==========================================================')
            print('== !!!   TURN __ON__ YOUR BNB COMISSION DISCOUNT !!!    ==')
            print('==========================================================')
        else:
            print('==========================================================')
            print('== !!!   TURN __OFF__ YOUR BNB COMISSION DISCOUNT !!!   ==')
            print('==========================================================')
        print()

        while True:
            if input_bool('I have done it', False):
                break
