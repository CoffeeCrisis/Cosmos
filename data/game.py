from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.fields import RadioField


class TestForm(FlaskForm):
    one = RadioField('Cамая большая планета солнечной системы?', choices=['Уран', 'Нептун', 'Марс', 'Земля', 'Юпитер'])
    two = RadioField('Сколько спутников у Марса?', choices=['0', '1', '2', '3', '4', '5'])
    three = RadioField('Ближайшая к Солнцу планета?', choices=['Венера', 'Марс', 'Уран', 'Меркурий', 'Земля'])
    four = RadioField('Где расположен пояс астероидов?', choices=['Между орбитами Марса и Юпитера', 'Между Солнцем и Меркурием', 'За орбитой Плутона'])
    five = RadioField('С какой периодичностью в небе Земли появляется камета Галлея?', choices=['Ежегодно', 'Каждые 15-16 лет', 'Каждые 75-76 лет', 'Каждые 140-145 лет'])
    six = RadioField('В какой галактике находится Солнечная система?', choices=['Галактика Андромеды', 'Млечный путь', 'Большое Магелланово Облако', 'Малое Магелланово Облако'])
    seven = RadioField('У какой планеты больше всего спутников?', choices=['Юпитер', 'Сатурн', 'Меркурий', 'Уран'])
    eight = RadioField('Из какого газа состоит атмосфера Венеры?', choices=['Азот', 'Углекислый газ', 'Водород', 'Озон', 'Метан'])
    nine = RadioField('На какой планете сутки равны году?', choices=['Плутон', 'Венера', 'Юпитер', 'Марс'])
    ten = RadioField('Какая планета вращается вокруг Солнца лёжа на боку?', choices=['Меркурий', 'Венера', 'Уран', 'Нептун', 'Марс'])
    submit = SubmitField('Завершить', default=False)