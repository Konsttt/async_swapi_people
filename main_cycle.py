# import asyncio
# import aiohttp
# import datetime
# import requests
# from models import SwapiPeople, engine, Base, Session
# from get_all import _load_all
#
#
# # Вспомогательная функция по выкачиванию по ссылкам links вложенных сущностей персонажа (films, starhips и т.д.)
# async def download_links(links_list, client_session):
#     coros = [client_session.get(link) for link in links_list]
#     http_responses = await asyncio.gather(*coros)
#     json_coros = [http_response.json() for http_response in http_responses]
#     return await asyncio.gather(*json_coros)
#
#
# # Основная функция запроса по персонажу и сбора требуемых сущностей из json-ответа.
# async def get_people(people_id, client_session):
#     async with client_session.get(f'https://swapi.dev/api/people/{people_id}') as response:
#         people_dict = {}  # Результирующий словарь для одного персонажа
#         # Получаем асинхронно json-ответ сервера по персонажу
#         json_data = await response.json()
#         # Если страничка с данным id-шником не найдена, то возвращаем пустой словарь
#         if json_data.get('detail') == 'Not found':
#             return {}
#
#         # Собираем простые(не вложенные) сущности
#         people_dict['id'] = people_id
#         people_dict['name'] = json_data.get('name', [])
#         people_dict['birth_year'] = json_data.get('birth_year', [])
#         people_dict['eye_color'] = json_data.get('eye_color', [])
#         people_dict['gender'] = json_data.get('gender', [])
#         people_dict['hair_color'] = json_data.get('hair_color', [])
#         people_dict['height'] = json_data.get('height', [])
#         people_dict['mass'] = json_data.get('mass', [])
#         people_dict['skin_color'] = json_data.get('skin_color', [])
#
#         # Формируем списки ссылок для вложенных сущностей
#         film_links = json_data.get('films', [])
#         homeworld_links = [json_data.get('homeworld', [])]
#         species_links = json_data.get('species', [])
#         starships_links = json_data.get('starships', [])
#         vehicles_links = json_data.get('vehicles', [])
#
#         # Формируем корутины по спискам ссылок вложенных сущностей
#         films_coro = download_links(film_links, client_session)
#         homeworld_coro = download_links(homeworld_links, client_session)
#         species_coro = download_links(species_links, client_session)
#         starships_coro = download_links(starships_links, client_session)
#         vehicles_coro = download_links(vehicles_links, client_session)
#
#         # Собираем асинхронно список json-ов по каждой вложенной ссылке. Из полей name и title формируем строки.
#         fields_ = await asyncio.gather(films_coro, homeworld_coro, species_coro, starships_coro, vehicles_coro)
#         films, homeworld, species, starships, vehicles = fields_
#         people_dict['films'] = ', '.join([f'"{film["title"]}"' if len(films) > 0 else [] for film in films])
#         people_dict['homeworld'] = homeworld[0]['name']  # Сохраняем в БД не ссылку, а имя планеты
#         people_dict['species'] = ', '.join([species_item['name'] if len(species) > 0 else [] for species_item in species])
#         people_dict['starships'] = ', '.join([starship['name'] if len(starships) > 0 else [] for starship in starships])
#         people_dict['vehicles'] = ', '.join([vehicle['name'] if len(vehicles) > 0 else [] for vehicle in vehicles])
#         return people_dict
#
#
# async def main(all_count, id_=1, n=10):
#     """ Функция: сохраняет асинхронно готовые словари по каждому персонажу в БД.
#     id_ - начальный индекс с которого начинаем выкачивать/сохранять записи.
#     n - кол-во в одной партии за 1 раз (таска), по умолчанию 10 записей за раз.
#     all_count - общее кол-во пользователей swapi"""
#     # Первоначальная миграция
#     async with engine.begin() as con:
#         await con.run_sync(Base.metadata.create_all)
#
#     count = 0
#     while True:
#         # Выкачиваем одну партию (асинхронно)
#         async with aiohttp.ClientSession() as client_session:
#             coros = [get_people(i, client_session) for i in range(id_, id_+n)]
#             results = await asyncio.gather(*coros)
#         id_ += n
#
#         async with Session() as session:
#             orm_objects = []
#             for result in results:
#
#                 if len(result) != 0:  # обход значений, таких как id=17 404 'Not found'
#                     orm_objects.append(SwapiPeople(id=result['id'],
#                                                    name=result['name'],
#                                                    birth_year=result['birth_year'],
#                                                    eye_color=result['eye_color'],
#                                                    films=result['films'],
#                                                    gender=result['gender'],
#                                                    hair_color=result['hair_color'],
#                                                    height=result['height'],
#                                                    homeworld=result['homeworld'],
#                                                    mass=result['mass'],
#                                                    skin_color=result['skin_color'],
#                                                    species=result['species'],
#                                                    starships=result['starships'],
#                                                    vehicles=result['vehicles']))
#                     count += 1
#             session.add_all(orm_objects)
#             await session.commit()
#         if count == all_count:
#             break
#
#
# if __name__ == '__main__':
#     # Получаем общее кол-во персонажей получаем обычным запросом
#     count_all_people = int(requests.get('https://swapi.dev/api/people/').json()['count'])
#     print(count_all_people)
#     # Засекаем время
#     start = datetime.datetime.now()
#     asyncio.run(main(count_all_people))
#     print(datetime.datetime.now() - start)
