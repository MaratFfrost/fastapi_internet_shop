from typing import Optional
from sqlalchemy import delete, insert, select
from app.database import async_session_maker

class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filters):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_limit_by_filter(cls, limit: Optional[int] = None, **filters):
      async with async_session_maker() as session:
        query = select(cls.model).filter_by(**filters)
        if limit is not None:
          query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().all()


    @classmethod
    async def add(cls, **information):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**information)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_by_filters(cls, **filters):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filters)
            await session.execute(query)
            await session.commit()
