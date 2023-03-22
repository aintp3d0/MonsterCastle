from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import InputRequired


class RegisterForm(FlaskForm):
  name = StringField('name', validators=[InputRequired()])


class LoginForm(FlaskForm):
  token = StringField('token', validators=[InputRequired()])
