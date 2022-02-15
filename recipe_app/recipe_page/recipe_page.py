from flask import Blueprint, render_template, redirect, url_for
from recipe_app.models import Recipe, IngredientInRecipe
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
        return redirect(url_for('recipe.one_recipe_page_view', id_recipe=info_about_recipe.id_recipe.data))

    return render_template('recipe/main.html', all_recipe=all_recipe, info_about_recipe=info_about_recipe)


@recipe.route('/recipe/<id_recipe>', methods=['GET', 'POST'])
def one_recipe_page_view(id_recipe):
    # Получение информации о текущем рецепте
    recipe_for_view = Recipe.get_recipe_by_id_with_category(id_recipe)
    # Вывод всех ингредиентов рецепта
    ingredients_in_recipe = IngredientInRecipe.get_all_ingredients_for_recipe(id_recipe)

    return render_template('recipe/one_recipe.html', recipe_for_view=recipe_for_view,
                           ingredients_in_recipe=ingredients_in_recipe)
