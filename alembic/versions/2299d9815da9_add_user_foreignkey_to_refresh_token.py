"""add user ForeignKey to refresh token

Revision ID: 2299d9815da9
Revises: 546da5be0013
Create Date: 2026-10-05 10:40:22.106891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2299d9815da9'
down_revision: Union[str, Sequence[str], None] = '546da5be0013'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("refresh_tokens") as batch_op:
        batch_op.create_foreign_key(
            "fk_refresh_tokens_user_id",
            "users",
            ["user_id"],
            ["id"]
        )


def downgrade() -> None:
    with op.batch_alter_table("refresh_tokens") as batch_op:
        batch_op.drop_constraint(
            "fk_refresh_tokens_user_id",
            type_="foreignkey"
        )
