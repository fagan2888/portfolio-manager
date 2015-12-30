"""Saves a copy of the portfolio every day at 9:00. """

import os
import time
import simplejson as json
import schedule
import portfolio
import config


def save_portfolio():
    """Saves a copy of the portfolio. """

    positions = portfolio.init_portfolio(config.POSITIONS_FILE)
    positions_json = json.dumps(positions, use_decimal=True)

    if os.path.isfile('positions.json'):
        try:
            os.makedirs('archive')
        except OSError:
            pass
        os.rename('positions.json',
                  'archive/positions.json.%s' % (int(time.time()),))
    with open('positions.json', 'w') as f:
        f.write(positions_json)


save_portfolio()
schedule.every().day.at('9:00').do(save_portfolio)

while True:
    schedule.run_pending()
    time.sleep(1)
