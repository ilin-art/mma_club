# Elevate MMA Beta version :tada:  

# Описание сервиса
Сайт Elevate MMA, «Спортивные единоборства». CRM-cервис для ведения учета данных.<br>
Сайт предназначен для ведения учета данных, таких как регистрация клиентов,
отображение дополнительных данных в профиле клиента, запись на тренировки,
создание напоминаний когда нужно написать или позвонить клиенту, сохранение ответов от клиентов.
В дальнейшем будут введены учет внесения клиентом платы, подсчет зарплаты тренерам, отображение выручки клуба.

# Для запуска проекта
- Создайте виртуальное окружение и подключите его.
```
python -m venv venv
source venv/Scripts/activate
```
- Установите все зависимости из файла requirements.txt
```
pip install -r requirements.txt
```
- Запустите проект
```
python manage.py runserver
```
Если вы это сделали на локальной машине. Сайт будет доступен по адресу http://localhost/ / http://127.0.0.1:8000/

# Технологии
* Python 3.9.9
* Django
* Django REST
* SQLite3<br>
Финальная версия будет переведена на SQL Postgres и работать через Docker

# Проект разработал:
* [Ильин Артём](https://github.com/ilin-art)
