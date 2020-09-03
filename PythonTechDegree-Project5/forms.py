from flask_wtf import Form
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired

class JournalForm(Form):
    def integer_test(self, hours):
        try:
            testint = int(hours)
        except:
            raise ValidationError('Number of hours must be a whole number')

    title = StringField('Title', validators=[DataRequired()]),
    timespent = IntegerField('Hours spent', validators=[integer_test])
    learned = TextAreaField('Title')
    resources = TextAreaField('Resources')
