"""Sends an email every Sunday if your portfolio needs rebalancing. """

import time
import schedule
import requests
from jinja2 import Template
import config
import portfolio

TMPL = Template(('{{ num_to_rebalance }} position(s) need to be rebalanced. '
                 'Buy more {{ categories_to_rebalance }}.'))


def rebalance_email():
    """Sends an email if your portfolio needs rebalancing. """

    positions = portfolio.init_portfolio(config.POSITIONS_FILE)
    categories = positions['categories']
    categories_to_rebalance = [category for category in categories
                               if category['rebalance']]
    categories_to_buy = [category['name'] for category in categories_to_rebalance
                         if category['target%'] > category['current%']]
    num_to_rebalance = len(categories_to_rebalance)
    if num_to_rebalance > 0:
        email_body = TMPL.render(
            num_to_rebalance=num_to_rebalance,
            categories_to_rebalance=', '.join(categories_to_buy)
        )
        requests.post(
            config.MAILGUN_API_URL,
            auth=('api', config.MAILGUN_API_KEY),
            data={'from': config.EMAIL_FROM,
                  'to': [config.EMAIL_TO],
                  'subject': 'Your Portfolio Needs Rebalancing',
                  'text': email_body})

schedule.every().sunday.at('9:00').do(rebalance_email)
rebalance_email()
while True:
    schedule.run_pending()
    time.sleep(1)
