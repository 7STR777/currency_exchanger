from database import Base, str_256
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated

intpk = Annotated[int, mapped_column(primary_key=True)]


class Users(Base): 
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str_256]
    password: Mapped[str_256]