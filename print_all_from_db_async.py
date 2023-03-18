from pprint import pprint
from models import SwapiPeople, Session
from sqlalchemy.future import select
import asyncio


async def _load_all():
    async with Session() as session:
        q = select(SwapiPeople)
        result = await session.execute(q)
        curr = result.scalars()
        CACHE = {i.id: i.name for i in curr}  # i.films, i.homeworld, i.starships и т.д.
        pprint(CACHE)
        print(len(CACHE))


# asyncio.run(_load_all())

