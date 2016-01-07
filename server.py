import decimal
import json
from flask import (Flask, render_template, request, jsonify,
                   session, redirect, url_for, abort)
from passlib.hash import pbkdf2_sha256
from utils.formatters import timefmt, moneyfmt, pctfmt
import config
from portfolio import init_portfolio

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
        uname = request.form['username']
        passwd = request.form['password']
        if (uname is not None and pbkdf2_sha256.verify(passwd, app.config['PASSWORD'])):
            session['uname'] = uname
            return redirect(url_for('index'))
    abort(401)


@app.route('/logout')
def logout():
    session.pop('uname', None)
    return redirect(url_for('login'))


@app.route('/')
def index():
    if session.get('uname', None) is None:
        return redirect(url_for('login'))
    return render_template('portfolio.html', portfolio=init_portfolio(config.POSITIONS_FILE))

@app.route('/positions')
def get_positions():
    if session.get('uname', None) is None:
        return redirect(url_for('login'))
    return jsonify(portfolio=init_portfolio(config.POSITIONS_FILE))

app.run(host='0.0.0.0', debug=True)
