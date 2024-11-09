from typing import List

from sqlalchemy import MetaData, PickleType
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base(metadata=MetaData(schema="public"))


class RecipeModel(Base):
    """Recipe model"""

    __tablename__ = "recipe"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    ingredients: Mapped[List[str]] = mapped_column(
        MutableList.as_mutable(PickleType)
    )
    instructions: Mapped[List[str]] = mapped_column(
        MutableList.as_mutable(PickleType)
    )
    raw: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return (
            f"Recipe(name={self.name}, ingredients={self.ingredients},"
            f" instructions={self.instructions})"
        )


class IndexFileModel(Base):
    """Index file model"""

    __tablename__ = "index_file"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    count: Mapped[int] = mapped_column()
    model: Mapped[str] = mapped_column()
    path: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"IndexFile(path={self.path})"
