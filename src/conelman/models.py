from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from typing import Optional

#Base class
class Base(DeclarativeBase):
    pass

#Contacts table model
class Contact(Base):
    __tablename__= "contact"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    phone: Mapped[int] = mapped_column(unique=True)
    notes: Mapped[Optional[str]] = mapped_column(default="")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

#User table model
class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement= True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[int]