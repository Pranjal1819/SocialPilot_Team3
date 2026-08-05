"""add social account relation and linkedin tracking

Revision ID: 37006afd9c52
Revises: 030caa7827df
Create Date: 2026-07-30 13:28:01.654068

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "37006afd9c52"
down_revision: Union[str, Sequence[str], None] = "030caa7827df"
branch_labels = None
depends_on = None


def upgrade() -> None:

    # Add social account reference
    op.add_column(
        "scheduled_posts", sa.Column("social_account_id", sa.Integer(), nullable=True)
    )

    # Store LinkedIn returned post ID
    # Example:
    # urn:li:share:7488501498956591105

    op.add_column(
        "scheduled_posts",
        sa.Column("platform_post_id", sa.String(length=500), nullable=True),
    )

    # Store public LinkedIn URL if generated

    op.add_column(
        "scheduled_posts",
        sa.Column("published_url", sa.String(length=500), nullable=True),
    )

    op.create_foreign_key(
        "fk_scheduled_posts_social_account",
        "scheduled_posts",
        "social_accounts",
        ["social_account_id"],
        ["id"],
    )


def downgrade() -> None:

    op.drop_constraint(
        "fk_scheduled_posts_social_account", "scheduled_posts", type_="foreignkey"
    )

    op.drop_column("scheduled_posts", "published_url")

    op.drop_column("scheduled_posts", "platform_post_id")

    op.drop_column("scheduled_posts", "social_account_id")
