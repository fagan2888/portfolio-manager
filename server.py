import decimal
import json
from flask import Flask, render_template, request, session, redirect, url_for, abort
from passlib.hash import pbkdf2_sha256
from utils.formatters import timefmt, moneyfmt, pctfmt
import config
import portfolio

app = Flask(__name__)
app.config.from_object(config)
app.jinja_env.filters['time'] = timefmt
app.jinja_env.filters['money'] = moneyfmt
app.jinja_env.filters['pct'] = pctfmt


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
            <form action="" method="post">
                <input type="text" placeholder="Username" name="username">
                <input type="password" placeholder="Password" name="password">
                <input type="submit" value="Login">
            </form>
        '''
    else:
        print 'here'
        print app.config
        uname = request.form['username']
        passwd = request.form['password']
        if uname is not None and pbkdf2_sha256.verify(passwd, app.config['PASSWORD']):
            session['uname'] = uname
            return redirect(url_for('index'))
    abort(401)


@app.route('/')
def index():
    if session.get('uname', None) is None:
        return redirect(url_for('login'))

    if request.args.get('force_refresh', '') != '':
        positions = portfolio.init_portfolio(config.POSITIONS_FILE)
    else:
        with open('positions.json') as f:
            positions = json.loads(f.read(), parse_float=decimal.Decimal)
    return render_template('portfolio.html', positions=positions)


app.run(debug=True)
