"""lookup tables must have label and desc

Revision ID: 49b8b12b7fa5
Revises: 647c9e4f551b
Create Date: 2025-05-30 17:06:42.692540

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore[attr-defined]

# revision identifiers, used by Alembic.
revision: str = "49b8b12b7fa5"
down_revision: Union[str, None] = "647c9e4f551b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # SQLite does not support ALTER TABLE
    op.add_column("engagement", sa.Column("label", sa.String(), nullable=False))
    op.add_column("engagement", sa.Column("desc", sa.String(), nullable=True))
    op.drop_column("engagement", "type")
    op.drop_column("engagement", "expanded_form")
    # op.alter_column('formb102r', 'army_number',
    #            existing_type=sa.INTEGER(),
    #            type_=sa.String(),
    #            existing_nullable=True)
    # op.alter_column('individual', 'army_number',
    #            existing_type=sa.INTEGER(),
    #            type_=sa.String(),
    #            existing_nullable=True)
    op.add_column("industry", sa.Column("label", sa.String(), nullable=False))
    # op.alter_column('industry', 'desc',
    #            existing_type=sa.VARCHAR(),
    #            nullable=True)
    op.add_column("maritalstatus", sa.Column("label", sa.String(), nullable=False))
    # op.alter_column('maritalstatus', 'desc',
    #            existing_type=sa.VARCHAR(),
    #            nullable=True)
    op.add_column("medicalcategory", sa.Column("label", sa.String(), nullable=False))
    # op.alter_column('medicalcategory', 'desc',
    #            existing_type=sa.VARCHAR(),
    #            nullable=True)
    op.add_column("nationality", sa.Column("label", sa.String(), nullable=False))
    # op.alter_column('nationality', 'desc',
    #            existing_type=sa.VARCHAR(),
    #            nullable=True)
    op.add_column("occupation", sa.Column("label", sa.String(), nullable=False))
    # op.alter_column('occupation', 'desc',
    #            existing_type=sa.VARCHAR(),
    #            nullable=True)
    op.add_column("place", sa.Column("label", sa.String(), nullable=False))
    op.add_column("place", sa.Column("desc", sa.String(), nullable=True))
    op.drop_column("place", "toponym")
    op.add_column("rank", sa.Column("label", sa.String(), nullable=False))
    # op.alter_column('rank', 'desc',
    #            existing_type=sa.VARCHAR(),
    #            nullable=True)
    op.add_column("regiment", sa.Column("label", sa.String(), nullable=False))
    # op.alter_column('regiment', 'desc',
    #            existing_type=sa.VARCHAR(),
    #            nullable=True)
    op.add_column("religion", sa.Column("label", sa.String(), nullable=False))
    # op.alter_column('religion', 'desc',
    #            existing_type=sa.VARCHAR(),
    #            nullable=True)
    op.add_column("servicetrade", sa.Column("label", sa.String(), nullable=False))
    # op.alter_column('servicetrade', 'desc',
    #            existing_type=sa.VARCHAR(),
    #            nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    # SQLite does not support ALTER TABLE
    # op.alter_column('servicetrade', 'desc',
    #            existing_type=sa.VARCHAR(),
    #            nullable=False)
    op.drop_column("servicetrade", "label")
    # op.alter_column('religion', 'desc',
    #            existing_type=sa.VARCHAR(),
    #            nullable=False)
    op.drop_column("religion", "label")
    # op.alter_column('regiment', 'desc',
    #            existing_type=sa.VARCHAR(),
    #            nullable=False)
    op.drop_column("regiment", "label")
    # op.alter_column('rank', 'desc',
    #            existing_type=sa.VARCHAR(),
    #            nullable=False)
    op.drop_column("rank", "label")
    op.add_column("place", sa.Column("toponym", sa.VARCHAR(), nullable=False))
    op.drop_column("place", "desc")
    op.drop_column("place", "label")
    # op.alter_column('occupation', 'desc',
    #            existing_type=sa.VARCHAR(),
    #            nullable=False)
    op.drop_column("occupation", "label")
    # op.alter_column('nationality', 'desc',
    #            existing_type=sa.VARCHAR(),
    #            nullable=False)
    op.drop_column("nationality", "label")
    # op.alter_column('medicalcategory', 'desc',
    #            existing_type=sa.VARCHAR(),
    #            nullable=False)
    op.drop_column("medicalcategory", "label")
    # op.alter_column('maritalstatus', 'desc',
    #            existing_type=sa.VARCHAR(),
    #            nullable=False)
    op.drop_column("maritalstatus", "label")
    # op.alter_column('industry', 'desc',
    #            existing_type=sa.VARCHAR(),
    #            nullable=False)
    op.drop_column("industry", "label")
    # op.alter_column('individual', 'army_number',
    #            existing_type=sa.String(),
    #            type_=sa.INTEGER(),
    #            existing_nullable=True)
    # op.alter_column('formb102r', 'army_number',
    #            existing_type=sa.String(),
    #            type_=sa.INTEGER(),
    #            existing_nullable=True)
    op.add_column("engagement", sa.Column("expanded_form", sa.VARCHAR(), nullable=True))
    op.add_column("engagement", sa.Column("type", sa.VARCHAR(), nullable=False))
    op.drop_column("engagement", "desc")
    op.drop_column("engagement", "label")
