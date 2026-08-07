"""add analytics dashboard tables

Revision ID: a4f2c9d81e33
Revises: 26dbbb2db6d5
Create Date: 2026-08-07 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.

revision: str = "a4f2c9d81e33"
down_revision: Union[str, Sequence[str], None] = "26dbbb2db6d5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # ================================
    # Post Analytics - New Metrics
    # ================================

    op.add_column(
        "post_analytics",
        sa.Column(
            "reach",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "post_analytics",
        sa.Column(
            "impressions",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "post_analytics",
        sa.Column(
            "clicks",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "post_analytics",
        sa.Column(
            "saves",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    # ================================
    # Audience Analytics Table
    # ================================

    op.create_table(
        "audience_analytics",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("social_account_id", sa.Integer(), nullable=True),
        sa.Column("platform", sa.String(length=50), nullable=False),
        sa.Column("total_followers", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("new_followers", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("lost_followers", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("net_growth", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("gender_distribution", sa.JSON(), nullable=True),
        sa.Column("age_distribution", sa.JSON(), nullable=True),
        sa.Column("country", sa.String(length=100), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("languages", sa.JSON(), nullable=True),
        sa.Column("most_active_hours", sa.JSON(), nullable=True),
        sa.Column("most_active_days", sa.JSON(), nullable=True),
        sa.Column("recorded_at", sa.DateTime(), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["social_account_id"], ["social_accounts.id"], ondelete="CASCADE"
        ),
    )

    op.create_index(
        "idx_audience_analytics_user",
        "audience_analytics",
        ["user_id"],
    )

    op.create_index(
        "idx_audience_analytics_platform",
        "audience_analytics",
        ["platform"],
    )

    # ================================
    # Campaign Analytics Snapshots Table
    # ================================

    op.create_table(
        "campaign_analytics_snapshots",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("campaign_id", sa.Integer(), nullable=False),
        sa.Column("total_posts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("reach", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("impressions", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("engagement", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("clicks", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("likes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("roi", sa.Integer(), nullable=True),
        sa.Column(
            "completion_percentage", sa.Integer(), nullable=False, server_default="0"
        ),
        sa.Column("recorded_at", sa.DateTime(), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["campaign_id"], ["campaigns.id"], ondelete="CASCADE"),
    )

    op.create_index(
        "idx_campaign_analytics_campaign",
        "campaign_analytics_snapshots",
        ["campaign_id"],
    )

    # ================================
    # Platform Analytics Table
    # ================================

    op.create_table(
        "platform_analytics",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("platform_name", sa.String(length=50), nullable=False),
        sa.Column("followers", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("reach", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("engagement", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("impressions", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("clicks", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("recorded_at", sa.DateTime(), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )

    op.create_index(
        "idx_platform_analytics_user",
        "platform_analytics",
        ["user_id"],
    )

    op.create_index(
        "idx_platform_analytics_platform",
        "platform_analytics",
        ["platform_name"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index("idx_platform_analytics_platform", table_name="platform_analytics")
    op.drop_index("idx_platform_analytics_user", table_name="platform_analytics")
    op.drop_table("platform_analytics")

    op.drop_index(
        "idx_campaign_analytics_campaign", table_name="campaign_analytics_snapshots"
    )
    op.drop_table("campaign_analytics_snapshots")

    op.drop_index("idx_audience_analytics_platform", table_name="audience_analytics")
    op.drop_index("idx_audience_analytics_user", table_name="audience_analytics")
    op.drop_table("audience_analytics")

    op.drop_column("post_analytics", "saves")
    op.drop_column("post_analytics", "clicks")
    op.drop_column("post_analytics", "impressions")
    op.drop_column("post_analytics", "reach")
