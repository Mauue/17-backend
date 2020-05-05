from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField
from wtforms import validators


class FileUploadForm(FlaskForm):
    file = FileField('file')
    path = StringField('path')


class FileDeleteForm(FlaskForm):
    path = StringField('path', validators=[validators.DataRequired()])


class FilesDeleteForm(FlaskForm):
    paths = StringField('paths', validators=[validators.DataRequired()])

