from flask_wtf import Form
from wtforms import StringField, IntegerField, TextAreaField, DateField
from wtforms.validators import DataRequired, NumberRange

import datetime


class JournalForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date', default=datetime.datetime.now())
    timeSpent = IntegerField('Hours spent', validators=[NumberRange(min=0)])
    learned = TextAreaField('Learned', validators=[DataRequired()])
    resources = TextAreaField('Resources')
