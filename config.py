#!/usr/bin/env python3

import argparse
import os

from belks.binance.config import Config

parser = argparse.ArgumentParser(description='Configuration')
parser.add_argument('--new', action='store_true', dest='overwrite')
parser.add_argument('--rm', action='store_true', dest='remove')
args = parser.parse_args()

config = Config(True)

if config.loaded():
    print('Existing configuration found')

    if args.remove:
        print('Removing...')
        os.remove('config.ini')

    elif args.overwrite:
        config.configure(True)

elif not args.remove:
    config.configure(True)
