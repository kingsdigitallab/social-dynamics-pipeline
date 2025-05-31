"""update FormB102r with fields for corrected data

Revision ID: a666e0cf3bc8
Revises: 49b8b12b7fa5
Create Date: 2025-05-30 20:18:18.277309

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore[attr-defined]

# revision identifiers, used by Alembic.
revision: str = "a666e0cf3bc8"
down_revision: Union[str, None] = "49b8b12b7fa5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("formb102r", sa.Column("form_type", sa.String(), nullable=True))
    op.add_column("formb102r", sa.Column("dob_date", sa.Date(), nullable=True))
    op.add_column(
        "formb102r", sa.Column("date_of_enlistment_date", sa.Date(), nullable=True)
    )
    op.add_column(
        "formb102r", sa.Column("regiment_or_corp", sa.String(), nullable=True)
    )
    op.add_column("formb102r", sa.Column("rank", sa.String(), nullable=True))
    op.add_column("formb102r", sa.Column("engagement", sa.String(), nullable=True))
    op.add_column("formb102r", sa.Column("nationality", sa.String(), nullable=True))
    op.add_column("formb102r", sa.Column("religion", sa.String(), nullable=True))
    op.add_column("formb102r", sa.Column("industry_group", sa.String(), nullable=True))
    op.add_column("formb102r", sa.Column("occupation", sa.String(), nullable=True))
    op.add_column("formb102r", sa.Column("service_trade", sa.String(), nullable=True))
    op.add_column("formb102r", sa.Column("marital_status", sa.String(), nullable=True))
    op.add_column(
        "formb102r", sa.Column("medical_category", sa.String(), nullable=True)
    )
    op.add_column("formb102r", sa.Column("hometown", sa.String(), nullable=True))

    # SQLite does not support ALTER COLUMN
    # op.alter_column(
    #     "formb102r",
    #     "army_number",
    #     existing_type=sa.INTEGER(),
    #     type_=sa.String(),
    #     existing_nullable=True,
    # )
    # op.alter_column(
    #     "formb102r",
    #     "dob",
    #     existing_type=sa.DATE(),
    #     type_=sa.String(),
    #     existing_nullable=True,
    # )
    # op.alter_column(
    #     "formb102r",
    #     "date_of_enlistment",
    #     existing_type=sa.DATE(),
    #     type_=sa.String(),
    #     existing_nullable=True,
    # )
    # op.alter_column(
    #     "individual",
    #     "army_number",
    #     existing_type=sa.INTEGER(),
    #     type_=sa.String(),
    #     existing_nullable=True,
    # )
    # op.alter_column("industry", "desc", existing_type=sa.VARCHAR(), nullable=True)
    # op.alter_column("maritalstatus", "desc", existing_type=sa.VARCHAR(),
    # nullable=True)
    # op.alter_column(
    #     "medicalcategory", "desc", existing_type=sa.VARCHAR(), nullable=True
    # )
    # op.alter_column("nationality", "desc", existing_type=sa.VARCHAR(), nullable=True)
    # op.alter_column("occupation", "desc", existing_type=sa.VARCHAR(), nullable=True)
    # op.alter_column("rank", "desc", existing_type=sa.VARCHAR(), nullable=True)
    # op.alter_column("regiment", "desc", existing_type=sa.VARCHAR(), nullable=True)
    # op.alter_column("religion", "desc", existing_type=sa.VARCHAR(), nullable=True)
    # op.alter_column("servicetrade", "desc", existing_type=sa.VARCHAR(), nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    # SQLite does not support DROP COLUMN or ALTER COLUMN,
    # so this downgrade step is not reversible using SQLite.
    raise RuntimeError(
        "Downgrade not supported on SQLite. "
        "This migration cannot be reversed automatically."
    )
    # op.alter_column("servicetrade", "desc", existing_type=sa.VARCHAR(),
    # nullable=False)
    # op.alter_column("religion", "desc", existing_type=sa.VARCHAR(), nullable=False)
    # op.alter_column("regiment", "desc", existing_type=sa.VARCHAR(), nullable=False)
    # op.alter_column("rank", "desc", existing_type=sa.VARCHAR(), nullable=False)
    # op.alter_column("occupation", "desc", existing_type=sa.VARCHAR(), nullable=False)
    # op.alter_column("nationality", "desc", existing_type=sa.VARCHAR(), nullable=False)
    # op.alter_column(
    #     "medicalcategory", "desc", existing_type=sa.VARCHAR(), nullable=False
    # )
    # op.alter_column("maritalstatus", "desc", existing_type=sa.VARCHAR(),
    # nullable=False)
    # op.alter_column("industry", "desc", existing_type=sa.VARCHAR(), nullable=False)
    # op.alter_column(
    #     "individual",
    #     "army_number",
    #     existing_type=sa.String(),
    #     type_=sa.INTEGER(),
    #     existing_nullable=True,
    # )
    # op.alter_column(
    #     "formb102r",
    #     "date_of_enlistment",
    #     existing_type=sa.String(),
    #     type_=sa.DATE(),
    #     existing_nullable=True,
    # )
    # op.alter_column(
    #     "formb102r",
    #     "dob",
    #     existing_type=sa.String(),
    #     type_=sa.DATE(),
    #     existing_nullable=True,
    # )
    # op.alter_column(
    #     "formb102r",
    #     "army_number",
    #     existing_type=sa.String(),
    #     type_=sa.INTEGER(),
    #     existing_nullable=True,
    # )
    # op.drop_column("formb102r", "hometown")
    # op.drop_column("formb102r", "medical_category")
    # op.drop_column("formb102r", "marital_status")
    # op.drop_column("formb102r", "service_trade")
    # op.drop_column("formb102r", "occupation")
    # op.drop_column("formb102r", "industry_group")
    # op.drop_column("formb102r", "religion")
    # op.drop_column("formb102r", "nationality")
    # op.drop_column("formb102r", "engagement")
    # op.drop_column("formb102r", "rank")
    # op.drop_column("formb102r", "regiment_or_corp")
    # op.drop_column("formb102r", "date_of_enlistment_date")
    # op.drop_column("formb102r", "dob_date")
    # op.drop_column("formb102r", "form_type")
