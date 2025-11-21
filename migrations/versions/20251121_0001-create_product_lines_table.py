"""create product_lines table

Revision ID: 6b3c4d5e6f7a
Revises: 5a2b3c4d5e6f
Create Date: 2025-11-21 00:01:00.000000+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6b3c4d5e6f7a"
down_revision: Union[str, Sequence[str], None] = "5a2b3c4d5e6f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "product_lines",
        sa.Column("product_line", sa.String(50), primary_key=True),
        sa.Column("text_description", sa.String(4000), nullable=True),
        sa.Column("html_description", sa.Text, nullable=True),
        sa.Column("image", sa.LargeBinary, nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("product_lines")
