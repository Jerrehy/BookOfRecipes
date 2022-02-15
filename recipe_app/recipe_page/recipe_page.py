from flask import Blueprint, render_template, redirect, url_for
from recipe_app.models import Recipe
from recipe_app.forms import RecipeInfoById

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
        pass

    return render_template('recipe/main.html', all_recipe=all_recipe, info_about_recipe=info_about_recipe)
