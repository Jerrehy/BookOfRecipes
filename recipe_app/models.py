from flask_login import UserMixin
from recipe_app import db
from recipe_app import bcrypt
from recipe_app import login_manager
from flask import flash


# Обязательный метод для получения текущего ID пользователя
@login_manager.user_loader
def load_user(user_id):
    return BookUser.query.get(int(user_id))


# Таблица с пользователями системы
class BookUser(db.Model, UserMixin):
    __tablename__ = 'book_user'
    __table_args__ = {'extend_existing': True}

    id_book_user = db.Column(db.Integer(), primary_key=True)
    password = db.Column(db.String(length=150), nullable=False)

    # Метод получения ID пользователя из таблицы
    def get_id(self):
        return self.id_book_user

    # Получение пароля
    @property
    def unencrypted_password(self):
        return self.unencrypted_password

    # Шифрование пароля
    @unencrypted_password.setter
    def unencrypted_password(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    # Проверка пароля
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)

    # Получение информации о пользователе по логину
    @staticmethod
    def get_user_by_login(login):
        return BookUser.query.filter_by(login=login).first()

    # Получение информации о пользователе по фамилии
    @staticmethod
    def get_user_by_fio(fio):
        return BookUser.query.filter_by(fio=fio).first()

    # Изменение данных о пользователе
    @staticmethod
    def update_system_user(login, fio, email, photo):
        try:
            user_for_update = BookUser.get_user_by_login(login)

            user_for_update.fio = fio
            user_for_update.email = email
            user_for_update.photo = photo

            db.session.commit()
            flash("Пользователь был успешно изменён.", category='success')
        except:
            db.session.rollback()
            flash("Произошла ошибка при изменнии пользователя. Повторите попытку.", category='danger')

    # Добавление нового пользователя
    @staticmethod
    def add_system_user(fio, email, login, password, id_role, photo=None):
        new_system_user = BookUser(fio=fio, email=email, login=login, unencrypted_password=password,
                                   id_role=id_role, photo=photo)

        try:
            db.session.add(new_system_user)
            db.session.commit()
            flash("Пользователь был успешно добавлен.", category='success')
        except:
            db.session.rollback()
            flash("Произошла ошибка при добавлении пользователя. Повторите попытку.", category='danger')


# Таблица с ролями пользователей в системе
class RoleUser(db.Model):
    __tablename__ = 'role_user'
    __table_args__ = {'extend_existing': True}

    # Получение всего списка ролей
    @staticmethod
    def get_all_roles():
        return RoleUser.query.all()

    # Получение всего списка ролей
    @staticmethod
    def get_role_by_name(name_role):
        return RoleUser.query.filter_by(name_role=name_role).first()


# Таблица с любимыми рецептами - избранное
class Favorite(db.Model):
    __tablename__ = 'favorite'
    __table_args__ = {'extend_existing': True}


# Таблица с ингридиентами на выбор
class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    __table_args__ = {'extend_existing': True}


# Таблица с ингридиентами в блюде
class IngredientInRecipe(db.Model):
    __tablename__ = 'ingredient_in_recipe'
    __table_args__ = {'extend_existing': True}


# Таблица с владельцами рецептов
class Publication(db.Model):
    __tablename__ = 'publication'
    __table_args__ = {'extend_existing': True}


# Таблица со всеми рецептами
class Recipe(db.Model):
    __tablename__ = 'recipe'
    __table_args__ = {'extend_existing': True}

    # Получение списка всех рецептов
    @staticmethod
    def get_all_recipes():
        query = db.session.query(Recipe, RecipeCategory)
        query = query.join(RecipeCategory, RecipeCategory.id_category == Recipe.id_category)
        return query.all()


# Таблица с категориями рецептов
class RecipeCategory(db.Model):
    __tablename__ = 'recipe_category'
    __table_args__ = {'extend_existing': True}


# Таблица с отзывами о рецептах
class Review(db.Model):
    __tablename__ = 'review'
    __table_args__ = {'extend_existing': True}
