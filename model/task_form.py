from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, DateTimeField
from wtforms import validators


class TaskCreateForm(FlaskForm):
    name = StringField('name', validators=[validators.DataRequired(), validators.length(2, 20)])
    remarks = StringField('remarks', validators=[validators.length(max=200)])
    t_begin = DateTimeField('t_begin')
    t_end = DateTimeField('t_begin')
    priority = IntegerField('priority')
    label = StringField('label', validators=[validators.length(max=200)])
