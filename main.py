import re

from flask import Flask, render_template, url_for, redirect

from DataBase import DB, NewsModel, UsersModel
from Forms import LoginForm, AddNewsForm, InForm
from Password import password_level
from User import User

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


def validate_email(email):
    if re.fullmatch(regex, email):
        return True
    return False


app = Flask(__name__)
app.config['SECRET_KEY'] = 'lenochek_secret_key'

# Словарь (почта: (пароля, имя))
users = {}
session = {}
db = DB()
user = User
d = []
um = UsersModel(db.get_connection())


# Функция регистрации
def reg_funk(email, name, password):
    last_user = email
    error = 0
    # Если такое имя уже есть
    for i in users.keys():
        if users[i][0] == name:
            error = 4
    # Если email не соответствует стандарту email
    if not validate_email(last_user):
        error = 1
        print(last_user)
    # Если человек с такой почтой уже есть
    elif last_user in users.keys():
        error = 2
    elif password_level(password) != "Надежный пароль":
        pas_lvl = password_level(password)
        if pas_lvl == 'Недопустимый пароль':
            error = 5
        elif pas_lvl == 'Ненадежный пароль':
            error = 6
        elif pas_lvl == 'Слабый пароль':
            error = 7
    # если все в порядке
    elif error == 0:
        user_model = UsersModel(db.get_connection())
        user_model.insert(name, password)
        user.last_user = last_user
        user.signed = 1
        user.name = name
        users[last_user] = (name, password)
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(user.name, password)
        print(exists, user.name, password, session)
        user.name = users[last_user][0]
        exists = user_model.exists(user.name, password)
        if exists[0]:
            session['username'] = user.name
            session['user_id'] = exists[1]
        print(users)
    return error


# Функция входа
def in_funk(email, password):
    print("in funk")
    last_user = email
    error = 0
    # если такого пользователя нет
    if last_user not in users.keys():
        error = 1
        print("2")
    # если пароль не верен
    elif password != users[last_user][1]:
        error = 3
        print("3")
    # если все в поряке
    else:
        print("OK")
        user.last_user = last_user
        user.signed = 1
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(user.name, password)
        print(exists, user.name, password, session)
        user.name = users[last_user][0]
        exists = user_model.exists(user.name, password)
        if exists[0]:
            session['username'] = user.name
            session['user_id'] = exists[1]
        print(users)
    return error


@app.route('/')
@app.route('/index')
@app.route('/index.html')
@app.route('/Главная')
@app.route('/главная')
@app.route('/main page')
def index():
    return render_template('index.html', image=url_for(
        "static", filename="css/img/my_images/str211.jpg"),
                           style=url_for(
                               "static", filename="css/qw.css"),
                           name=user.name, signed=user.signed)


@app.route("/creations.html")
def creations():
    return render_template('creations.html',
                           style=url_for("static",
                                         filename="css/qw.css"),
                           image1=url_for("static",
                                          filename=
                                          "css/img/images/str241.jpg"),
                           image2=url_for("static",
                                          filename=
                                          "css/img/my_images/str312.jpg"),
                           image3=url_for("static",
                                          filename=
                                          "css/img/images/str242.jpg"),
                           image4=url_for("static",
                                          filename=
                                          "css/img/images/str243.jpg"),
                           image5=url_for("static",
                                          filename=
                                          "css/img/images/str244.jpg"),
                           image6=url_for("static",
                                          filename=
                                          "css/img/images/str245.jpg"),
                           image7=url_for("static",
                                          filename=
                                          "css/img/images/str246.jpg"),
                           image8=url_for("static",
                                          filename=
                                          "css/img/images/str247.jpg"),
                           name=user.name, signed=user.signed)


@app.route("/bestiary.html")
def bestiary():
    return render_template('bestiary.html',
                           style=url_for("static",
                                         filename="css/qw.css"),
                           name=user.name, signed=user.signed)


# Функция выхода
@app.route("/out.html")
def out():
    # нет вошедшего пользователя
    user.signed = 0
    # обнуляем переменные user
    user.name = 0
    user.last_user = 0
    # удаляем юзера из сессии
    session.pop('username', 0)
    session.pop('user_id', 0)
    return render_template('index.html',
                           style=url_for("static",
                                         filename="css/qw.css"),
                           name=user.name, signed=user.signed)


@app.route("/personal.html")
def personal():
    # беререм все новости данного пользователя
    news = NewsModel(db.get_connection()).get_all(session['user_id'])
    return render_template('personal.html', username=session['username'],
                           news=news, style=url_for("static",
                                                    filename="css/qw.css"),
                           name=user.name, signed=user.signed)


@app.route("/registration.html", methods=['GET', 'POST'])
def registration():
    form = LoginForm()
    if form.validate_on_submit():
        # проверяем ошибки при регистрации
        error = reg_funk(str(form.email.data), str(form.username.data), str(form.password.data))
        return render_template('success.html',
                               style=url_for("static",
                                             filename="css/qw.css"),
                               par=error, name=user.name,
                               signed=user.signed)

    return render_template('registration.html', form=form,
                           style=url_for("static",
                                         filename="css/qw.css"),
                           name=user.name, signed=user.signed)


@app.route("/input.html", methods=['GET', 'POST'])
def input1():
    form = InForm()
    if form.validate_on_submit():
        # проверяем ошибки при входе
        error = in_funk(str(form.email.data), str(form.password.data))
        return render_template('success.html',
                               style=url_for("static",
                                             filename="css/qw.css"),
                               par=error, name=user.name,
                               signed=user.signed)

    return render_template('input.html', form=form,
                           style=url_for("static",
                                         filename="css/qw.css"),
                           name=user.name, signed=user.signed)


@app.route('/add_news.html', methods=['GET', 'POST'])
def add_news():
    if 'username' not in session:
        print(session)
        return redirect('/input.html')
    form = AddNewsForm()
    if form.validate_on_submit():
        # добавляем новость
        title = form.title.data + " (author: " + session['username'] + ")"
        content = form.content.data
        nm = NewsModel(db.get_connection())
        nm.insert(title, content, session['user_id'])
        return redirect("/all_news.html")
    return render_template('add_news.html', title='Добавление новости',
                           form=form, username=session['username'],
                           style=url_for("static",
                                         filename="css/qw.css"),
                           name=user.name, signed=user.signed)


@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news(news_id):
    if 'username' not in session:
        return redirect('/login')
    # удаляем новость
    nm = NewsModel(db.get_connection())
    nm.delete(news_id)
    return redirect("/personal.html")


@app.route('/all_news.html', methods=['GET', 'POST'])
def all_news():
    if 'username' not in session:
        print(session)
        return redirect('/input.html')
    # показываем все новости
    news = NewsModel(db.get_connection()).get_all()
    return render_template('all_news.html', username=session['username'],
                           news=news, style=url_for("static",
                                                    filename="css/qw.css"),
                           name=user.name, signed=user.signed)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
