"""army_number must be string not int

Revision ID: 647c9e4f551b
Revises: d49540103e28
Create Date: 2025-05-30 16:38:03.250278

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "647c9e4f551b"
down_revision: Union[str, None] = "d49540103e28"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # SQLite does not support ALTER TABLE
    # op.alter_column(
    #     "individual",
    #     "army_number",
    #     existing_type=sa.INTEGER(),
    #     type_=sa.String(),
    #     existing_nullable=True,
    # )


def downgrade() -> None:
    """Downgrade schema."""
    # SQLite does not support ALTER TABLE
    # op.alter_column(
    #     "individual",
    #     "army_number",
    #     existing_type=sa.String(),
    #     type_=sa.INTEGER(),
    #     existing_nullable=True,
    # )
