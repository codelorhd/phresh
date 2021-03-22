"""create_main_tables

Revision ID: 48976538dfd0
Revises: 
Create Date: 2021-03-20 09:03:18.701497

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic
revision = "48976538dfd0"
down_revision = None
branch_labels = None
depends_on = None


def create_cleanings_table() -> None:
    op.create_table(
        "cleanings",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column(
            "cleaning_type", sa.Text, nullable=False, server_default="spot_clean"
        ),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
    )


def upgrade() -> None:
    create_cleanings_table()


def downgrade() -> None:
    try:
        op.drop_table("cleanings")
    except UndefinedTableError:
        pass


from asyncpg.exceptions import UndefinedTableError
