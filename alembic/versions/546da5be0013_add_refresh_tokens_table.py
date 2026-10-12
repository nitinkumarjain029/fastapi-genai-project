"""add refresh tokens table

Revision ID: 546da5be0013
Revises: 569ebb386fed
Create Date: 2026-10-05 00:26:41.832817
"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "546da5be0013"
down_revision: Union[str, Sequence[str], None] = "569ebb386fed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
