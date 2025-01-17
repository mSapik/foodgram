from django_filters.rest_framework import filters, FilterSet
from recipes.models import Ingredient, Recipe, Tag


class UserFilterMixin:
    """
    Миксин для фильтрации по пользователю.
    """

    def filter_by_user(self, queryset, user_field, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(**{user_field: self.request.user})
        return queryset


class RecipeFilter(UserFilterMixin, FilterSet):
    author = filters.CharFilter(field_name='author__id')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug'
    )
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('name',)

    def filter_is_favorited(self, queryset, name, value):
        return self.filter_by_user(queryset, 'recipe__user', value)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        return self.filter_by_user(queryset, 'shoping_list__user', value)


class IngredientFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class TagFilter(UserFilterMixin, FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    class Meta:
        model = Tag
        fields = ('name',)

    def filter_is_favorited(self, queryset, name, value):
        return self.filter_by_user(queryset, 'users_recipe__user', value)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        return self.filter_by_user(queryset, 'shopping_cart__user', value)
