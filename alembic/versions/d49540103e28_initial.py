"""initial

Revision ID: d49540103e28
Revises:
Create Date: 2025-05-30 12:19:28.838199

"""

from typing import Sequence, Union

# from alembic import op
# import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d49540103e28"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
