"""add recurring scheduling support

Revision ID: ba85ebad7b7a
Revises: f3fc48680731
Create Date: 2026-07-24 14:33:24.215821

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision: str = "ba85ebad7b7a"
down_revision: Union[str, Sequence[str], None] = "f3fc48680731"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add recurring scheduling support

    op.add_column(
        "scheduled_posts",
        sa.Column("is_recurring", sa.Boolean(), nullable=False, server_default="false"),
    )

    op.add_column(
        "scheduled_posts",
        sa.Column("recurrence_type", sa.String(length=50), nullable=True),
    )

    op.add_column(
        "scheduled_posts",
        sa.Column(
            "recurrence_interval", sa.Integer(), nullable=True, server_default="1"
        ),
    )

    op.add_column(
        "scheduled_posts", sa.Column("next_run_time", sa.DateTime(), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("scheduled_posts", "next_run_time")

    op.drop_column("scheduled_posts", "recurrence_interval")

    op.drop_column("scheduled_posts", "recurrence_type")

    op.drop_column("scheduled_posts", "is_recurring")
