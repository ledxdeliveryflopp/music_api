"""add nullable music duration

Revision ID: b4563432005b
Revises: 3e5ab0deeec0
Create Date: 2024-10-01 15:22:16.853602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4563432005b'
down_revision: Union[str, None] = '3e5ab0deeec0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('music', 'duration',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('music', 'duration',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
