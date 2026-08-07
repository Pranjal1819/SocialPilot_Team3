"""sync updated models

Revision ID: 26dbbb2db6d5
Revises: d1b1284f1d48
Create Date: 2026-08-07 09:55:30.064758

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.

revision: str = "26dbbb2db6d5"
down_revision: Union[str, Sequence[str], None] = "d1b1284f1d48"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # ================================
    # Post Analytics Updates
    # ================================

    op.alter_column(
        "post_analytics",
        "post_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )

    op.drop_constraint(
        op.f("post_analytics_user_id_fkey"),
        "post_analytics",
        type_="foreignkey",
    )

    op.drop_constraint(
        op.f("post_analytics_post_id_fkey"),
        "post_analytics",
        type_="foreignkey",
    )

    op.drop_constraint(
        op.f("post_analytics_campaign_id_fkey"),
        "post_analytics",
        type_="foreignkey",
    )

    op.create_foreign_key(
        None,
        "post_analytics",
        "scheduled_posts",
        ["post_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.create_foreign_key(
        None,
        "post_analytics",
        "campaigns",
        ["campaign_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.create_foreign_key(
        None,
        "post_analytics",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # ================================
    # Scheduled Posts Updates
    # ================================

    op.add_column(
        "scheduled_posts",
        sa.Column("hashtags", sa.Text(), nullable=True),
    )

    op.add_column(
        "scheduled_posts",
        sa.Column("mentions", sa.Text(), nullable=True),
    )

    op.add_column(
        "scheduled_posts",
        sa.Column("first_comment", sa.Text(), nullable=True),
    )

    op.add_column(
        "scheduled_posts",
        sa.Column("recurrence_end_date", sa.DateTime(), nullable=True),
    )

    op.add_column(
        "scheduled_posts",
        sa.Column(
            "approval_status",
            sa.String(length=50),
            nullable=False,
            server_default="pending",
        ),
    )

    op.add_column(
        "scheduled_posts",
        sa.Column("approved_by", sa.Integer(), nullable=True),
    )

    op.add_column(
        "scheduled_posts",
        sa.Column("approved_at", sa.DateTime(), nullable=True),
    )

    op.add_column(
        "scheduled_posts",
        sa.Column(
            "is_deleted",
            sa.Boolean(),
            nullable=False,
            server_default="false",
        ),
    )

    op.create_foreign_key(
        None,
        "scheduled_posts",
        "users",
        ["approved_by"],
        ["id"],
    )

    op.drop_column(
        "scheduled_posts",
        "media_url",
    )

    # ================================
    # Social Account Updates
    # ================================

    op.add_column(
        "social_accounts",
        sa.Column(
            "profile_url",
            sa.String(length=500),
            nullable=True,
        ),
    )

    op.add_column(
        "social_accounts",
        sa.Column(
            "profile_picture",
            sa.String(length=500),
            nullable=True,
        ),
    )

    op.add_column(
        "social_accounts",
        sa.Column(
            "followers_count",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "social_accounts",
        sa.Column(
            "following_count",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "social_accounts",
        sa.Column(
            "total_posts",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "social_accounts",
        sa.Column(
            "last_synced",
            sa.DateTime(),
            nullable=True,
        ),
    )

    # ================================
    # User Updates
    # ================================

    op.add_column(
        "users",
        sa.Column(
            "phone",
            sa.String(length=20),
            nullable=True,
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "organization",
            sa.String(length=200),
            nullable=True,
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "designation",
            sa.String(length=100),
            nullable=True,
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "bio",
            sa.String(length=500),
            nullable=True,
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "is_verified",
            sa.Boolean(),
            nullable=False,
            server_default="false",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("users", "is_verified")
    op.drop_column("users", "bio")
    op.drop_column("users", "designation")
    op.drop_column("users", "organization")
    op.drop_column("users", "phone")

    op.drop_column("social_accounts", "last_synced")
    op.drop_column("social_accounts", "total_posts")
    op.drop_column("social_accounts", "following_count")
    op.drop_column("social_accounts", "followers_count")
    op.drop_column("social_accounts", "profile_picture")
    op.drop_column("social_accounts", "profile_url")

    op.add_column(
        "scheduled_posts",
        sa.Column(
            "media_url",
            sa.VARCHAR(length=500),
            nullable=True,
        ),
    )

    op.drop_constraint(
        None,
        "scheduled_posts",
        type_="foreignkey",
    )

    op.drop_column("scheduled_posts", "is_deleted")
    op.drop_column("scheduled_posts", "approved_at")
    op.drop_column("scheduled_posts", "approved_by")
    op.drop_column("scheduled_posts", "approval_status")
    op.drop_column("scheduled_posts", "recurrence_end_date")
    op.drop_column("scheduled_posts", "first_comment")
    op.drop_column("scheduled_posts", "mentions")
    op.drop_column("scheduled_posts", "hashtags")

    op.drop_constraint(
        None,
        "post_analytics",
        type_="foreignkey",
    )

    op.drop_constraint(
        None,
        "post_analytics",
        type_="foreignkey",
    )

    op.drop_constraint(
        None,
        "post_analytics",
        type_="foreignkey",
    )

    op.create_foreign_key(
        op.f("post_analytics_campaign_id_fkey"),
        "post_analytics",
        "campaigns",
        ["campaign_id"],
        ["id"],
    )

    op.create_foreign_key(
        op.f("post_analytics_post_id_fkey"),
        "post_analytics",
        "scheduled_posts",
        ["post_id"],
        ["id"],
    )

    op.create_foreign_key(
        op.f("post_analytics_user_id_fkey"),
        "post_analytics",
        "users",
        ["user_id"],
        ["id"],
    )

    op.alter_column(
        "post_analytics",
        "post_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
