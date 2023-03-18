## Asyncio. API swapi.
### Асинхронная загрузка персонажей swapi и асинхронное сохранение в БД. Netology homework.

### Что реализовано:
<br>main_tasks.py - асинхронность реализована тасками.
<br>main_cycle.py - асинхронность реализована простым циклом,без тасок. Закомментирован.
<br>models.py - файл с моделью
<br>print_all_from_db_query.py - для вывода из БД и очистки таблицы. Обычная sqlalchemy.
<br>print_all_from_db_async.py - для асинхронной выгрузки из ДБ.
<br>(В коде учтён вариант наличия страниц с отсутствием инф-ции по id. (Например id=17 404 'Not found')

### Запуск:

```shell
docker-compose up -d
```
<br>Далее:
<br>main_tasks.py - RUN.
<br>Для очистки БД: print_all_from_db_query.py - RUN.