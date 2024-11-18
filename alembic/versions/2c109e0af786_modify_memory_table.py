"""modify memory table

Revision ID: 2c109e0af786
Revises: 6413379cb6e7
Create Date: 2024-11-12 11:24:15.669382

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c109e0af786'
down_revision: Union[str, None] = '6413379cb6e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('memory', sa.Column('index', sa.BigInteger(), nullable=True))
    op.add_column('memory', sa.Column('special', sa.TEXT(), nullable=True))
    op.drop_column('memory', 'song_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('memory', sa.Column('song_id', sa.BIGINT(), autoincrement=False, nullable=True))
    op.drop_column('memory', 'special')
    op.drop_column('memory', 'index')
    # ### end Alembic commands ###
