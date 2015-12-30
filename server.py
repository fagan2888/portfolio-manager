import decimal
import json
from flask import Flask, render_template, request
from utils.formatters import timefmt, moneyfmt, pctfmt
import config
import portfolio

app = Flask(__name__)
app.jinja_env.filters['time'] = timefmt
app.jinja_env.filters['money'] = moneyfmt
app.jinja_env.filters['pct'] = pctfmt


@app.route('/')
def index():
    if request.args.get('force_refresh', '') != '':
        positions = portfolio.init_portfolio(config.POSITIONS_FILE)
    else:
        with open('positions.json') as f:
            positions = json.loads(f.read(), parse_float=decimal.Decimal)
    return render_template('portfolio.html', positions=positions)


app.run(debug=True)
