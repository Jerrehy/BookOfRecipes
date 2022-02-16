from flask import Blueprint, render_template, redirect, url_for, session, flash
from recipe_app.models import Recipe, RecipeCategory, IngredientInRecipe, Publication, Review
from recipe_app.forms import RecipeInfoById, AddRecipeForm, DeleteRecipe, AddComment
from flask_login import login_required, current_user

recipe = Blueprint('recipe', __name__, template_folder="templates")


# Начальная страница сайта
@recipe.route('/')
@recipe.route('/main', methods=['GET', 'POST'])
def recipe_page_view():
    # Получение списка всех рецептов
    all_recipe = Recipe.get_all_recipes()
    # Подключение формы для перехода за большей информацией о рецептемаршруте
    info_about_recipe = RecipeInfoById()

    # Переход по форме "узнать больше"
    if info_about_recipe.submit_info.data:
        return redirect(url_for('recipe.one_recipe_page_view', id_recipe=info_about_recipe.id_recipe.data))

    return render_template('recipe/main.html', all_recipe=all_recipe, info_about_recipe=info_about_recipe)


@recipe.route('/recipe/<id_recipe>', methods=['GET', 'POST'])
def one_recipe_page_view(id_recipe):
    # Получение информации о текущем рецепте
    recipe_for_view = Recipe.get_recipe_by_id_with_category(id_recipe)
    # Вывод всех ингредиентов рецепта
    ingredients_in_recipe = IngredientInRecipe.get_all_ingredients_for_recipe(id_recipe)
    # Форма для добавления комментария
    add_comment = AddComment()
    # Список всех комментариев для определённого рецепта
    all_comments = Review.get_review(id_recipe)

    if add_comment.submit_add.data:
        # Добавления отзыва
        Review.add_review(add_comment.id_recipe.data, current_user.get_id(), add_comment.comment.data,
                          add_comment.rate.data)
        return redirect(url_for('recipe.one_recipe_page_view', id_recipe=id_recipe))

    return render_template('recipe/one_recipe.html', recipe_for_view=recipe_for_view, all_comments=all_comments,
                           ingredients_in_recipe=ingredients_in_recipe, add_comment=add_comment, id_recipe=id_recipe)


@recipe.route('/personal_recipes', methods=['GET', 'POST'])
@login_required
def personal_recipe_view():
    if session['role'] == 1:
        # Получение информации о всех рецептах по ID пользователя
        all_recipe = Publication.get_personal_recipes(current_user.get_id())

        # Форма удаления рецепта
        del_recipe_form = DeleteRecipe()

        # Удаление рецепта - активация
        if del_recipe_form.submit_del.data:
            Recipe.del_recipe(del_recipe_form.id_recipe.data)
            return redirect(url_for('recipe.personal_recipe_view'))

        return render_template('recipe/view_personal_recipe.html', all_recipe=all_recipe,
                               del_recipe_form=del_recipe_form)
    else:
        flash("У администратора нет личных рецептов", category='danger')
        return redirect(url_for('recipe.recipe_page_view'))


@recipe.route('/add_personal_recipe', methods=['GET', 'POST'])
@login_required
def personal_recipe_add():
    if session['role'] == 1:
        # Форма для добавления рецепта
        add_recipe_form = AddRecipeForm()

        # Заполнение категории рецепта
        add_recipe_form.category.choices = [i.name_category for i in RecipeCategory.get_all_category()]

        if add_recipe_form.submit_add.data:
            # Поиск ID категории блюда
            category_for_add = RecipeCategory.get_category_by_name(add_recipe_form.category.data)
            # Добавление нового рецепта
            Recipe.add_recipe(add_recipe_form.recipe_name.data, add_recipe_form.description.data,
                              add_recipe_form.date_publication.data, category_for_add.id_category,
                              add_recipe_form.photo.data, add_recipe_form.number_of_servings.data)
            # Публикация нового рецепта
            new_recipe = Recipe.get_recipes_by_name(add_recipe_form.recipe_name.data)
            Publication.add_recipe_to_user(new_recipe.id_recipe, current_user.get_id())

            return redirect(url_for('recipe.personal_recipe_view'))

        return render_template('recipe/add_personal_recipe.html', add_recipe_form=add_recipe_form)
    else:
        flash("Работа с рецептами чеез личную страницу доступен только пользователям", category='danger')
        return redirect(url_for('recipe.recipe_page_view'))
