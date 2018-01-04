#!/usr/bin/env python3

import argparse

from belks.binance.dustsweeper import DustSweeper

PRIMARY = 'BTC,BNB,ETH,USDT'

parser = argparse.ArgumentParser(description='Adjust Coin Quantities')
parser.add_argument('-p', '--primary', dest='primary', default=PRIMARY)
parser.add_argument('-f', '--filter', dest='regex', default='.*')
parser.add_argument('-b', '--dust-balance', dest='min_balance', default=0.001)
parser.add_argument('--no-discount', action="store_false", dest='bnb_prompt')
parser.add_argument('--no-confirm', action="store_true", dest='headless')
parser.add_argument('--dry-run', action="store_true", dest='dry_run')
parser.add_argument('--test-order', action="store_true", dest='test_order')
args = parser.parse_args()

helper = DustSweeper(args.headless)

helper.set_primary(args.primary.split(','))
helper.set_regex(args.regex)
helper.set_bnb_prompt(args.bnb_prompt)
helper.set_test_order(args.test_order)
helper.set_min_balance(args.min_balance)

helper.run(args.dry_run, args.headless)
