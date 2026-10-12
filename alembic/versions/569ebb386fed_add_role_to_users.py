"""add role to users

Revision ID: 569ebb386fed
Revises: 0732ac9b2cbc
Create Date: 2026-10-03 09:46:17.820824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '569ebb386fed'
down_revision: Union[str, Sequence[str], None] = '0732ac9b2cbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute(
        "UPDATE users SET role = 'user' WHERE role IS NULL"
    )

    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column(
            'role',
            existing_type=sa.String(),
            nullable=False
        )


def downgrade() -> None:
    op.drop_column('users', 'role')
