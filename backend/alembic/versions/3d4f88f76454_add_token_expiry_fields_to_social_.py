"""add token expiry fields to social accounts

Revision ID: 3d4f88f76454
Revises: ba85ebad7b7a
Create Date: 2026-07-24 14:49:19.733707

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision: str = "3d4f88f76454"
down_revision: Union[str, Sequence[str], None] = "ba85ebad7b7a"
branch_labels = None
depends_on = None


def upgrade() -> None:

    # Add token expiry support
    op.add_column(
        "social_accounts", sa.Column("token_expires_at", sa.DateTime(), nullable=True)
    )

    # Enable token refresh checking
    op.add_column(
        "social_accounts",
        sa.Column("is_active", sa.Boolean(), nullable=True, server_default=sa.true()),
    )


def downgrade() -> None:

    op.drop_column("social_accounts", "is_active")

    op.drop_column("social_accounts", "token_expires_at")
