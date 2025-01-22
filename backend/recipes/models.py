from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.constants import (ING_NAME_LENGHT, MAX_STR_VALUE, MAX_VALUE,
                           MEAS_NAME_LENGHT, MIN_VALUE, RECIPE_NAME_LENGHT,
                           TAG_NAME_LENGHT)
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=TAG_NAME_LENGHT,
        verbose_name='Название тэга'
    )
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'тэги'
        ordering = ('name',)
        default_related_name = 'tags'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=ING_NAME_LENGHT,
        verbose_name='Ингредиент',
        unique=True
    )
    measurement_unit = models.CharField(
        max_length=MEAS_NAME_LENGHT,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'ингредиенты'
        ordering = ('name',)
        default_related_name = 'ingredient'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient')
        ]

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=RECIPE_NAME_LENGHT,
        verbose_name='Название рецепта'
    )
    text = models.TextField(verbose_name='Рецепт')
    image = models.ImageField(
        blank=False,
        upload_to="recipes/images/",
        verbose_name='Изображение'
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='AmountIngredient',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги'
    )
    cooking_time = models.IntegerField(
        validators=(
            MinValueValidator(MIN_VALUE),
            MaxValueValidator(MAX_VALUE)
        ),
        verbose_name='Время приготовления'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ('-pub_date',)
        default_related_name = 'recipe'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'author'],
                name='unique_recipe')
        ]

    def str(self):
        return self.text


class AmountIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_ingredients',
        verbose_name='Название рецепта',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(MIN_VALUE),
            MaxValueValidator(MAX_VALUE)
        ),
        verbose_name='Количество ингредиента',
    )

    class Meta:
        ordering = ('amount',)
        verbose_name = 'Состав рецепта'
        verbose_name_plural = 'Состав рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredients')
        ]

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        related_name='subscriptions',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='subscribers',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'подписки'
        ordering = ('user',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subs')
        ]

    def __str__(self) -> str:
        return f'{self.user} {self.author}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'избранные рецепты'
        ordering = ('recipe',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_fav_recipe'
            ),
        ]


class ShopingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'списки покупок'
        ordering = ('recipe',)
        default_related_name = 'shoping_list'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shoping_list'
            )
        ]

    def __str__(self):
        return f'{self.recipe}'[:MAX_STR_VALUE]
