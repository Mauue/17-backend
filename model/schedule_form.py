from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, DateTimeField
from wtforms import validators


class ScheduleCreateForm(FlaskForm):
    content = StringField('content', validators=[validators.DataRequired(), validators.length(1, 20)])
    remarks = StringField('remarks', validators=[validators.length(max=200)])
    t_set = DateTimeField('t_set', validators=[validators.DataRequired()])
    t_remind = DateTimeField('t_remind')
    label = StringField('label', validators=[validators.length(max=200)])


class ScheduleUpdateForm(FlaskForm):
    id = IntegerField('id', validators=[validators.DataRequired()])
    content = StringField('content', validators=[validators.DataRequired(), validators.length(1, 20)])
    remarks = StringField('remarks', validators=[validators.length(max=200)])
    t_set = DateTimeField('t_set', validators=[validators.DataRequired()])
    label = StringField('label', validators=[validators.length(max=200)])


class ScheduleDeleteForm(FlaskForm):
    id = IntegerField('id', validators=[validators.DataRequired()])

