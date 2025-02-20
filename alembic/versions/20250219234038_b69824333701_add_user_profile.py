"""Add user profile

Revision ID: b69824333701
Revises: 6a085665295c
Create Date: 2025-02-19 23:40:38.304382

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b69824333701"
down_revision: Union[str, None] = "6a085665295c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade"""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_profile",
        sa.Column("username", sa.String(), nullable=False),
        sa.Column(
            "veggie_identity",
            sa.Enum(
                "NONE",
                "VEGAN",
                "VEGETARIAN",
                name="userprofilemodelveggieidentity",
            ),
            nullable=False,
        ),
        sa.Column("prefer", sa.PickleType(), nullable=False),
        sa.Column("dislike", sa.PickleType(), nullable=False),
        sa.Column("embedding", sa.PickleType(), nullable=False),
        sa.PrimaryKeyConstraint("username"),
        schema="public",
    )
    op.add_column(
        "recipe",
        sa.Column(
            "veggie_identity",
            sa.Enum(
                "NONE",
                "VEGAN",
                "VEGETARIAN",
                name="userprofilemodelveggieidentity",
            ),
            nullable=False,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade"""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("recipe", "veggie_identity")
    op.drop_table("user_profile", schema="public")
    # ### end Alembic commands ###
