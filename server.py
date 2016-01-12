import decimal
import json
from shutil import move
from os import remove
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
    return render_template('index.html', portfolio=init_portfolio(config.POSITIONS_FILE))


@app.route('/positions', methods=['GET'])
def get_positions():
    if session.get('uname', None) is None:
        return redirect(url_for('login'))
    return jsonify(portfolio=init_portfolio(config.POSITIONS_FILE))

@app.route('/positions', methods=['POST'])
def set_positions():
    if session.get('uname', None) is None:
        return redirect(url_for('login'))
    new_positions = request.get_json()['positions']
    with open(config.POSITIONS_FILE, 'r') as old_file:
        with open('tmp.txt', 'w') as new_file:
            keys = old_file.readline().strip().split(',')
            new_file.write(','.join(keys) + '\n')
            for line in old_file:
                old_position = dict(zip(keys, line.strip().split(',')))
                ticker = old_position['ticker']
                if ticker in new_positions:
                    old_position['qty'] = new_positions[ticker]['qty']
                    if old_position['qty'] != 0:
                        for k in keys[:-1]:
                            new_file.write(str(old_position[k]) + ',')
                        new_file.write(old_position[keys[len(keys) - 1]] + '\n')
                else:
                    new_file.write(line + '\n')
    remove(config.POSITIONS_FILE)
    move('tmp.txt', config.POSITIONS_FILE)
    return '', 200

app.run(host='0.0.0.0', debug=True)
