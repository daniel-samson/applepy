"""create payments table

Revision ID: 0f7a8b9c0d1e
Revises: 9e6f7a8b9c0d
Create Date: 2025-11-21 00:05:00.000000+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0f7a8b9c0d1e"
down_revision: Union[str, Sequence[str], None] = "9e6f7a8b9c0d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "payments",
        sa.Column("customer_number", sa.Integer, nullable=False),
        sa.Column("check_number", sa.String(50), nullable=False),
        sa.Column("payment_date", sa.Date, nullable=False),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
        sa.PrimaryKeyConstraint("customer_number", "check_number"),
        sa.ForeignKeyConstraint(
            ["customer_number"],
            ["customers.customer_number"],
            name="fk_payments_customer_number",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("payments")
