"""Initial models

Revision ID: 8f773f31cf09
Revises:
Create Date: 2024-12-26 12:21:32.162204

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8f773f31cf09"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("full_name", sa.String(length=100), nullable=False),
        sa.Column("position", sa.String(length=100), nullable=False),
        sa.Column("com_name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("full_name"),
    )
    op.create_table(
        "ecp",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("employees_id", sa.Integer(), nullable=False),
        sa.Column("type_ecp", sa.String(), nullable=False),
        sa.Column("status_ecp", sa.String(), nullable=False),
        sa.Column("install_location", sa.String(), nullable=False),
        sa.Column("storage_location", sa.String(), nullable=False),
        sa.Column("sbis", sa.String(), nullable=False),
        sa.Column("chz", sa.String(), nullable=False),
        sa.Column("diadok", sa.String(), nullable=False),
        sa.Column("fns", sa.String(), nullable=False),
        sa.Column("report", sa.String(), nullable=False),
        sa.Column("fed_resours", sa.String(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("finish_date", sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(
            ["employees_id"],
            ["employees.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "kriptos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("employees_id", sa.Integer(), nullable=False),
        sa.Column("install_location", sa.String(), nullable=False),
        sa.Column("licens_type", sa.String(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("finish_date", sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(
            ["employees_id"],
            ["employees.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )



def downgrade() -> None:
    op.drop_table("kriptos")
    op.drop_table("ecp")
    op.drop_table("employees")
