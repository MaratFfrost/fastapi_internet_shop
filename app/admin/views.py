from sqladmin import ModelView

from app.users.model import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name]
