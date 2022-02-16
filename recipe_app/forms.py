from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, SelectField, IntegerField, \
    HiddenField, EmailField
from wtforms.validators import ValidationError, Length, EqualTo, DataRequired
from recipe_app.models import BookUser


# Форма регистрации на сайте
class RegisterForm(FlaskForm):
    # Проверка наличия совпадений имён пользователей при создании нового пользователя
    def validate_login(self, login_to_check):
        user = BookUser.get_user_by_login(login_to_check.data)
        if user:
            raise ValidationError('Такое имя пользователя уже есть! Попробуйте придумать другое')

    # Проверка наличия совпадени ФИО при создании нового пользователя
    def validate_fio(self, fio_to_check):
        fio = BookUser.get_user_by_fio(fio_to_check.data)
        if fio:
            raise ValidationError('У такого человека уже существует аккаунт! '
                                  'Если пароль и логин забыты, то обратитесь к администратору')

    # Данные для создания нового пользователя с ограничениями, которые накладываются на таблицу в БД
    fio = TextAreaField(label='ФИО:', validators=[DataRequired()])
    email = EmailField(label='Электронная почта:', validators=[DataRequired()])
    role = SelectField(label='Роль на сайте:', choices=[])
    photo = StringField(label='Ссылка на фото пользователя с размером близким к 300х300')
    login = StringField(label='Логин:', validators=[Length(min=6, max=20), DataRequired()])
    password1 = PasswordField(label='Пароль:', validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label='Подтвердить пароль:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Создать аккаунт')


# Форма авторизации на сайте
class LoginForm(FlaskForm):
    login = StringField(label="Логин:", validators=[DataRequired()])
    password = PasswordField(label="Пароль:", validators=[DataRequired()])
    submit = SubmitField(label='Вход')


# Форма для перехода в окно информации о рецепте
class RecipeInfoById(FlaskForm):
    id_recipe = HiddenField()
    submit_info = SubmitField(label='Подробнее о рецепте')


# Форма изменения данных о пользователе
class UpdateUserProfile(FlaskForm):
    # Данные для создания нового пользователя с ограничениями, которые накладываются на таблицу в БД
    fio = TextAreaField(label='Новое ФИО:')
    email = EmailField(label='Электронная почта:')
    photo = StringField(label='Ссылка на новое фото пользователя с размером близким к 300х300')
    submit_update = SubmitField(label='Обновить данные профиля')


# Форма добавления рецепта
class AddRecipeForm(FlaskForm):
    # Данные для создания нового пользователя с ограничениями, которые накладываются на таблицу в БД
    recipe_name = StringField(label='Именование рецепта:', validators=[DataRequired()])
    description = TextAreaField(label='Описание приготовления', validators=[DataRequired()])
    date_publication = DateField(label='Дата публикации', validators=[DataRequired()])
    category = SelectField(label='Категория блюда:', choices=[])
    number_of_servings = IntegerField(label='Количество персон')
    photo = StringField(label='Ссылка на фото блюда с размером близким к 300х300')
    submit_add = SubmitField(label='Добавить рецепт')
