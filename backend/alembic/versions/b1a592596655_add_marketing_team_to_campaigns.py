"""add marketing team to campaigns

Revision ID: b1a592596655
Revises: 70cde057359e
Create Date: 2026-07-29 16:06:01.630289

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "b1a592596655"
down_revision: Union[str, Sequence[str], None] = "70cde057359e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # Add column temporarily nullable
    op.add_column(
        "campaigns", sa.Column("marketing_team_id", sa.Integer(), nullable=True)
    )

    # Create relationship with users table
    op.create_foreign_key(
        "fk_campaigns_marketing_team",
        "campaigns",
        "users",
        ["marketing_team_id"],
        ["id"],
    )


def downgrade() -> None:

    op.drop_constraint("fk_campaigns_marketing_team", "campaigns", type_="foreignkey")

    op.drop_column("campaigns", "marketing_team_id")
