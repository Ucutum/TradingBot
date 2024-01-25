from flask import Flask, render_template, url_for, abort, redirect

app = Flask(__name__)

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

@app.route('/dashboard/<company_url>')
def dashboard_page(company_url):
    if company_url == "first":
        company_url = "google"
    free_companies = [
        {"url": "google", "title": "Google", "active": False},
        {"url": "vk", "title": "Вконтакте", "active": False}
    ]
    for company in free_companies:
        if company["url"] == company_url:
            company["active"] = True
    paid_companies = [
        {"url": "sber", "title": "Сбербанк", "active": False},
        {"url": "tinkoff", "title": "Тинькофф", "active": False},
        {"url": "yandex", "title": "Яндекс", "active": False}
    ]
    for company in paid_companies:
        if company["url"] == company_url:
            company["active"] = True
    data = {
        "free_companies": free_companies,
        "paid_companies": paid_companies
    }
    return render_template('dashboard_page.html', **data)

@app.route("/futer")
def futer_page():
    return render_template('futer_page.html')

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
