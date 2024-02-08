from flask import Flask, render_template, url_for, abort, redirect, request, flash
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

from data.db_session import create_session, global_init
from data.users import User
from data.stocks import Stock
from data.companies import Company
import os


from forms.login_form import LogInForm
from forms.singup_form import SingUpForm


global_init(os.path.join("db", "database.db"))


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
    if company_token == "first":
        company_token = "GOGL"
    free_companies = [
        {"title": "Google", "active": False, "token": "GOGL"},
        {"title": "Вконтакте", "active": False, "token": "VKCO"}
    ]
    for company in free_companies:
        if company["token"] == company_token:
            company["active"] = True
    paid_companies = [
        {"title": "Сбербанк", "active": False, "token": "SBER"},
        {"title": "Тинькофф", "active": False, "token": "TCSG"},
        {"title": "Яндекс", "active": False, "token": "YNDX"},
        {"title": "Газпром", "active": False, "token": "GAZP"},
        {"title": "Татнефть", "active": False, "token": "TATN"},
        {"title": "Мечел", "active": False, "token": "MTLR"},
        {"title": "Лукойл", "active": False, "token": "LKOH"},
        {"title": "Аэрофлот", "active": False, "token": "AFLT"},
        {"title": "Сургутнефтегаз", "active": False, "token": "SNGS"},
        {"title": "МТС", "active": False, "token": "MTSS"},
        {"title": "Магнит", "active": False, "token": "MGNT"},
        {"title": "Новатэк", "active": False, "token": "NVTK"},
        {"title": "М.Видео", "active": False, "token": "MVID"},
        {"title": "Татнефть", "active": False, "token": "TATN"},
        {"title": "НЛМК", "active": False, "token": "NLMK"},
        {"title": "Эн+", "active": False, "token": "ENPG"},
        {"title": "ММК", "active": False, "token": "MAGN"},
        {"title": "Северсталь", "active": False, "token": "CHMF"},
        {"title": "АФК Система", "active": False, "token": "AFKS"},
        {"title": "Трубная Металлургическая Компания", "active": False, "token": "TRMK"},
        {"title": "Мосэнерго", "active": False, "token": "MSNG"},
        {"title": "ФосАгро", "active": False, "token": "PHOR"},
        {"title": "РусГидро", "active": False, "token": "HYDR"},
        {"title": "Полюс", "active": False, "token": "PLZL"},
        {"title": "АЛРОСА", "active": False, "token": "ALRS"},
        {"title": "РосНефть", "active": False, "token": "RNFT"},
        {"title": "КАМАЗ", "active": False, "token": "KMAZ"},
        {"title": "Россети Московский Регион", "active": False, "token": "MSRS"},
        {"title": "Детский Мир", "active": False, "token": "DSKY"},
        {"title": "Группа Черкизово", "active": False, "token": "GCHE"},
        {"title": "Совкомфлот", "active": False, "token": "FLOT"},
        {"title": "СОЛЛЕРС", "active": False, "token": "SVAV"},
        {"title": "Юнипро", "active": False, "token": "UPRO"},
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

@app.route("/ai_strategy")
def ai_strategy_page():
    return render_template('ai_strategy.html')

@app.route("/futer")
def futer_page():
    return render_template('futer_page.html')

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
