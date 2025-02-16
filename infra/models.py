from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Dict, List, Optional

from sqlalchemy import MetaData, PickleType
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from protos.chat_by_recipe_pb2 import ChatByRecipeRole
from protos.recipe_nutrition_pb2 import RecipeNutritionValue
from protos.search_recipes_pb2 import SearchRecipesMatchField

Base = declarative_base(metadata=MetaData(schema="public"))


@dataclass
class RecipeModelIngredient:
    """Recipe model ingredient class."""

    name: str
    quantity: Optional[str] = None
    unit: Optional[str] = None

    def __repr__(self) -> str:
        return (
            f"RecipeModelIngredient(name={self.name},"
            f" quantity={self.quantity}, unit={self.unit})"
        )

    def as_dict(self) -> Dict[str, Any]:
        """Get the ingredient as a dictionary."""
        return {
            "name": self.name,
            "quantity": self.quantity,
            "unit": self.unit,
        }


class RecipeModelNutritionValue(StrEnum):
    """Recipe model nutrition value class."""

    high = "high"
    medium = "medium"
    low = "low"
    none = "none"

    @classmethod
    def from_proto(
        cls, value: RecipeNutritionValue
    ) -> "RecipeModelNutritionValue":
        """Create a nutrition value from a proto value.

        Arguments:
            value (str): The proto value.

        Returns:
            RecipeModelNutritionValue: The new nutrition value.
        """
        if value == RecipeNutritionValue.HIGH:
            return cls.high
        if value == RecipeNutritionValue.MEDIUM:
            return cls.medium
        if value == RecipeNutritionValue.LOW:
            return cls.low
        if value == RecipeNutritionValue.NONE:
            return cls.none

    def to_proto(self) -> str:
        """Convert the nutrition value to a proto value.

        Returns:
            str: The proto value.
        """
        if self == self.high:
            return RecipeNutritionValue.HIGH
        if self == self.medium:
            return RecipeNutritionValue.MEDIUM
        if self == self.low:
            return RecipeNutritionValue.LOW
        if self == self.none:
            return RecipeNutritionValue.NONE


@dataclass
class RecipeModelNutrition:
    """Recipe model nutrition class."""

    calories: RecipeModelNutritionValue
    fat: RecipeModelNutritionValue
    protein: RecipeModelNutritionValue
    carbs: RecipeModelNutritionValue

    def __repr__(self) -> str:
        return (
            f"RecipeModelNutrition(calories={self.calories},"
            f" fat={self.fat}, protein={self.protein}, carbs={self.carbs})"
        )

    def as_dict(self) -> Dict[str, str]:
        """Get the nutrition as a dictionary."""
        return {
            "calories": self.calories,
            "fat": self.fat,
            "protein": self.protein,
            "carbs": self.carbs,
        }


class RecipeModel(Base):
    """Recipe model"""

    __tablename__ = "recipe"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    ingredients: Mapped[List[RecipeModelIngredient]] = mapped_column(
        MutableList.as_mutable(PickleType)
    )
    directions: Mapped[List[str]] = mapped_column(
        MutableList.as_mutable(PickleType)
    )
    tips: Mapped[List[str]] = mapped_column(MutableList.as_mutable(PickleType))
    utensils: Mapped[List[str]] = mapped_column(
        MutableList.as_mutable(PickleType)
    )
    nutrition: Mapped[RecipeModelNutrition] = mapped_column(PickleType)

    def __repr__(self) -> str:
        return (
            f"RecipeModel(id={self.id}, title={self.title},"
            f" description={self.description}, ingredients={self.ingredients},"
            f" directions={self.directions}, tips={self.tips},"
            f" utensils={self.utensils}, nutrition={self.nutrition})"
        )

    def as_dict(self) -> Dict[str, Any]:
        """Get the recipe as a dictionary."""
        return {
            "title": self.title,
            "description": self.description,
            "ingredients": [
                ingredient.as_dict() for ingredient in self.ingredients
            ],
            "directions": self.directions,
            "tips": self.tips,
            "utensils": self.utensils,
            "nutrition": self.nutrition.as_dict(),
        }


"""
Following models are not database models,
they are simply used as in-memory data structures.
"""


@dataclass
class TypesenseResultHighlight:
    """Typesense search result highlight class."""

    class Field(StrEnum):
        """Typesense search result highlight field class."""

        TITLE = "title"
        DESCRIPTION = "description"
        INGREDIENTS = "ingredients"

        def to_proto(self) -> SearchRecipesMatchField:
            """Convert the result highlight field to a proto object.

            Returns:
                SearchRecipesMatchField: The proto object.
            """
            if self == self.TITLE:
                return SearchRecipesMatchField.TITLE
            if self == self.DESCRIPTION:
                return SearchRecipesMatchField.DESCRIPTION
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
            title=json["document"]["title"],
            description=json["document"]["description"],
            ingredients=[
                RecipeModelIngredient(name=ingredient)
                for ingredient in json["document"]["ingredients"]
            ],
        )

        def get_highlights(highlight: dict) -> List[TypesenseResultHighlight]:
            if highlight["field"] == "title":
                return [
                    TypesenseResultHighlight(
                        field=TypesenseResultHighlight.Field.TITLE,
                        tokens=highlight["matched_tokens"],
                    )
                ]

            if highlight["field"] == "description":
                return [
                    TypesenseResultHighlight(
                        field=TypesenseResultHighlight.Field.DESCRIPTION,
                        tokens=highlight["matched_tokens"],
                    )
                ]

            return [
                TypesenseResultHighlight(
                    field=TypesenseResultHighlight.Field.INGREDIENTS,
                    tokens=tokens,
                    index=index,
                )
                for index, tokens in zip(
                    highlight["indices"], highlight["matched_tokens"]
                )
            ]

        highlights = [
            get_highlights(highlight) for highlight in json["highlights"]
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
