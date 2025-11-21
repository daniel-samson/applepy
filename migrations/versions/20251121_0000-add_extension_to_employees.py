"""add extension field to employees

Revision ID: 5a2b3c4d5e6f
Revises: 4177a5ef2d93
Create Date: 2025-11-21 00:00:00.000000+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5a2b3c4d5e6f"
down_revision: Union[str, Sequence[str], None] = "4177a5ef2d93"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "employees",
        sa.Column("extension", sa.String(10), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("employees", "extension")
