from flask_sqlalchemy_lite import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

#Base class
class Base(DeclarativeBase):
    pass

#contacts table
class contacts(Base):
    __tablename__= "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[int] = mapped_column()
    notes: Mapped[str] = mapped_column()
