from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms import validators


class ProjectCreateForm(FlaskForm):
    name = StringField('name', validators=[validators.DataRequired(), validators.length(2, 20)])


class ProjectMemberManageForm(FlaskForm):
    id = IntegerField('id', validators=[validators.DataRequired()])
