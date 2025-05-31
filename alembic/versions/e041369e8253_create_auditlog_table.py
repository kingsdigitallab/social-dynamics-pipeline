"""create AuditLog table

Revision ID: e041369e8253
Revises: a666e0cf3bc8
Create Date: 2025-05-31 15:33:27.676379

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore[attr-defined]

# revision identifiers, used by Alembic.
revision: str = "e041369e8253"
down_revision: Union[str, None] = "a666e0cf3bc8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "auditlog",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("table_name", sa.String(), nullable=False),
        sa.Column("record_id", sa.Integer(), nullable=False),
        sa.Column("field_name", sa.String(), nullable=False),
        sa.Column("field_type", sa.String(), nullable=True),
        sa.Column("old_value", sa.String(), nullable=True),
        sa.Column("new_value", sa.String(), nullable=True),
        sa.Column("change_reason", sa.String(), nullable=True),
        sa.Column("session_id", sa.String(), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_auditlog_record_id"), "auditlog", ["record_id"], unique=False
    )
    op.create_index(
        op.f("ix_auditlog_table_name"), "auditlog", ["table_name"], unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    if bind.dialect.name == "sqlite":
        # SQLite drops indexes automatically with the table
        op.drop_table("auditlog")
    else:
        op.drop_index(op.f("ix_auditlog_table_name"), table_name="auditlog")
        op.drop_index(op.f("ix_auditlog_record_id"), table_name="auditlog")
        op.drop_table("auditlog")
