## Installation
install dependencies via pipenv
```shell
pipenv shell
pipenv install
```

set up postgresql and environment variable
```shell
SECRET_KEY=your_secret_key
DEBUG_MODE=True
DATABASE_URL=postgres://user:password@host:port/dbname
```
migrate and run
```shell
python manage.py migrate
python manage.py runserver
```

documentation is available on `/swagger` (example `localhost:8000/swagger`)


You can also use docker
```shell
docker-compose up
```