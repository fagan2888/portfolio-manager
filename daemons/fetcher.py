"""Saves a copy of the portfolio every day at 9:00. """

import time
import simplejson as json
import schedule
import portfolio
import config


def save_portfolio():
    """Saves a copy of the portfolio. """

    positions = portfolio.init_portfolio(config.POSITIONS_FILE)
    positions_json = json.dumps(positions, use_decimal=True)

    with open('positions.json', 'w') as f:
        f.write(positions_json)


save_portfolio()
schedule.every().day.at('9:00').do(save_portfolio)

while True:
    schedule.run_pending()
    time.sleep(1)