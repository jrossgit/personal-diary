
import datetime
from uuid import uuid4

from sqlalchemy import CHAR, Date, DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


def generate_uuid():
    return str(uuid4())


class TodoCategory(Base):
    __tablename__ = "app_todocategory"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String)
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    deactivate_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)

    todos: Mapped[list["Todo"]] = relationship(back_populates="category", cascade="all, delete-orphan")


class Todo(Base):
    __tablename__ = "app_todo"
    id: Mapped[str] = mapped_column(primary_key=True, default=generate_uuid)
    text: Mapped[str] = mapped_column(String)
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    complete_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    category_id: Mapped[str] = mapped_column(ForeignKey("app_todocategory.id"))

    category: Mapped[TodoCategory] = relationship(back_populates="todos")

    __table_args__ = (
        Index(
            "app_todo_category_id_660031a8",
            category_id,
        ),
    )


class DiaryEntry(Base):
    __tablename__ = "app_diaryentry"
    category_id: Mapped[str] = mapped_column(ForeignKey("app_todocategory.id"))

    id: Mapped[str] = mapped_column(CHAR(length=256), primary_key=True, default=generate_uuid)
    text: Mapped[str] = mapped_column(Text)
    date: Mapped[datetime.date] = mapped_column(Date)

    category: Mapped[TodoCategory] = relationship(back_populates="todos")

    __table_args__ = (
        Index(
            "app_diaryentry_category_id_f4e1efad",
            category_id,
        ),
    )
