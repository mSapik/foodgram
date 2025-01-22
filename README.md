<p align="center">
    <img src="frontend/src/images/logo-footer.png" width="150">
</p>
# **_Foodgram_**
Foodgram – это не просто платформа, предоставляющая онлайн-сервис и API для рецептов, а целое кулинарное сообщество. Пользователи могут публиковать свои блюда, следить за публикациями друзей, сохранять понравившиеся рецепты и, что немаловажно, быстро составлять список покупок для их приготовления.

**_Ссылка на [проект](http://foodgram.sapik.ru "Cсылка на проект.")_**

**_Ссылка на [админку](http://foodgram.sapik.ru/admin/ "Ссылка на админку.")_**

### Проект использует:
Django
Python
Gunicorn
Nginx
JS
Node.js
PostgreSQL
Docker

### Установка
1. Клонируйте репозиторий:
    ```
    git clone git@github.com:msapik/foodgram.git
    ```
2. Создайте файл переменных окружения `.env` и заполните его. Пример файла с переменными окуржения `.env.example` находится в корне.
3. Создайте Docker образы для backend, frontend и nginx в соответствующих директориях:

    ```
    docker build -t YOUR_USERNAME/foodgram_frontend .
    docker build -t YOUR_USERNAME/foodgram_backend .
    docker build -t YOUR_USERNAME/foodgram_gateway . 
    ```
4. Загрузите образы на DockerHub:

    ```
    docker push YOUR_USERNAME/foodgram_frontend
    docker push YOUR_USERNAME/foodgram_backend
    docker push YOUR_USERNAME/foodgram_gateway
    ```
5. На удаленном сервере создайте папку `foodgram`, поместите в нее файл с переменными окружения`.env` и `docker-compose.yml`.

6. Запустите Docker Compose:
   ```
   sudo docker-compose -f ~/foodgram/docker-compose.yml up -d
   ```
   Выполните миграции и соберите статику.

Проект так же содержит Workflow для Github Actions. Workflow срабатывает при пуше в репозиторий, после деплоя вы получите сообщение в телергам.

Для сборки тестов и деплоя потребуется настроить секреты в репозитории github:

```
DOCKER_USERNAME имя пользователя в DockerHub,
DOCKER_PASSWORD пароль пользователя в DockerHub,
HOST IP-адрес сервера,
USER имя пользователя на сервере,
SSH_KEY содержимое приватного SSH-ключа,
SSH_PASSPHRASE пароль для SSH-ключа,
TELEGRAM_TO ID вашего телеграм-аккаунта,
TELEGRAM_TOKEN токен бота,
```

### Автор - [msapik](https://github.com/msapik)