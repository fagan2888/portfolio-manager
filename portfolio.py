"""Builds a portfolio object containing asset allocation details."""

import time
import decimal
from stockretriever import get_current_info

DEC = decimal.Decimal


def init_portfolio(filename):
    """Returns a portfolio object containing positional, categorical, and
     portfolio totals.

     Usage:
     call init_portfolio(filename) with a csv file with at LEAST the
     following columns:
        ticker,qty,target%,category,currency
    """

    portfolio = {
        'asof': int(time.time()),
        'positions': {},
        'categories': {},
        'total': DEC(0),
        'usdcad': DEC(get_current_info(['USDCAD=X'])['LastTradePriceOnly'])
    }
    with open(filename) as f:
        keys = f.readline().strip().split(',')
        for line in f:
            position = dict(zip(keys, line.strip().split(',')))
            position['qty'] = DEC(position['qty'])
            position['target%'] = DEC(position['target%']) / 100
            portfolio['positions'][position['ticker']] = position
            category = portfolio['categories'].setdefault(
                position['category'], {
                    'name': position['category'],
                    'mktvalue': DEC(0),
                    'target%': position['target%'],
                    'tickers': []
                }
            )
            category['tickers'].append(position['ticker'])

    _populate_market_values(portfolio)
    _populate_asset_allocations(portfolio)
    return portfolio


def _populate_market_values(portfolio):
    """Populates positional, categorical, and portfolio market values."""

    quotes = get_current_info(portfolio['positions'].keys())
    for quote in quotes:
        ticker = quote['symbol']
        price = DEC(quote['LastTradePriceOnly'])
        position = portfolio['positions'][ticker]
        category = portfolio['categories'][position['category']]
        position['mktvalue'] = position['qty'] * price
        if quote['Currency'] == 'USD':
            position['mktvalue'] *= portfolio['usdcad']
        category['mktvalue'] += position['mktvalue']
        portfolio['total'] += position['mktvalue']


def _populate_asset_allocations(portfolio):
    """Populates categorical current and target allocations."""

    for category in portfolio['categories'].values():
        category['current%'] = category['mktvalue'] / portfolio['total']
        category['target'] = category['target%'] * portfolio['total']
        category['rebalance'] = _needs_rebalance(category)
        category['sortkey'] = category['name']
        if category['name'] == 'Other':
            category['sortkey'] = 'ZZ'
    portfolio['categories'] = portfolio['categories'].values()
    portfolio['categories'].sort(key=lambda c: c['sortkey'])
    for category in portfolio['categories']:
        del category['sortkey']


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
