from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from urlshortner.models import Url
from urlshortner.utils import shorten_url

from api import serializers
from api.filters import IngredientFilter, RecipeFilter, TagFilter
from api.mixins import IngridientTagMixin
from api.permissions import IsAuthorOrReadOnly
from api.services import shopping_list_txt
from recipes.models import (
    Favorite, Ingredient, Recipe, ShopingList, Tag
)
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для регистрации, получения и редактирования данных пользователя.
    """

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.SignUpSerializer
        if self.request.method == 'GET':
            return serializers.UserProfileSerializer

    @action(
        ['GET'],
        detail=False,
        url_name='current_user',
        permission_classes=[IsAuthenticated, ]
    )
    def me(self, request):
        serializer = serializers.UserProfileSerializer(
            request.user,
            context={'request': request}
        )
        return Response(data=serializer.data)

    @action(
        ['POST', 'DELETE'],
        detail=True,
        url_name='subscribe',
        permission_classes=[IsAuthenticated, ]
    )
    def subscribe(self, request, pk):
        author = get_object_or_404(User, id=self.kwargs.get('pk', None))
        user = self.request.user
        is_subscription_exist = user.subscriptions.filter(
            author=author
        ).exists()
        if request.method == 'POST':
            serializer = serializers.SubscribeSerializer(
                data=request.data,
                context={
                    'author': author,
                    'user': user,
                    'request': request,
                    'is_subscription_exist': is_subscription_exist}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if is_subscription_exist:
            user.subscriptions.get(author=author).delete()
            return Response('Успешная отписка',
                            status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Вы не подписаны на данного автора'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        ['GET'],
        detail=False,
        url_name='get_subscriptions',
        permission_classes=[IsAuthenticated, ],
    )
    def subscriptions(self, request):
        user = self.request.user
        paginate_subs = self.paginate_queryset(user.subscriptions.all())
        serializer = serializers.SubscribeSerializer(
            paginate_subs,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        ['POST'],
        detail=False,
        url_name='set_new_password',
        permission_classes=[IsAuthenticated, ]
    )
    def set_password(self, request):
        serializer = serializers.SetPasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.update(
            instance=self.request.user,
            validated_data=serializer.validated_data
        )
        return Response(
            'Пароль успешно изменен',
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        ['PUT', 'DELETE'],
        detail=False,
        url_path='me/avatar',
        permission_classes=[IsAuthenticated, ],
        url_name='set_avatar'
    )
    def avatar(self, request):
        user = request.user
        if request.method == 'PUT':
            if not request.data.get('avatar', None):
                return Response(
                    'Не выбран файл!',
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = serializers.UserProfileSerializer(
                user,
                data=request.data,
                partial=True,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {'avatar': serializer.data['avatar']},
                status=status.HTTP_200_OK
            )
        user.avatar = None
        user.save()
        return Response(
            'Аватар успешно удален',
            status=status.HTTP_204_NO_CONTENT
        )


class TagViewSet(IngridientTagMixin):
    """
    Вьюсет для просмотра тэгов.

    Доступно всем пользователям.
    """

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    filterset_class = TagFilter


class IngredientViewSet(IngridientTagMixin):
    """
    Вьюсет для просмотра ингредиентов.

    Доступно всем пользователям.
    """

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для создания, удаления, редактирования, получения рецептов.
    """

    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    permission_classes = [IsAuthorOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return serializers.RecipeGetSerializer
        return serializers.RecipeSerializer

    @action(
        ['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated, ],
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_recipe(request, ShopingList, pk, 'SHOPPING_CART')
        return self.delete_recipe(request, ShopingList, pk, 'SHOPPING_CART')

    @action(
        ['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated, ],
    )
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.add_recipe(request, Favorite, pk, 'FAVORITE')
        return self.delete_recipe(request, Favorite, pk, 'FAVORITE')

    def add_recipe(self, request, model, pk, error_key):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        if model.objects.filter(recipe=recipe, user=user).exists():
            return Response(
                'Рецепт уже добавлен',
                status=status.HTTP_400_BAD_REQUEST
            )
        model.objects.create(recipe=recipe, user=user)
        serializer = serializers.RecipeMiniSerializer(recipe)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete_recipe(self, request, model, pk, error_key):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        try:
            obj = get_object_or_404(model, recipe=recipe, user=user)
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(
                'Рецепт не добавлен',
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        ['GET'],
        detail=False,
        permission_classes=[IsAuthenticated, ],
    )
    def download_shopping_cart(self, request):
        if not request.user.shoping_list.exists():
            return Response(
                'Список покупок пуст.',
                status=status.HTTP_404_NOT_FOUND
            )
        return shopping_list_txt(user=request.user)

    @action(
        ['GET'],
        detail=True,
        url_path='get-link',
        url_name='get_link',
        permission_classes=[AllowAny, ]
    )
    def get_link(self, request, pk):
        """
        Создание/получение короткой ссылки на рецепт.
        """
        main_domain = request.build_absolute_uri().replace(
            request.get_full_path(), ''
        )
        url_route_to_recipe = f'{main_domain}/recipes/{pk}/'
        short_url = Url.objects.filter(url=url_route_to_recipe).first()
        if short_url:
            final_short_link = f'{main_domain}/s/{short_url.short_url}/'
            return Response({'short-link': final_short_link})
        url_route_to_recipe = shorten_url(
            url_route_to_recipe, is_permanent=False)
        final_short_link = f'{main_domain}/s/{url_route_to_recipe}'
        return Response({'short-link': final_short_link})
