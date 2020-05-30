from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, DateTimeField, BooleanField
from wtforms import validators


class TaskCreateForm(FlaskForm):
    name = StringField('name', validators=[validators.DataRequired(), validators.length(2, 20)])
    remarks = StringField('remarks', validators=[validators.length(max=200)])
    t_begin = DateTimeField('t_begin')
    t_end = DateTimeField('t_end')
    priority = IntegerField('priority')
    label = StringField('label', validators=[validators.length(max=200)])


class TaskUpdateForm(TaskCreateForm):
    id = IntegerField('id', validators=[validators.DataRequired()])
    finish = BooleanField('finish')


class TaskDeleteForm(FlaskForm):
    id = IntegerField('id', validators=[validators.DataRequired()])


class TaskManageParticipant(FlaskForm):
    task_id = IntegerField('task_id', validators=[validators.DataRequired()])
    user_id = IntegerField('user_id', validators=[validators.DataRequired()])

