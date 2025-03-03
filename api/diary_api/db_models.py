
import datetime
from uuid import uuid4

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


def generate_uuid():
    return str(uuid4())


# TODO default factory for uuids here
class TodoCategory(Base):
    __tablename__ = "app_todocategory"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(256))
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    deactivate_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)

    todos: Mapped[list["Todo"]] = relationship(back_populates="category", cascade="all, delete-orphan")


class Todo(Base):
    __tablename__ = "app_todo"
    id: Mapped[str] = mapped_column(primary_key=True, default=generate_uuid)
    text: Mapped[str] = mapped_column(String(256))
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    complete_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    category_id: Mapped[str] = mapped_column(ForeignKey("app_todocategory.id"))

    category: Mapped[TodoCategory] = relationship(back_populates="todos")


class DiaryEntry(Base):
    __tablename__ = "app_diaryentry"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    text: Mapped[str] = mapped_column(Text)
    date: Mapped[datetime.date] = mapped_column(Date)
