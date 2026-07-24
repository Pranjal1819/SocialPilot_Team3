"""add campaign relation to scheduled posts

Revision ID: 9e5e628497e2
Revises: 1b788d20e7f4
Create Date: 2026-07-24 13:16:02.249744

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "9e5e628497e2"
down_revision: Union[str, Sequence[str], None] = "1b788d20e7f4"
branch_labels = None
depends_on = None


def upgrade() -> None:

    # Add campaign connection to scheduled posts
    op.add_column(
        "scheduled_posts", sa.Column("campaign_id", sa.Integer(), nullable=True)
    )

    op.create_foreign_key(
        "fk_scheduled_posts_campaign",
        "scheduled_posts",
        "campaigns",
        ["campaign_id"],
        ["id"],
    )


def downgrade() -> None:

    op.drop_constraint(
        "fk_scheduled_posts_campaign", "scheduled_posts", type_="foreignkey"
    )

    op.drop_column("scheduled_posts", "campaign_id")
