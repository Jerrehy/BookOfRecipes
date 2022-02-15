from flask import flash
from flask_login import UserMixin
from recipe_app import db, login_manager, bcrypt


# # Обязательный метод для получения текущего ID пользователя
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
