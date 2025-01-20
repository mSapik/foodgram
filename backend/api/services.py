from django.http import HttpResponse

from recipes.models import AmountIngredient


def shopping_list_txt(user) -> HttpResponse:
    """
    Функция скачивания текстового файла списка ингредиентов.
    """
    text_shop_list = 'Список покупок \n\n'
    measurement_unit = {}
    ingredient_amount = {}

    ingredients = AmountIngredient.objects.filter(
        recipe__shoping_list__user=user
    ).values(
        'ingredient__name', 'ingredient__measurement_unit', 'amount'
    )

    for ingredient in ingredients:
        name = ingredient['ingredient__name']
        unit = ingredient['ingredient__measurement_unit']
        amount = ingredient['amount']

        if name in ingredient_amount:
            ingredient_amount[name] += amount
        else:
            measurement_unit[name] = unit
            ingredient_amount[name] = amount

    for name, amount in ingredient_amount.items():
        text_shop_list += f'{name} - {amount} {measurement_unit[name]}\n'

    response = HttpResponse(text_shop_list, content_type='text/plain')
    response['Content-Disposition'] = (
        'attachment; filename="shopping_list.txt"'
    )

    return response
