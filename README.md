### бэкенд для образовательного мобильного приложения
## Установка
#### нет времени?
запустите многовенно при помощи докера
```shell
docker-compose up
```

Откройте виртуальное окружение при помощи pipenv и скачайте зависимисти
```shell
pipenv shell
pipenv install
```

У вас должен быть установлен и запущен PostgreSQL

Задайте переменные окружения
```shell
SECRET_KEY=your_secret_key
DEBUG_MODE=True
DATABASE_URL=postgres://user:password@host:port/dbname

EMAIL_HOST=smtp_server_address
EMAIL_USE_TLS=True
EMAIL_PORT=smtp_server_port
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=email_app_password
DEFAULT_FROM_EMAIL=default_from_email
```
сделайте миграции и можно запускать
```shell
python manage.py migrate
python manage.py runserver
```
так же запустите месячные задания
```
manage.py runjobs monthly
```

###Описание
документация API доступна в урлах `/api/swagger/` и `/api/redoc/`

(пример `localhost:8000/swagger`)

__Внимание!__
На данный момент платежная система не работает