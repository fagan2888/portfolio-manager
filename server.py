import decimal
import json
from flask import Flask, render_template
from utils.formatters import timefmt, moneyfmt, pctfmt

app = Flask(__name__)
app.jinja_env.filters['time'] = timefmt
app.jinja_env.filters['money'] = moneyfmt
app.jinja_env.filters['pct'] = pctfmt


@app.route('/')
def index():
    with open('positions.json') as f:
        positions = json.loads(f.read(), parse_float=decimal.Decimal)
    print positions['categories']
    return render_template('portfolio.html', positions=positions)


app.run(debug=True)
