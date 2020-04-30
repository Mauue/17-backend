from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import validators


class UserRegisterForm(FlaskForm):
    account_type = StringField('account_type', validators=[validators.DataRequired()])
    account = StringField('account', validators=[validators.DataRequired()])
    password = StringField('password', validators=[validators.DataRequired()])
    username = StringField('username', validators=[validators.DataRequired(), validators.Length(min=2, max=12)])


class UserLoginForm(FlaskForm):
    account_type = StringField('account_type', validators=[validators.DataRequired()])
    account = StringField('account', validators=[validators.DataRequired()])
    password = StringField('password', validators=[validators.DataRequired()])