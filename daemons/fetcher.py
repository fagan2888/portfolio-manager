"""Saves a copy of the portfolio every day at 6:00 PM. """

import os
import time
import simplejson as json
import schedule
import portfolio
import config


def save_portfolio():
    """Saves a copy of the portfolio. """

    ymd = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    positions = portfolio.init_portfolio(config.POSITIONS_FILE)
    positions_json = json.dumps(positions, use_decimal=True)
    positions_filename = ('%s-positions.json' % (ymd, ))

    try:
        os.makedirs('archive')
        os.makedirs('stats')
    except OSError:
        pass

    with open('archive/' + positions_filename, 'w') as f:
        f.write(positions_json)

    with open('stats/mktval.txt', 'w') as f:
        f.write(ymd + ',' + str(positions['total']) + '\n')

    with open('stats/catmktval.txt', 'w') as f:
        for category in positions['categories']:
            f.write((
                ymd + ',' +
                category['name'] + ',' +
                str(category['mktvalue']) +
                '\n'
            ))

    with open('stats/posmktval.txt', 'w') as f:
        for ticker, position in positions['positions'].iteritems():
            f.write((
                ymd + ',' +
                ticker + ',' +
                str(position['qty']) + ',' +
                str(position['mktvalue']) +
                '\n'
            ))


save_portfolio()
schedule.every().day.at('18:00').do(save_portfolio)

while True:
    schedule.run_pending()
    time.sleep(1)
