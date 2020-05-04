from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField
from wtforms import validators


class UserRegisterForm(FlaskForm):
    account_type = StringField('account_type', validators=[validators.DataRequired()])
    account = StringField('account', validators=[validators.DataRequired()])
    password = StringField('password', validators=[validators.DataRequired()])
    username = StringField('username', validators=[validators.DataRequired(),
                                                   validators.Length(min=2, max=12)])


class UserLoginForm(FlaskForm):
    account_type = StringField('account_type', validators=[validators.DataRequired()])
    account = StringField('account', validators=[validators.DataRequired()])
    password = StringField('password', validators=[validators.DataRequired()])


class UserUpdateInfoForm(FlaskForm):
    username = StringField('username', validators=[validators.DataRequired(),
                                                   validators.Length(min=2, max=12)])
    location = StringField('location', validators=[validators.Length(max=200)])
    website = StringField('website', validators=[validators.Length(max=200)])


class UserUploadPhotoForm(FlaskForm):
    image = FileField('image', validators=[FileAllowed(['jpg', 'png'], "image only"), FileRequired()])

