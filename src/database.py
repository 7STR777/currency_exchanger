from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from typing import Annotated
from config import settings


async_engine = create_async_engine(
    url = settings.DATABASE_URL_asyncpg,
    echo = False
)
async_session_factory = async_sessionmaker(async_engine)

str_3 = Annotated[str, 3]
str_256 = Annotated[str, 256]
str_50 = Annotated[str, 50]

class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256),
        str_3: String(3)
    }

    repr_cols_num = 3
    repr_cols = tuple()
    

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
