"""Add relationships to EmployeesORM

Revision ID: 2d02226e04ef
Revises: e72a4169ea20
Create Date: 2024-12-23 09:54:10.495527

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2d02226e04ef"
down_revision: Union[str, None] = "e72a4169ea20"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
