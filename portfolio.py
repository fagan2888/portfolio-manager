"""Builds a portfolio object containing asset allocation details."""

import time
import decimal
from googlefinance import getQuotes


DEC = decimal.Decimal
USDCAD = DEC(getQuotes('CURRENCY:USDCAD')[0]['LastTradePrice'])


def init_portfolio(filename):
    """Returns a portfolio object containing positional, categorical, and
     portfolio totals.

     Usage:
     call init_portfolio(filename) with a csv file with at LEAST the
     following columns:
        ticker,qty,target%,category,currency
    """

    portfolio = {
        'asof': time.time(),
        'positions': {},
        'categories': {},
        'total': DEC(0)
    }
    with open(filename) as f:
        keys = f.readline().strip().split(',')
        for line in f:
            position = dict(zip(keys, line.strip().split(',')))
            position['qty'] = DEC(position['qty'])
            position['target%'] = DEC(position['target%']) / 100
            portfolio['positions'][position['ticker']] = position
            portfolio['categories'][position['category']] = {
                'name': position['category'],
                'mktvalue': DEC(0),
                'target%': position['target%']
            }

    _populate_market_values(portfolio)
    _populate_asset_allocations(portfolio)
    return portfolio


def _populate_market_values(portfolio):
    """Populates positional, categorical, and portfolio market values."""

    quotes = getQuotes(portfolio['positions'].keys())
    for quote in quotes:
        ticker = quote['StockSymbol']
        if ticker not in portfolio['positions']:
            ticker = quote['Index'] + ':' + ticker
        position = portfolio['positions'][ticker]
        category = portfolio['categories'][position['category']]
        position['mktvalue'] = position['qty'] * DEC(quote['LastTradePrice'])
        if position['currency'] == 'USD':
            position['mktvalue'] *= USDCAD
        category['mktvalue'] += position['mktvalue']
        portfolio['total'] += position['mktvalue']


def _populate_asset_allocations(portfolio):
    """Populates categorical current and target allocations."""

    for category in portfolio['categories'].values():
        category['current%'] = category['mktvalue'] / portfolio['total']
        category['target'] = category['target%'] * portfolio['total']
        category['rebalance'] = _needs_rebalance(category)


def _needs_rebalance(category):
    """Determines whether the given asset category needs to be rebalanced.

    Uses the Swedroe 5/25 Rebalancing Rule. See here:
    http://awealthofcommonsense.com/larry-swedroe-525-rebalancing-rule/
    """

    target_pct, current_pct = category['target%'], category['current%']
    pct_diff = abs(target_pct - current_pct)
    return (
        (target_pct >= 0.2 and pct_diff > 0.05)
        or
        (target_pct < 0.2 and pct_diff > DEC(0.25) * target_pct)
    )
