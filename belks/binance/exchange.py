from decimal import Decimal

def _find_step(filters):
    for element in filters:
        if 'stepSize' in element:
            return Decimal(element['stepSize'])

    print('Warning: USING DEFAULT STEP SIZE')
    return 0.001 # default

class Exchange:
    def load(self, client):
        self.coins = {}
        self.markets = {}
        self.symbols = {}

        res = client.get_exchange_info()
        for symbol in res['symbols']:
            if symbol['status'] == 'TRADING':
                self._parse_coin(symbol)

        res = client.get_orderbook_tickers()
        for symbol in res:
            self._update_coin(symbol)

    def _parse_coin(self, symbol):
        coin = {}

        coin['ticker'] = symbol['baseAsset']
        coin['market'] = symbol['quoteAsset']
        coin['step'] = _find_step(symbol['filters'])

        if coin['ticker'] not in self.coins:
            self.coins[coin['ticker']] = {}

        if coin['market'] not in self.markets:
            self.markets[coin['market']] = {}

        self.symbols[coin['ticker'] + coin['market']] = coin
        self.coins[coin['ticker']][coin['market']] = coin
        self.markets[coin['market']][coin['ticker']] = coin

    def _update_coin(self, symbol):
        if symbol['symbol'] in self.symbols:
            coin = self.symbols[symbol['symbol']]
            coin['bid'] = Decimal(symbol['bidPrice'])
            coin['ask'] = Decimal(symbol['askPrice'])

    def to_usdt(self, market, amount):
        if market == 'USDT':
            return Decimal(amount).quantize(Decimal('1.00'))

        bid = self.markets['USDT'][market]['bid']
        ask = self.markets['USDT'][market]['ask']
        return Decimal(amount * (bid + ask) / 2).quantize(Decimal('1.00'))
