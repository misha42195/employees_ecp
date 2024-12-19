"""add employees model

Revision ID: 5b1287175e57
Revises:
Create Date: 2024-12-12 15:00:39.364394

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b1287175e57'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('employees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('position', sa.String(), nullable=False),
    sa.Column('com_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('full_name')
    )


def downgrade() -> None:
    op.drop_table('employees')
