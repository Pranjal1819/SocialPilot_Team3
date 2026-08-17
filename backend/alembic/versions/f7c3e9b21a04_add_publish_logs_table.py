"""add publish_logs table

Revision ID: f7c3e9b21a04
Revises: a4f2c9d81e33
Create Date: 2026-08-14

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "f7c3e9b21a04"
down_revision = "a4f2c9d81e33"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "publish_logs",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column(
            "scheduled_post_id",
            sa.Integer(),
            sa.ForeignKey("scheduled_posts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "social_account_id",
            sa.Integer(),
            sa.ForeignKey("social_accounts.id"),
            nullable=True,
        ),
        sa.Column("platform", sa.String(length=50), nullable=False),
        sa.Column("attempt_number", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("response_data", sa.Text(), nullable=True),
        sa.Column("platform_post_id", sa.String(length=500), nullable=True),
        sa.Column("published_url", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_index("idx_publish_log_post", "publish_logs", ["scheduled_post_id"])
    op.create_index("idx_publish_log_status", "publish_logs", ["status"])


def downgrade():
    op.drop_index("idx_publish_log_status", table_name="publish_logs")
    op.drop_index("idx_publish_log_post", table_name="publish_logs")
    op.drop_table("publish_logs")
