from django.contrib import admin

from recipes.models import Ingredient, Recipe, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('slug',)
    list_filter = ('slug',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = ('name', 'measurement_unit',)
    list_filter = ('measurement_unit',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
        'cooking_time',
        'pub_date'
    )
    search_fields = ('name', 'author__username', 'ingredients__name')
    list_filter = ('tags', 'pub_date',)
    list_editable = ('name', 'cooking_time',)
    filter_horizontal = ('tags', 'ingredients')


admin.site.empty_value_display = 'Не задано'
