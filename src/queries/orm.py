from sqlalchemy import select, delete
from database import async_session_factory
from models import Users, Banners, Articles, Reviews
from datetime import datetime


class AsyncORM:
    @staticmethod
    async def insert_user(username: str, password: str, email: str, role = "user"):
        async with async_session_factory() as session:
            new_user = Users(username=username, password=password, email=email, role=role)
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
        
    @staticmethod
    async def insert_article_into_db(title: str, intro_text: str, full_text: str, codeimg: str):
        async with async_session_factory() as session:
            new_article = Articles(title=title, intro_text=intro_text, full_text=full_text, codeimg=codeimg)
            session.add(new_article)
            await session.flush()
            await session.commit()

    @staticmethod
    async def get_article_by_id(article_id: int):
        async with async_session_factory() as session:
            query = select(Articles).filter(Articles.article_id == article_id)
            result = await session.execute(query)
            article = result.scalars().first()
            return article
        
    @staticmethod
    async def get_review_from_db():
        async with async_session_factory() as session:
            query = select(Reviews)
            result = await session.execute(query)
            reviews = result.scalars().all()
            return reviews
        
    @staticmethod
    async def insert_review_into_db(user_id: int, username: str, rating: int, comment: str, timestamp: datetime):
        async with async_session_factory() as session:
            new_review = Reviews(user_id=user_id, username=username, rating=rating, comment=comment, timestamp=timestamp)
            session.add(new_review)
            await session.flush()
            await session.commit()

    @staticmethod
    async def delete_article(article_id: int):
        async with async_session_factory() as session:
            stmt = delete(Articles).where(Articles.article_id==article_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def deltete_review(review_id: int):
        async with async_session_factory() as session:
            stmt = delete(Reviews).where(Reviews.review_id==review_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def insert_banner_into_db(code: str):
        async with async_session_factory() as session:
            new_banner = Banners(code=code)
            session.add(new_banner)
            await session.flush()
            await session.commit()

    @staticmethod
    async def delete_banner(banner_id: int):
        async with async_session_factory() as session:
            stmt = delete(Banners).where(Banners.banner_id == banner_id)
            await session.execute(stmt)
            await session.commit()