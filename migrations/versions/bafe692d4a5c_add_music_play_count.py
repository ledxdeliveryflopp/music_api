"""add music play count

Revision ID: bafe692d4a5c
Revises: 7ea4909fc53d
Create Date: 2024-10-07 17:44:38.849878

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bafe692d4a5c'
down_revision: Union[str, None] = '7ea4909fc53d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('music', sa.Column('play_numbers', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('music', 'play_numbers')
    # ### end Alembic commands ###
