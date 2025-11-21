"""create orders table

Revision ID: 8d5e6f7a8b9c
Revises: 7c4d5e6f7a8b
Create Date: 2025-11-21 00:03:00.000000+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8d5e6f7a8b9c"
down_revision: Union[str, Sequence[str], None] = "7c4d5e6f7a8b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "orders",
        sa.Column("order_number", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("order_date", sa.Date, nullable=False),
        sa.Column("required_date", sa.Date, nullable=False),
        sa.Column("shipped_date", sa.Date, nullable=True),
        sa.Column("status", sa.String(15), nullable=False),
        sa.Column("comments", sa.Text, nullable=True),
        sa.Column("customer_number", sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(
            ["customer_number"],
            ["customers.customer_number"],
            name="fk_orders_customer_number",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("orders")
