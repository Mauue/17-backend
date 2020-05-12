from db import db, red
db = db
red = red


def model_data_init():
    from .action import ActionType
    ActionType.init_type()

