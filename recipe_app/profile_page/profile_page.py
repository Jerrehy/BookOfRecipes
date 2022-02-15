from flask import render_template, Blueprint, redirect, url_for, session
from recipe_app.models import BookUser
from recipe_app.forms import UpdateUserProfile
from flask_login import login_required, current_user


# Создание узла связанного с профилем и его изменением
profile = Blueprint('profile', __name__, template_folder="templates")


# Просмотр информации о пользователе
@profile.route('/profile_view', methods=['GET'])
@login_required
def profile_view():
    activated_user = BookUser.get_user_by_login_with_role(session['login'])
    return render_template('profile/user_profile.html', activated_user=activated_user)


# Обновление профиля пользователя
@profile.route('/update_profile_view', methods=['GET', 'POST'])
@login_required
def profile_update_view():
    # Форма для обновления профиля
    update_profile_form = UpdateUserProfile()
    # Получение текущей информации о пользователе
    activated_user = BookUser.get_user_by_login(session['login'])

    if update_profile_form.submit_update.data:
        # Проверка на введённые в форме данные

        # ФИО
        if update_profile_form.fio.data:
            fio = update_profile_form.fio.data
        else:
            fio = activated_user.fio
        # Дата рождения
        if update_profile_form.email.data:
            email = update_profile_form.email.data
        else:
            email = activated_user.email
        # Фото пользователя
        if update_profile_form.photo.data:
            photo = update_profile_form.photo.data
        else:
            photo = activated_user.photo

        # Обновление профиля пользователя
        BookUser.update_system_user(session['login'], fio, email, photo)

        return redirect(url_for('profile.profile_view'))

    return render_template('profile/update_user_profile.html', activated_user=activated_user,
                           update_profile_form=update_profile_form)
