import decimal
from googlefinance import getQuotes


DEC = decimal.Decimal
USDCAD = DEC(getQuotes('CURRENCY:USDCAD')[0]['LastTradePrice'])


def init_portfolio(filename):
    portfolio = {
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
    for category in portfolio['categories'].values():
        category['current%'] = category['mktvalue'] / portfolio['total']
        category['target'] = category['target%'] * portfolio['total']
        category['rebalance'] = _needs_rebalance(category)


def _needs_rebalance(category):
    pct_diff = abs(category['current%'] - category['target%'])
    return (
        (category['target%'] < 0.2 and pct_diff < 0.05)
        or
        (category['target%'] >= 0.2 and pct_diff > DEC(0.25) * category['target%'])
    )
