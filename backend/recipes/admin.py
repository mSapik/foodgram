from django.contrib import admin

from recipes.models import Favorite, Ingredient, Recipe, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name', 'slug',)
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
        'pub_date',
        'in_favorites',
    )
    search_fields = ('name', 'author__username', 'ingredients__name')
    list_filter = ('tags', 'pub_date',)
    list_editable = ('name',)
    filter_horizontal = ('tags', 'ingredients')
    readonly_fields = ('in_favorites',)

    def in_favorites(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


admin.site.empty_value_display = 'Не задано'
