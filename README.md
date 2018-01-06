# Binance Dust Sweeper

## Installation

Requires [python-binance](https://github.com/sammchardy/python-binance) and
[simple-crypt](https://github.com/andrewcooke/simple-crypt)
installed:

```bash
pip3 install --user python-binance simple-crypt
```

### Windows
The easiest way to install on Windows is to use [Miniconda](https://conda.io/miniconda.html). Download and install either the Python 3.6 or Python 2.7 version. Once installed go to the directory where you cloned the Binance Dust Sweeper repo. Then type:

```bash
conda env create
```

Once finished activate the environment using:

```bash
activate binance-dust-sweeper
```

You are now ready to run dustsweeper using:

```bash
python dustsweeper.py
```

See additional usage instructions below.


## Copy-Paste instructions from reddit (raw comment)


Writing instructions is definitely not something I'm good at, hence the repository is missing them. In brief, after installing the dependencies, simply run the script with

```bash
./dustsweeper.py --dry-run
```

and follow the interactive process. The script will not commit anything when --dry-run option is set. The script will prompt for the API key and secret which you can get form the binance account page.

I personally use

```bash
./dustweeper.py -p btc,bnb
```

^ that lets me sell other "primary" coins like eth and usdt and assumes i don't want to convert into them. (i only use btc and bnb as base coins on binance)

You don't need to give the script the priveleges to commit the orders if you don't want to. You can simply execute yourself the proposed amounts which you get by dry-running or --test-order.

This will only work when you DISABLE the bnb discount for BUY orders (the script will prompt you to do so and wait till you do)

Note: if you decide to save your API key and secret they will be securely ecnrypted. You don't have to save them

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
