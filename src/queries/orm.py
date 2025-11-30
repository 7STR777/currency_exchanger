from sqlalchemy import select
from database import async_session_factory
from models import Users, Banners, Articles


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

    @staticmethod
    async def select_banners():
        async with async_session_factory() as session:
            query = select(Banners)
            result = await session.execute(query)
            banners = result.scalars().all()
            return banners
        
    @staticmethod
    async def get_article_from_db():
        async with async_session_factory() as session:
            query = select(Articles)
            result = await session.execute(query)
            articles = result.scalars().all()
            return articles