# Cat charity fund v1.1.0

Проект представляет платформу для сбора средств на благотворительные проекты для кошек.

Проект собран на фреймворке FastAPI. После локального запуска прокта вся документакия к API будет доступна по адресам:
* http://127.0.0.1:8000/docs
* http://127.0.0.1:8000/redoc

## Изменения
Это новая версия v1.1.0 в которую добавлена возможность получения отчета в Google Sheets.
Был добавлен endpoint http://127.0.0.1:8000/google/
Для работы приложения теперь необходимо добавить в файл .env следующие константы:

```
TYPE
PROJECT_ID
PRIVATE_KEY_ID
PRIVATE_KEY # эту константу казываем в кавычках ""
CLIENT_EMAIL # эту константу казываем в кавычках ""
CLIENT_ID
AUTH_URI
TOKEN_URI
AUTH_PROVIDER_X509_CERT_URL
CLIENT_X509_CERT_URL
UNIVERSE_DOMAIN

EMAIL # Тут ваш личный email для google аккаунта
```

Все эти константы можно получить при создании нового проета на https://console.cloud.google.com/projectselector2/home/dashboard.

Пользователь обладающий правами суперюзера, может отправить запрос GET запрос на этот адрес.
В ответ придет ссылка на гугл таблицу с отчетом по проектам набравшим нужную сумму.
Проекты будут отсортированы по возрастанию времени, за которое была набрана сумма.
Если данных в таблице нет - в ответ вернется ошибка 404.

#### Проекты

В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

#### Пожертвования

Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.

#### Пользователи

Целевые проекты создаются администраторами сайта. 
Любой пользователь может видеть список всех проектов, включая требуемые и уже внесенные суммы. Это касается всех проектов — и открытых, и закрытых.
Зарегистрированные пользователи могут отправлять пожертвования и просматривать список своих пожертвований.

Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.

## Технологии

* Python3.9
* FastAPI
* FastAPI Users
* sqlAlchemy
* Alembic
* SQLite
* JSON

## Запуск проекта

Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

Переходим в папку проекта

```
cd cat_cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3.9 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Локальный запуск проекта:

Создаём файл .env.

Пример заполнения:
```
APP_TITLE=Сервис помощи котикам
APP_DESCRIPTION=Приложение для сбора пожертвований которые будут направлены на помощь котикам.
DATABASE_URL=sqlite+aiosqlite:///./qrkot.db
SECRET=Вместо этой надписи можно побиться головой об клаву или поездить по ней лицом, желательно не своим
FIRST_SUPERUSER_EMAIL=Вашемыло@ya.ru
FIRST_SUPERUSER_PASSWORD=Супер_сложный_пароль

```

Применяем миграции

```
alembic upgrade head
```

Стартуем

```
uvicorn app.main:app --reload
```
