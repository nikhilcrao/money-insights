import wtforms

from flask_wtf import FlaskForm
from wtforms import validators

class LoginForm(FlaskForm):
    username = wtforms.StringField('Username', [validators.InputRequired(), validators.Email()])
    password = wtforms.PasswordField('Password', [validators.InputRequired()])
    next = wtforms.HiddenField()
    submit = wtforms.SubmitField('Submit')


class RegistrationForm(FlaskForm):
    username = wtforms.StringField('username', [validators.InputRequired(), validators.Email()])
    password = wtforms.PasswordField('Password', [validators.InputRequired()])
    next = wtforms.HiddenField()
    submit = wtforms.SubmitField('Submit')
