from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, viewsets

from recipes.models import AmountIngredient


class IngridientTagMixin(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Миксин для работы с тегами и ингредиентами.
    """
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    permission_classes = (permissions.AllowAny,)


class AmountMixin:
    """
    Миксин для работы с количеством ингредиентов.
    """

    def update_or_create_ingredient(self, recipe, ingredients: list) -> None:
        """
        Обновляет или создает ингредиенты для рецепта.
        """
        recipe.ingredients.clear()
        ingredient_list = [
            AmountIngredient(
                recipe=recipe,
                ingredient_id=ingredient['id'].id,
                amount=ingredient['amount']
            )
            for ingredient in ingredients
        ]
        AmountIngredient.objects.bulk_create(ingredient_list)


class ChosenMixin():
    """
    Миксин для работы с выбранными рецептами.
    """

    def get_chosen_recipe(self, obj, model) -> bool:
        """
        Метод получения статуса выбранного рецепта.

        Используется для избранного и списка покупок.
        """
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return model.objects.filter(user=user, recipe=obj).exists()
