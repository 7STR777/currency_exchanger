from sqlalchemy import select
from database import async_session_factory
from models import Users


class AsyncORM:
    @staticmethod
    async def insert_user(username: str, password: str, email: str):
        async with async_session_factory() as session:
            new_user = Users(username=username, password=password, email=email)
            session.add(new_user)
            await session.flush()
            await session.commit()

    @staticmethod
    async def select_user(username: str):
        async with async_session_factory() as session:
            query = select(Users).filter(Users.username==username)
            result = await session.execute(query)
            user = result.scalars().first()
            return user