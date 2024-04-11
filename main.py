from flask import Flask, render_template, request, make_response, jsonify
from flask import redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import abort, Api

from forms.news import NewsForm
from forms.user import RegisterForm, LoginForm
from data.news import News
from data import db_session, news_api, news_resources
from data.users import User
import sqlite3

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
con = sqlite3.connect('db/Railway_data.db')
cursor_sql = con.cursor()
cursor_sql.execute('')

lines = [i[0] for i in cursor_sql.execute('SELECT name FROM LINES').fetchall()]
dic_line_to_stations = {i[0]: i[1].split(', ') for i in
                        cursor_sql.execute('SELECT name, stations FROM LINES').fetchall()}
RESOURCES = ['Нефтепродукты', "Строительные материалы", "Химическая продукция", "Металлопрокат",
             "Контейнеры", "Уголь", "Нефть", "Песок", "Глина", "Древесина", "Сталь", "Алюминий", "Зерно", "Сахар",
             "Мука", "Фрукты", "Овощи", "Мясо", "Рыба", "Молоко",
             "Яйца", "Ткани", "Одежда", "Обувь", "Мебель", "Электроника", "Автомобили",
             "Мотоциклы", "Книги", "Бумага", "Пластик", "Стекло", "Керамика",
             "Лекарства", "Химикаты"]
# ресурсы и вес единицы этого ресурса в кг || ВРЯД ЛИ ЭТО ПРИГОДИТСЯ
resources_weight = {
    'Нефтепродукты': 500, "Строительные материалы": 1000, "Химическая продукция": 300, "Металлопрокат": 700,
    "Контейнеры": 200, "Уголь": 600, "Нефть": 800, "Песок": 1200, "Глина": 1000,
    "Древесина": 500, "Сталь": 900, "Алюминий": 400, "Зерно": 600, "Сахар": 300,
    "Мука": 400, "Фрукты": 200, "Овощи": 300, "Мясо": 500, "Рыба": 400, "Молоко": 1000, "Яйца": 200, "Ткани": 300,
    "Одежда": 500, "Обувь": 400, "Мебель": 600, "Электроника": 200, "Автомобили": 1500, "Мотоциклы": 300,
    "Книги": 200, "Бумага": 400, "Пластик": 500, "Стекло": 700, "Керамика": 600, "Лекарства": 300, "Химикаты": 400}


@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route('/resources')
def resources():
    if current_user.is_authenticated:
        is_authenticated = True
    else:
        is_authenticated = False
    return render_template('resources.html', resources=RESOURCES, is_authenticated=is_authenticated)


@app.route('/buying_train', methods=['GET', "POST"])
def buying_train():
    if current_user.is_authenticated:
        is_authenticated = True
    else:
        is_authenticated = False

    if request.method == 'GET':  # TODO
        params = {"lines": lines, "line_to_stations": dic_line_to_stations}
        return render_template('buying_train.html', **params, is_authenticated=is_authenticated)
    elif request.method == 'POST':
        params = dict(request.form)
        return render_template('result_buying_train.html', **params)


@app.route
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/news")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route('/add_news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)


@app.route('/edit_news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(news_api.blueprint)
    # для списка объектов
    api.add_resource(news_resources.NewsListResource, '/api/v2/news')

    # для одного объекта
    api.add_resource(news_resources.NewsResource, '/api/v2/news/<int:news_id>')
    app.run()


if __name__ == '__main__':
    main()
