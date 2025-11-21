"""create products table

Revision ID: 7c4d5e6f7a8b
Revises: 6b3c4d5e6f7a
Create Date: 2025-11-21 00:02:00.000000+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7c4d5e6f7a8b"
down_revision: Union[str, Sequence[str], None] = "6b3c4d5e6f7a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "products",
        sa.Column("product_code", sa.String(15), primary_key=True),
        sa.Column("product_name", sa.String(70), nullable=False),
        sa.Column("product_line", sa.String(50), nullable=False),
        sa.Column("product_scale", sa.String(10), nullable=False),
        sa.Column("product_vendor", sa.String(50), nullable=False),
        sa.Column("product_description", sa.Text, nullable=False),
        sa.Column("quantity_in_stock", sa.SmallInteger, nullable=False),
        sa.Column("buy_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("msrp", sa.Numeric(10, 2), nullable=False),
        sa.ForeignKeyConstraint(
            ["product_line"],
            ["product_lines.product_line"],
            name="fk_products_product_line",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("products")
