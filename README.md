# Binance Dust Sweeper

## Installation

Requires [python-binance](https://github.com/sammchardy/python-binance) and
[simple-crypt](https://github.com/andrewcooke/simple-crypt)
installed:

```bash
pip3 install --user python-binance simple-crypt
```

## Usage

Interactive interface will guide you through
```bash
./dustsweeper.py
```

You can specify your primiary currencies
```bash
./dustsweeper.py -p btc,bnb
```

You can filter the currencies to convert
```bash
./dustsweeper.py -f 'xlm'
```

Use --dry-run or --test-order for test orders
```bash
./dustsweeper.py --dry-run
./dustsweeper.py --test-order
```

You can tweak the "dust" balance for your sh!tcoins
```bash
./dustsweeper.py -b 0.001 #BTC
```

## Screenshot
![alt tag](https://raw.github.com/sQu1rr/binance-dust-sweeper/assets/img/screenshot1.png)
![alt tag](https://raw.github.com/sQu1rr/binance-dust-sweeper/assets/img/screenshot2.png)

## If you found the utility useful

*BTC*: 15WVMwYG7SKW7oTuxxTnJuWsd94on3emU8

*BCH*: 1G9EwZKxodUDWaU6sckiYBKS4xYGdTVVL5

*LTC*: LX7W9SA2tPLj2a6YF1tiK5vEZSWCAR8ikH

*ETH*: 0xe1391e885cc8d6cad7777829026a422e163affcf

*NEO*: AbZJJFhGEu5AQRYZxtNdnjd6J4zUx8zS83

*XMR*: 44YfBWCVfJXRzQyagP3T7oN7trDn3AfwZRe3kWKW3SQmCkZpAtabRXxSCFLvowg4fUU8CEYzjGVcoRhqWeZTUDaD3hMG6pi
