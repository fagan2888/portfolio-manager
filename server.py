from shutil import move
from os import remove
from functools import wraps
from flask import (Flask, render_template, request, jsonify,
                   session, redirect, url_for, abort)
from passlib.hash import pbkdf2_sha256
import config
from portfolio import init_portfolio

app = Flask(__name__)
app.config.from_object(config)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('uname', None) is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return app.send_static_file('login.html')
    else:
        uname = request.form['username']
        passwd = request.form['password']
        if (uname is not None and
                pbkdf2_sha256.verify(passwd, app.config['PASSWORD'])):
            session['uname'] = uname
            return redirect(url_for('index'))
    abort(401)


@app.route('/logout')
def logout():
    session.pop('uname', None)
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    return render_template(
        'index.html',
        portfolio=init_portfolio(config.POSITIONS_FILE)
    )


@app.route('/positions', methods=['GET'])
@login_required
def get_positions():
    return jsonify(portfolio=init_portfolio(config.POSITIONS_FILE))


@app.route('/positions', methods=['POST'])
@login_required
def set_positions():
    new_positions = request.get_json()['positions']
    with open(config.POSITIONS_FILE, 'r') as old_file:
        with open('tmp.txt', 'w') as new_file:
            keys = old_file.readline().strip().split(',')
            num_keys = len(keys)
            new_file.write(','.join(keys) + '\n')
            for line in old_file:
                old_position = dict(zip(keys, line.strip().split(',')))
                ticker = old_position['ticker']
                if ticker in new_positions:
                    old_position['qty'] = new_positions[ticker]['qty']
                    if old_position['qty'] != 0:
                        for k in keys[:-1]:
                            new_file.write(str(old_position[k]) + ',')
                        new_file.write(old_position[keys[num_keys - 1]] + '\n')
                else:
                    new_file.write(line + '\n')
    remove(config.POSITIONS_FILE)
    move('tmp.txt', config.POSITIONS_FILE)
    return '', 200

app.run(host='0.0.0.0', debug=True)
