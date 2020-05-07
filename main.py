from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import abort

from data import db_session
from data.login_form import LoginForm
from data.users import User
from data.register import RegisterForm
from data.date import DateForm
from data.game import TestForm

import requests

import random
from datetime import date


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

def main():
    db_session.global_init("db/book.sqlite")

    @login_manager.user_loader
    def load_user(user_id):
        session = db_session.create_session()
        return session.query(User).get(user_id)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            session = db_session.create_session()
            user = session.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('login.html', message="Wrong login or password", form=form)
        return render_template('login.html', title='Authorization', form=form)

    @app.route("/collection", methods=['GET', 'POST'])
    def collection():
        data = 'https://launchlibrary.net/1.3/launch/next/10'
        response = requests.get(data)
        if response:
            json_response = response.json()
            rocket = [[json_response['launches'][i]['id'], json_response['launches'][i]['name'], json_response['launches'][i]['windowstart'], json_response['launches'][i]['location']['pads'][0]['name']] for i in range(10)]
        return render_template("collection.html", rocket=rocket)

    @app.route("/mission", methods=['GET', 'POST'])
    def mission():
        data = 'https://launchlibrary.net/1.3/mission/next/10'
        response = requests.get(data)
        if response:
            json_response = response.json()
            task = [[json_response['missions'][i]['id'], json_response['missions'][i]['name'], json_response['missions'][0]['description']] for i in range(10)]
        return render_template("mission.html", task=task)

    @app.route("/iss", methods=['GET', 'POST'])
    def iss():
        data = 'http://api.open-notify.org/iss-now.json'
        response = requests.get(data)
        if response:
            json_response = response.json()
            point = [[json_response['iss_position']['longitude'], json_response['iss_position']['latitude']]]
        data = 'http://api.open-notify.org/astros.json'
        response = requests.get(data)
        if response:
            json_response = response.json()
            n = json_response['number']
            name = [json_response['people'][i]['name'] for i in range(n)]
        return render_template("iss.html", point=point, n=n, name=name)

    @app.route("/tesla", methods=['GET', 'POST'])
    def tesla():
        data = 'https://api.spacexdata.com/v3/roadster'
        response = requests.get(data)
        if response:
            json_response = response.json()
            speed = json_response['speed_kph']
            earth = json_response['earth_distance_km']
            mars = json_response['mars_distance_km']
        return render_template("tesla.html", speed=speed, earth=earth, mars=mars)

    @app.route("/mars", methods=['GET', 'POST'])
    def mars():
        picture = f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1100&api_key=AqT7xtdscaq96S0w4KdsgtQ637Z0DbHasFDT8S2J'
        response = requests.get(picture)
        if response:
            json_response = response.json()
            pic = [json_response['photos'][i]['img_src'] for i in range(3)]
        data = 'https://api.nasa.gov/insight_weather/?api_key=AqT7xtdscaq96S0w4KdsgtQ637Z0DbHasFDT8S2J&feedtype=json&ver=1.0'
        d = str(date.today())[-4:].split('-')
        d = ''.join(d)
        response = requests.get(data)
        if response:
            json_response = response.json()
            t = [json_response[d]['AT']['mn'], json_response[d]['AT']['mx']]
            v = [json_response[d]['HWS']['mn'], json_response[d]['HWS']['mx']]
            p = [json_response[d]['PRE']['mn'], json_response[d]['PRE']['mx']]
        return render_template("mars.html", pic=pic, today=date.today(), t=t, v=v, p=p)

    @app.route("/comet", methods=['GET', 'POST'])
    def comet():
        data = 'https://ssd-api.jpl.nasa.gov/cad.api?fullname=True'
        response = requests.get(data)
        if response:
            json_response = response.json()
            time = [json_response['data'][i][3] for i in range(10)]
            v = [json_response['data'][i][7] for i in range(10)]
            fail = [json_response['data'][i][9] for i in range(10)]
            name = [json_response['data'][i][-1] for i in range(10)]
        return render_template("comet.html", time=time, v=v, fail=fail, name=name)

    @app.route("/fireball", methods=['GET', 'POST'])
    def fireball():
        data = 'https://ssd-api.jpl.nasa.gov/fireball.api?req-vel=True&limit=10'
        response = requests.get(data)
        if response:
            json_response = response.json()
            time = [json_response['data'][i][0] for i in range(10)]
            v = [json_response['data'][i][-1] for i in range(10)]
            energy = [json_response['data'][i][1] for i in range(10)]
        return render_template("fireball.html", time=time, v=v, energy=energy)

    @app.route("/photo", methods=['GET', 'POST'])
    def photo():
        form = DateForm()
        data = f"https://apodapi.herokuapp.com/api/?date={str(DateForm().date).split()[-1][7:17]}&html_tags=true&image_thumbnail_size=450&absolute_thumbnail_url=true"
        response = requests.get(data)
        if response:
            json_response = response.json()
            pic = json_response['url']
            text = json_response['title']
        else:
            return render_template("photo.html", form=form, pic='', text='')
        if form.submit():
            data = f"https://apodapi.herokuapp.com/api/?date={str(DateForm().date).split()[-1][7:17]}&html_tags=true&image_thumbnail_size=400&absolute_thumbnail_url=true"
            response = requests.get(data)
            if response:
                json_response = response.json()
                pic = json_response['url']
                text = json_response['title']
            else:
                return render_template("photo.html", form=form, pic='', text='')
            return render_template("photo.html", form=form, pic=pic, text=text)
        return render_template("photo.html", form=form, pic=pic, text=text)

    @app.route("/game", methods=['GET', 'POST'])
    @login_required
    def game():
        form = TestForm()
        if TestForm().data['submit']:
            global score
            score = 0
            global answer
            answer = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            if TestForm().data['one'] == 'Юпитер':
                score += 1
                answer[0] = 1
            if TestForm().data['two'] == '2':
                score += 1
                answer[1] = 1
            if TestForm().data['three'] == 'Меркурий':
                score += 1
                answer[2] = 1
            if TestForm().data['four'] == 'Между орбитами Марса и Юпитера':
                score += 1
                answer[3] = 1
            if TestForm().data['five'] == 'Каждые 75-76 лет':
                score += 1
                answer[4] = 1
            if TestForm().data['six'] == 'Млечный путь':
                score += 1
                answer[5] = 1
            if TestForm().data['seven'] == 'Юпитер':
                score += 1
                answer[6] = 1
            if TestForm().data['eight'] == 'Углекислый газ':
                score += 1
                answer[7] = 1
            if TestForm().data['nine'] == 'Венера':
                score += 1
                answer[8] = 1
            if TestForm().data['ten'] == 'Уран':
                score += 1
                answer[9] = 1
            return redirect('/result')
        return render_template("game.html", form=form)

    @app.route("/result", methods=['GET', 'POST'])
    @login_required
    def result():
        ques = ['Cамая большая планета солнечной системы?', 'Сколько спутников у Марса?', 'Ближайшая к Солнцу планета?', 'Где расположен пояс астероидов?', 'С какой периодичностью в небе Земли появляется камета Галлея?', 'В какой галактике находится Солнечная система?', 'У какой планеты больше всего спутников?', 'Из какого газа состоит атмосфера Венеры?', 'На какой планете сутки равны году?', 'Какая планета вращается вокруг Солнца лёжа на боку?']
        reply = ['Юпитер', '2', 'Меркурий', 'Между орбитами Марса и Юпитера', 'Каждые 75-76 лет', 'Млечный путь', 'Юпитер', 'Углекислый газ', 'Венера', 'Уран']
        return render_template("result.html", score=score, ques=ques, reply=reply, answer=answer)

    @app.route("/")
    @app.route("/index")
    def index():
        return render_template("index.html")

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Register', form=form,
                                       message="Passwords don't match")
            session = db_session.create_session()
            if session.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Register', form=form,
                                       message="This user already exists")
            user = User(
                name=form.name.data,
                surname=form.surname.data,
                email=form.email.data,
            )
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            return redirect('/login')
        return render_template('register.html', title='Регистрация', form=form)
    
    app.run()


if __name__ == '__main__':
    main()
