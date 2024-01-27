from flask import Flask, render_template, url_for, abort, redirect
from flask_login import LoginManager

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
    return create_session().query(User).get(user_id == user_id).first()


@app.route('/')
def index_page():
    return render_template('index_page.html')


@app.route('/e403')
def e403():
    return redirect(abort(403))

@app.route('/e404')
def e404():
    return redirect(abort(404))

@app.route('/e418')
def e418():
    return redirect(abort(418))

@app.route('/e500')
def e500():
    return redirect(abort(500))


@app.route('/cost')
def cost_page():
    return render_template('cost_page.html')

@app.route('/cover')
def cover_page():
    return render_template('cover_page.html')

@app.route('/dashboard/<company_token>')
def dashboard_page(company_token):
    free_companies = [
        {"title": "Google", "active": False, "token": "GOOG"},
        {"title": "Apple", "active": False, "token": "AAPL"}
    ]
    for company in free_companies:
        if company["token"] == company_token:
            company["active"] = True
    paid_companies = [
        {"title": "Yandex", "active": False, "token": "YNDX"}, # РАБотает
        {"title": "QIWI", "active": False, "token": "QIWI"}, # РАБотает
        {"title": "Татнефть", "active": False, "token": "OTC:OAOFY"}, # РАБотает
        {"title": "Группа Эталон", "active": False, "token": "ETLN"}, # РАБотает
        {"title": "Bitcoin", "active": False, "token": "BTCUSD"},
        {"title": "NVIDIA Corporation", "active": False, "token": "NVDA"},
        {"title": "Amazon", "active": False, "token": "AMZN"},
        {"title": "PayPal", "active": False, "token": "PYPL"},
        {"title": "UBER", "active": False, "token": "UBER"},
    ]
    for company in paid_companies:
        if company["token"] == company_token:
            company["active"] = True
    data = {
        "free_companies": free_companies,
        "paid_companies": paid_companies,
        "company_token": company_token
    }
    return render_template('dashboard_page.html', **data)

@app.route("/futer")
def futer_page():
    return render_template('futer_page.html')

@app.route("/futer2")
def futer_page2():
    return render_template('futer_page2.html')

@app.route("/logiin")
def login_page():
    return render_template('login_page.html')

@app.route("/ordering")
def ordering_page():
    return render_template('ordering_page.html')

@app.errorhandler(404)
def error404page(error):
    data = {
        "title": "Страница не найдена",
        "image": url_for('static', filename='images/error_images/error404image.jpeg'),
        "description": "Она точно точно тут была прям зуб даю."
    }
    return render_template('error_page.html', **data), 404


@app.errorhandler(403)
def error403page(error):
    data = {
        "title": "Не уполномочено",
        "image": url_for('static', filename='images/error_images/error403image.jpg'),
        "description": "Разрешения не получено."
    }
    return render_template('error_page.html', **data), 403


@app.errorhandler(418)
def error418page(error):
    data = {
        "title": "Я - чайник",
        "image": url_for('static', filename='images/error_images/error418image.jpeg'),
        "description": "Разработчики ушли попить чая."
    }
    return render_template('error_page.html', **data), 418


@app.errorhandler(500)
def error500page(error):
    data = {
        "title": "Упс, в сервере что-то пошло не так",
        "image": url_for('static', filename='images/error_images/error500image.jpg'),
        "description": "Разработчики сегодня без кофе."
    }
    return render_template('error_page.html', **data), 500


if __name__ == '__main__':
    app.run(debug=True)
