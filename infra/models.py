from dataclasses import dataclass
from enum import StrEnum
from typing import List

from sqlalchemy import MetaData, PickleType
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from protos.chat_by_recipe_pb2 import ChatByRecipeRole

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


"""
Following models are not database models,
they are simply used as in-memory data structures.
"""


class ChatRoleModel(StrEnum):
    """Chat role model"""

    USER = "user"
    ASSISTANT = "assistant"

    @classmethod
    def from_proto(cls, role: ChatByRecipeRole) -> "ChatRoleModel":
        """Create a role from a proto role.

        Arguments:
            role (ChatByRecipeRole): The proto role.

        Returns:
            ChatRoleModel: The new role.
        """
        if role == ChatByRecipeRole.USER:
            return cls.USER
        if role == ChatByRecipeRole.ASSISTANT:
            return cls.ASSISTANT

    def to_proto(self) -> ChatByRecipeRole:
        """Convert the role to a proto role.

        Returns:
            ChatByRecipeRole: The proto role.
        """
        if self == self.USER:
            return ChatByRecipeRole.USER
        if self == self.ASSISTANT:
            return ChatByRecipeRole.ASSISTANT


@dataclass
class ChatMessageModel:
    """Chat message model"""

    role: ChatRoleModel
    text: str

    def __repr__(self) -> str:
        return f"ChatMessage(role={self.role}, text={self.text})"


@dataclass
class ChatStreamHeaderModel:
    """Chat stream header model"""

    role: ChatRoleModel

    def __repr__(self) -> str:
        return f"ChatStreamHeader(role={self.role})"


@dataclass
class ChatStreamContentModel:
    """Chat stream content model"""

    text: str

    def __repr__(self) -> str:
        return f"ChatStreamContent(text={self.text})"


ChatStreamModel = ChatStreamHeaderModel | ChatStreamContentModel
