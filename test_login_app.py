from flask import Flask, render_template, url_for, abort, redirect, request
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

from data.db_session import create_session, global_init
from data.users import User
from data.stocks import Stock
from data.companies import Company
import os


global_init(os.path.join("db", "database.db"))


login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return create_session().query(User).get(user_id == user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = 1
        user = load_user(user_id)
        login_user(user)
        return redirect(url_for('dashboard'))
    return '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
  <form method='POST'>
    <input type="text" placeholder="Username" required>
    <input type="password" placeholder="Password" required>
    <button type="submit">Login</button>
  </form>
</body>
</html>
'''


@app.route('/dashboard')
@login_required
def dashboard():
    return f'Привет, {current_user.name}! Это защищенная страница.'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


def add_user():
    session = create_session()
    user1 = User(name="Newuser1")
    user1.set_password("1")
    session.add(user1)
    session.commit()


if __name__ == '__main__':
    # add_user()
    print(create_session().query(User).all())
    app.run(port=5001, debug=True)