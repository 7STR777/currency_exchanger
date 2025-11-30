from database import Base, str_256, str_3, str_50
from sqlalchemy import ForeignKey, Numeric, text
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated
import datetime

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]

class Users(Base): 
    __tablename__ = "users"

    user_id: Mapped[intpk]
    username: Mapped[str_256]
    password: Mapped[str_256]
    email: Mapped[str]

class Conversion_history(Base):
    __tablename__ = "conversion_history"

    history_id: Mapped[intpk]
    user_id:Mapped[int] =  mapped_column(ForeignKey("users.user_id", ondelete='CASCADE'))
    from_currency: Mapped[str_3]
    to_currency: Mapped[str_3]
    amount: Mapped[Decimal] = mapped_column(Numeric(precision=20, scale=2))
    result: Mapped[Decimal] = mapped_column(Numeric(precision=20, scale=2))
    timestamp: Mapped[created_at]

class Banners(Base):
    __tablename__ = "banners"

    banner_id: Mapped[intpk]
    code: Mapped[str]

class Reviews(Base):
    __tablename__ = "reviews"

    review_id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    user_name: Mapped[str_50]
    rating: Mapped[int]
    comment: Mapped[str]
    timestamp: Mapped[created_at]

class Articles(Base):
    __tablename__ = "articles"

    article_id: Mapped[intpk]
    title: Mapped[str_256]
    intro_text: Mapped[str]
    full_text: Mapped[str]