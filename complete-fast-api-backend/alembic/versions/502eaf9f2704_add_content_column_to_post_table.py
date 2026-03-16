"""add content column to post table

Revision ID: 502eaf9f2704
Revises: 07a7ae2e756f
Create Date: 2026-03-17 01:37:11.396939

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "502eaf9f2704"
down_revision: Union[str, Sequence[str], None] = "07a7ae2e756f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
