"""create posts table

Revision ID: 07a7ae2e756f
Revises:
Create Date: 2026-03-17 01:27:32.357244

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "07a7ae2e756f"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "posts",
        sa.Column("id", sa.INTEGER, nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts")
