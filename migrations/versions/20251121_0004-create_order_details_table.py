"""create order_details table

Revision ID: 9e6f7a8b9c0d
Revises: 8d5e6f7a8b9c
Create Date: 2025-11-21 00:04:00.000000+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9e6f7a8b9c0d"
down_revision: Union[str, Sequence[str], None] = "8d5e6f7a8b9c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "order_details",
        sa.Column("order_number", sa.Integer, nullable=False),
        sa.Column("product_code", sa.String(15), nullable=False),
        sa.Column("quantity_ordered", sa.Integer, nullable=False),
        sa.Column("price_each", sa.Numeric(10, 2), nullable=False),
        sa.Column("order_line_number", sa.SmallInteger, nullable=False),
        sa.PrimaryKeyConstraint("order_number", "product_code"),
        sa.ForeignKeyConstraint(
            ["order_number"],
            ["orders.order_number"],
            name="fk_order_details_order_number",
        ),
        sa.ForeignKeyConstraint(
            ["product_code"],
            ["products.product_code"],
            name="fk_order_details_product_code",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("order_details")
