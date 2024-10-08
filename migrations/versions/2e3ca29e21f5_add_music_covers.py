"""add music covers

Revision ID: 2e3ca29e21f5
Revises: be82eb3f8d56
Create Date: 2024-10-05 21:01:53.624218

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e3ca29e21f5'
down_revision: Union[str, None] = 'be82eb3f8d56'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('music', sa.Column('cover_url', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'music', ['cover_url'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'music', type_='unique')
    op.drop_column('music', 'cover_url')
    # ### end Alembic commands ###
