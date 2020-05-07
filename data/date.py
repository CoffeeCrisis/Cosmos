from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import SubmitField
from datetime import date


class DateForm(FlaskForm):
    date = DateField(default=date.today)
    submit = SubmitField('Искать фото дня')