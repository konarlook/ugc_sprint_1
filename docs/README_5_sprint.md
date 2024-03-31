 # Проектная работа 5 спринта

В папке **tasks** ваша команда найдёт задачи, которые необходимо выполнить во втором спринте модуля "Сервис Async API".

Как и в прошлом спринте, мы оценили задачи в стори поинтах.

Вы можете разбить эти задачи на более маленькие, например, распределять между участниками команды не большие куски задания, а маленькие подзадачи. В таком случае не забудьте зафиксировать изменения в issues в репозитории.

**От каждого разработчика ожидается выполнение минимум 40% от общего числа стори поинтов в спринте.**



Ссылка на репозиторий:
https://github.com/samtonck/sprint_4_and_5_team_5

Участники проекта:
Анатолий Кротов https://github.com/samtonck
Григорий Мосягин https://github.com/RSstrobe
Дмитрий Усиков https://github.com/konarlook




## Инструкция по поднятию сервиса

1. Создать в корне проекта `.env` по подобию `.env.example` (для ускорения развертки и проверки переменные окружения
   можно скопировать)
2. Для запуска проекта необходимо выполнить команду `docker-compose up -d` в корне проекта - `.../sprint_4_and_5_team_5`
3. При первичном запуске необходимо запустить скрипт миграции данных из sqlite в Postgres. Это необходимо сделать в
   контейнере `backend`. Команда в
   терминале `docker exec -it backend bash` -> `cd sqlite_to_postgres` -> `python load_data.py`

*. После запуска проекта и миграции бд необходимо подождать 1-2 минуты чтобы данные прокинулись в эластик

## Инструкция по поднятию тестов
1. Создать `.env` по подобию `.env.example` по пути `./fastapi/tests/functional`
2. Для запуска проекта необходимо выполнить команду `docker-compose up -d`, лежащего по пути `./fastapi/tests/functional`
3. После поднятия контейнеров, дождаться прохождения всех тестов


Урлы которые пригодятся для проверки:

   * FastAPI = http://localhost/api/openapi

   * Elasticvue = http://localhost:8080/

   * Redisvue = http://localhost:8081/