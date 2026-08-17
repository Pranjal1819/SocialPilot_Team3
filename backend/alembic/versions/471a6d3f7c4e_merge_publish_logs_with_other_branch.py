"""merge publish_logs with other branch

Revision ID: 471a6d3f7c4e
Revises: 9dfdc1a12ba9, f7c3e9b21a04
Create Date: 2026-08-14 14:51:31.011664

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '471a6d3f7c4e'
down_revision: Union[str, Sequence[str], None] = ('9dfdc1a12ba9', 'f7c3e9b21a04')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
