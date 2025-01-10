from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        max_length=50,
        verbose_name='Электронная почта'
    )
    username = models.CharField(
        verbose_name='Логин', max_length=50, unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя', max_length=50
    )
    last_name = models.CharField(
        verbose_name='Фамилия', max_length=50
    )
    role = models.CharField(
        max_length=20,
        choices=(
            ('user', 'User'),
            ('admin', 'Admin')
        ),
        default='user',
        verbose_name='Роль'
    )
    avatar = models.ImageField(
        upload_to='users_avatar/',
        null=True,
        verbose_name='Аватар',
        default=None
    )

    class Meta:
        default_related_name = 'user'
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'профили пользователей'

    def __str__(self) -> str:
        return self.username
