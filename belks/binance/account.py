from decimal import Decimal

class Account:
    def load(self, client):
        res = client.get_account()

        self.coins = {}

        self.maker = Decimal(res['makerCommission']) / Decimal(10000.0)
        self.taker = Decimal(res['takerCommission']) / Decimal(10000.0)

        self.trade = res['canTrade']

        for balance in res['balances']:
            if Decimal(balance['free']) > 0:
                self._parse_coin(balance)

    def _parse_coin(self, balance):
        coin = {}

        coin['ticker'] = balance['asset']
        coin['balance'] = Decimal(balance['free'])

        self.coins[coin['ticker']] = coin

    def has_bnb(self):
        return ('BNB' in self.coins) and (self.coins['BNB']['balance'] > 0)
