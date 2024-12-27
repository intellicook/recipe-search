from dataclasses import dataclass
from enum import StrEnum
from typing import List, Optional

from sqlalchemy import MetaData, PickleType
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from protos.chat_by_recipe_pb2 import ChatByRecipeRole
from protos.search_recipes_pb2 import SearchRecipesMatchField

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


@dataclass
class TypesenseResultHighlight:
    """Typesense search result highlight class."""

    class Field(StrEnum):
        """Typesense search result highlight field class."""

        NAME = "name"
        INGREDIENTS = "ingredients"

        def to_proto(self) -> SearchRecipesMatchField:
            """Convert the result highlight field to a proto object.

            Returns:
                SearchRecipesMatchField: The proto object.
            """
            if self == self.NAME:
                return SearchRecipesMatchField.NAME
            if self == self.INGREDIENTS:
                return SearchRecipesMatchField.INGREDIENTS

    field: Field
    tokens: List[str]
    index: Optional[int] = None


@dataclass
class TypesenseResult:
    """Typesense search result class."""

    recipe: RecipeModel
    highlights: List[TypesenseResultHighlight]

    def from_json(json: dict) -> "TypesenseResult":
        """Create a result from a JSON object.

        Arguments:
            json (dict): The JSON object.

        Returns:
            TypesenseResult: The result.
        """
        recipe = RecipeModel(
            id=int(json["document"]["id"]),
            name=json["document"]["name"],
            ingredients=json["document"]["ingredients"],
        )

        highlights = [
            (
                [
                    TypesenseResultHighlight(
                        field=TypesenseResultHighlight.Field.NAME,
                        tokens=highlight["matched_tokens"],
                    )
                ]
                if highlight["field"] == "name"
                else [
                    TypesenseResultHighlight(
                        field=TypesenseResultHighlight.Field.INGREDIENTS,
                        tokens=tokens,
                        index=index,
                    )
                    for index, tokens in zip(
                        highlight["indices"], highlight["matched_tokens"]
                    )
                ]
            )
            for highlight in json["highlights"]
        ]
        highlights = [
            highlight for sublist in highlights for highlight in sublist
        ]

        return TypesenseResult(recipe=recipe, highlights=highlights)


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
