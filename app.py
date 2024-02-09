from flask import Flask, render_template, url_for, abort, redirect, request, flash, send_file
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
import datetime
from csv_parser import parse
from create_al_graphs import create_all

from forms.login_form import LogInForm
from forms.singup_form import SingUpForm
import json

from graph_creator import remove_trailing_empty_lines
import graph_creator



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


@app.route('/subscriptions', methods=['GET', 'POST'])
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

@app.route('/personal_area')
def cover_page():
    return render_template('cover_page.html')

@app.route("/graphs/<string:filename>")
def return_csv(filename):
    return send_file("graphs/" + filename)

@app.route('/dashboard/<company_token>')
def dashboard_page(company_token):
    if company_token == "first":
        company_token = "NVDA"

    free_companies = []
    with open('all.csv', newline='', encoding="utf-8") as f:
        spamreader = list(csv.reader(f, delimiter=';'))

        for row in list(spamreader)[:len(list(spamreader)) // 2]:
            free_companies.append({"title" : row[0], "active" : False, "token" : row[1]})


    for company in free_companies:
        if company["token"] == company_token:
            company["active"] = True

    paid_companies = list()
    free_companies_data = list()
    paid_companies_data = list()
    
    with open('all.csv', newline='', encoding="utf-8") as f:
        spamreader = list(csv.reader(f, delimiter=';'))

        for row in list(spamreader)[len(list(spamreader))//2:]:
            paid_companies.append({"title" : row[0], "active" : False, "token" : row[1]})

    for company in paid_companies:
        if company["token"] == company_token:
            company["active"] = True
            
    for company in free_companies:
        symbol = company["token"]
        with open(f'graphs/{symbol}.csv', newline='', encoding="utf-8") as f:
            for idx, row in enumerate(reversed(list(csv.reader(f, delimiter=';')))):
                if idx == 0: continue
                if idx > 30: break
                free_companies_data.append({"Symbol" : symbol, "Date" : row[0], "Open" : round(float(row[1]), 2), "High" : round(float(row[2]), 2), "Low" : round(float(row[3]), 2), "Close" : round(float(row[4]), 2), "Volume" : int(float(row[5]))})
        
    for company in paid_companies:
        symbol = company["token"]
        with open(f'graphs/{symbol}.csv', newline='', encoding="utf-8") as f:
            for idx, row in enumerate(reversed(list(csv.reader(f, delimiter=';')))):
                if idx == 0: continue
                if idx > 30: break
                free_companies_data.append({"Symbol" : symbol, "Date" : row[0], "Open" : round(float(row[1]), 2), "High" : round(float(row[2]), 2), "Low" : round(float(row[3]), 2), "Close" : round(float(row[4]), 2), "Volume" : int(float(row[5]))})

    canwatch = False
    if company_token in [i["token"] for i in free_companies]:
        canwatch = True
    elif company_token in [i["token"] for i in paid_companies]:
        if current_user.is_authenticated:
            if current_user.subscription:
                canwatch = True
    print(canwatch, company_token)


    data = {
        "free_companies": free_companies,
        "paid_companies": paid_companies,
        "company_token": company_token,
        "free_companies_data" : free_companies_data,
        "paid_companies_data" : paid_companies_data,
        "canwatch" : canwatch
    }
    # print(data["free_companies"])

    return render_template('dashboard_page.html', **data)

@app.route("/strategy")
def futer_page():
    
    shares = list()
    data = dict()

    remove_trailing_empty_lines("gdata/Package_.txt")

    with open("gdata/Package_.txt", "r", newline="") as f:
        lines = f.readlines()
        full_money = 0.0
        for item in lines:
            y, c, cn = item.split()     
            if(y != "MONEY"): full_money += float(c) * float(cn)
        for item in lines:
            title, cost, cost_one = item.split()
            if title == "MONEY": data[title] = cost
            else: shares.append({"title" : title, "cost" : round(float(cost) * float(cost_one) / full_money * 100, 2), "spend" : round(float(cost) * float(cost_one), 2)})

    data['current_shares'] = shares

    return render_template('futer_page.html', **data)

def get_graphs_paths():
    '''дает ссылки на графики прогы Артема'''
    with open("all.csv") as f:
        companies = [e for e in csv.reader(f, delimiter=";")]
    return list(filter(lambda x: x is not None, [(
            (i[0], f"graph/{i[1]}_graph.png") if
         os.path.exists(f"static/graph/{i[1]}_graph.png"
                        ) else None) for i in companies]))


last_update = settings.get("last_update", None)


@app.route("/update_data")
def update_data():
    if last_update is None:
        parse("graphs/")
        subprocess.run([run_command])
        create_all()
        graph_creator.main()
        last_update = datetime.now()
        settings["last_update"] = last_update
        with open("settings.json", "w") as f:
            json.dump(settings, f)
    elif last_update + datetime.timedelta(days=1) < datetime.now():
        parse("graphs/")
        subprocess.run([run_command])
        create_all()
        graph_creator.main()
        last_update = datetime.now()
        settings["last_update"] = last_update
        with open("settings.json", "w") as f:
            json.dump(settings, f)
    return "OK"


@app.route("/ai_strategy")
def ai_strategy_page():
    companies = get_graphs_paths()
    print(companies)
    graphs = [
        {"name": i[0],
         "img":f"{i[1]}"}
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

@app.route('/tologout')
def tologout():
    return render_template('cover3_page.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))

@app.route('/cancel_subscription')
def cancel_subscription_page():
    if not current_user.is_authenticated:
        return abort(403)
    return render_template('cancel_subscription_page.html')

@app.route('/cover2', methods=['GET', 'POST'])
def cover2_page():
    if current_user.is_authenticated:
        if not current_user.subscription:
            return redirect(url_for('на покупку'))
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash("Войдите в систему для покупки")
            return redirect(url_for('login_page'))
        else:
            session = create_session()
            user = session.query(User).get(current_user.id)
            user.subscription = False
            session.commit()
            return redirect(url_for('cancel_subscription_page'))
    return render_template('cover2_page.html')

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
