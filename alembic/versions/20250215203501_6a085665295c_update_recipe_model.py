"""Update recipe model

Revision ID: 6a085665295c
Revises: e9ea3f128824
Create Date: 2025-02-15 20:35:01.584915

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6a085665295c"
down_revision: Union[str, None] = "e9ea3f128824"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade"""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("index_file")
    op.add_column("recipe", sa.Column("title", sa.String(), nullable=False))
    op.add_column(
        "recipe", sa.Column("description", sa.String(), nullable=False)
    )
    op.add_column(
        "recipe", sa.Column("directions", sa.PickleType(), nullable=False)
    )
    op.add_column("recipe", sa.Column("tips", sa.PickleType(), nullable=False))
    op.add_column(
        "recipe", sa.Column("utensils", sa.PickleType(), nullable=False)
    )
    op.add_column(
        "recipe", sa.Column("nutrition", sa.PickleType(), nullable=False)
    )
    op.drop_column("recipe", "instructions")
    op.drop_column("recipe", "raw")
    op.drop_column("recipe", "name")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade"""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "recipe",
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "recipe",
        sa.Column("raw", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "recipe",
        sa.Column(
            "instructions",
            postgresql.BYTEA(),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_column("recipe", "nutrition")
    op.drop_column("recipe", "utensils")
    op.drop_column("recipe", "tips")
    op.drop_column("recipe", "directions")
    op.drop_column("recipe", "description")
    op.drop_column("recipe", "title")
    op.create_table(
        "index_file",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("count", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("model", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("path", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="index_file_pkey"),
    )
    # ### end Alembic commands ###
