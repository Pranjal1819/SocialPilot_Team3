"""add scheduled post extra fields

Revision ID: f3fc48680731
Revises: 9e5e628497e2
Create Date: 2026-07-24 13:19:26.942741

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "f3fc48680731"
down_revision: Union[str, Sequence[str], None] = "9e5e628497e2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add content type
    op.add_column(
        "scheduled_posts",
        sa.Column(
            "content_type", sa.String(length=50), nullable=False, server_default="text"
        ),
    )

    # Add timezone support
    op.add_column(
        "scheduled_posts",
        sa.Column(
            "timezone", sa.String(length=50), nullable=False, server_default="UTC"
        ),
    )

    # Add retry tracking
    op.add_column(
        "scheduled_posts",
        sa.Column("retry_count", sa.Integer(), nullable=False, server_default="0"),
    )

    # Add updated timestamp
    op.add_column(
        "scheduled_posts", sa.Column("updated_at", sa.DateTime(), nullable=True)
    )

    # Allow drafts without scheduled time
    op.alter_column(
        "scheduled_posts",
        "scheduled_time",
        existing_type=postgresql.TIMESTAMP(),
        nullable=True,
    )

    # Status should always exist
    op.alter_column(
        "scheduled_posts", "status", existing_type=sa.VARCHAR(length=50), nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        "scheduled_posts", "status", existing_type=sa.VARCHAR(length=50), nullable=True
    )

    op.alter_column(
        "scheduled_posts",
        "scheduled_time",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
    )

    op.drop_column("scheduled_posts", "updated_at")

    op.drop_column("scheduled_posts", "retry_count")

    op.drop_column("scheduled_posts", "timezone")

    op.drop_column("scheduled_posts", "content_type")
