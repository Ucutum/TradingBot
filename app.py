from flask import Flask, render_template, url_for, abort, redirect, request, flash
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

from data.db_session import create_session, global_init
from data.users import User
from data.stocks import Stock
from data.companies import Company
import os
import csv
import subprocess

from forms.login_form import LogInForm
from forms.singup_form import SingUpForm
import json


with open('settings.json', 'r') as f:
    settings = json.load(f)


global_init(os.path.join("db", "database.db"))
if settings["system"] == "Windows":
    run_command = ["./TradingBot.exe"]
elif settings["system"] == "Linux":
    run_command = ["./TradingBot"]
else:
    run_command = ["./TradingBot"] 


login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    session = create_session()
    return session.query(User).get(int(user_id))


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


@app.route('/subscription_purchased')
def subscription_purchased_page():
    if not current_user.is_authenticated:
        return abort(403)
    return render_template('subscription_purchased_page.html')


@app.route('/cost', methods=['GET', 'POST'])
def cost_page():
    if current_user.is_authenticated:
        if current_user.subscription:
            return redirect(url_for('subscription_purchased_page'))
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash("Войдите в систему для покупки")
            return redirect(url_for('login_page'))
        else:
            session = create_session()
            user = session.query(User).get(current_user.id)
            user.subscription = True
            session.commit()
            return redirect(url_for('subscription_purchased_page'))
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

    paid_companies = list()
    with open('all.csv', newline='', encoding="utf-8") as f:
        spamreader = csv.reader(f, delimiter=';')

        for row in spamreader:
            paid_companies.append({"title" : row[0], "active" : False, "token" : row[1]})

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
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "gdata", "package_NASDAQ.txt")
    subprocess.run(run_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    shares = list()
    data = dict()

    with open(path, "r", newline="") as f:
        lines = f.readlines()
        for item in lines:
            title, cost = item.split()
            if title == "MONEY": data[title] = cost
            else: shares.append({"title" : title, "cost" : cost})

    data['current_shares'] = shares

    return render_template('futer_page.html', **data)

@app.route("/ai_strategy")
def ai_strategy_page():
    with open("all.csv") as f:
        companies = [i for i in csv.reader(f, delimiter=";")]
    graphs = [
        {"name": i[0],
         "img":f"graph/{i[1]}_graph.png"}
               for i in companies]
    return render_template('ai_strategy.html', graphs=graphs)

@login_manager.unauthorized_handler
@app.route("/login", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("cover_page"))
    form = LogInForm()
    if request.method == "POST":
        session = create_session()
        user = session.query(User).filter(User.name == form.username.data).first()
        if not user:
            flash("Неверное имя пользователя или пароль")
        else:
            if not user.check_password(form.password.data):
                flash("Неверное имя пользователя или пароль")
            else:
                login_user(user)
                return redirect(url_for("cover_page"))
    return render_template('login_page.html', form=form)

@app.route("/singup", methods=["GET", "POST"])
def singup_page():
    if current_user.is_authenticated:
        return redirect(url_for("cover_page"))
    form = SingUpForm()
    if request.method == "POST":
        if not form.validate_on_submit():
            flash("Форма некорректна")
        else:
            print(form.password.data, form.repeat.data)
            if not (form.password.data == form.repeat.data):
                flash("Пароли не совпадают")
            else:
                session = create_session()
                user = session.query(User).filter(User.name == form.username.data).first()
                if user:
                    flash("Пользователь с таким именем уже существует")
                else:
                    user = session.query(User).filter(User.email == form.email.data).first()
                    if user:
                        flash("Такая почта уже существует")
                    else:
                        user = User(name=form.username.data, email=form.email.data)
                        user.set_password(form.password.data)
                        session.add(user)
                        session.commit()
                        return redirect(url_for("login_page"))
    return render_template('singup_page.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('cover_page'))


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
