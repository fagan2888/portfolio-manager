"""Sends an email every Sunday if your portfolio needs rebalancing. """

import time
import schedule
import requests
from jinja2 import Template
import config
import portfolio

TMPL = Template('{{ num_to_rebalance }} position(s) need to be rebalanced.')


def rebalance_email():
    """Sends an email if your portfolio needs rebalancing. """

    positions = portfolio.init_portfolio(config.POSITIONS_FILE)
    categories = positions['categories'].values()
    num_to_rebalance = len([category for category in categories
                            if category['rebalance']])
    if num_to_rebalance > 0:
        email_body = TMPL.render(num_to_rebalance=num_to_rebalance)
        requests.post(
            config.MAILGUN_API_URL,
            auth=('api', config.MAILGUN_API_KEY),
            data={'from': config.EMAIL_FROM,
                  'to': [config.EMAIL_TO],
                  'subject': 'Your Portfolio Needs Rebalancing',
                  'text': email_body})

schedule.every().sunday.at('9:00').do(rebalance_email)

while True:
    schedule.run_pending()
    time.sleep(1)
