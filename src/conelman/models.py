from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import Optional

#Base class
class Base(DeclarativeBase):
    pass

#Contacts table model
class Contact(Base):
    __tablename__= "contact"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    phone: Mapped[int] = mapped_column(String(9))
    notes: Mapped[Optional[str]] = mapped_column(String(200))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

#User table model
class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement= True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(String(25))

    contacts = relationship("Contact", backref="user")