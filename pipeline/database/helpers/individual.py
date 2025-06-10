from sqlmodel import Session, select

from pipeline.database.helpers.audit_log import log_change
from pipeline.database.models import Individual
from pipeline.database.validators import validate_date


def get_individuals(session: Session) -> list[Individual]:
    """Retrieve a list of all individuals sorted by the numeric part of pdf_id"""
    statement = select(Individual)
    individuals = session.exec(statement).all()
    # Sort by numeric part of PDF ID - expected form is "APV<int>"
    return sorted(
        individuals,
        key=lambda ind: (
            int(ind.pdf_id.removeprefix("APV"))
            if ind.pdf_id and ind.pdf_id.startswith("APV")
            else 0
        ),
    )


def get_individual(session: Session, individual_id: int) -> Individual | None:
    """Retrieve one Individual by id"""
    form = session.get(Individual, individual_id)
    return form


def save_individual(session: Session, individual: Individual) -> None:
    """Persist changes to an Individual"""
    session.merge(individual)
    session.commit()


def save_individual_with_log(
    session: Session,
    *,
    updated_individual: Individual,
    original_individual: Individual,
    change_reason: str | None = None,
    session_id: str | None = None,
):
    """Persist changes to an Individual, logging any changes in AuditLog."""
    for field in Individual.model_fields.keys():

        # Skip "id" field because we won't be updating the PK
        if field == "id":
            continue

        old_value = getattr(original_individual, field)
        new_value = getattr(updated_individual, field)

        assert (
            updated_individual.id is not None
        ), "Individual must have an ID to be saved"

        updated_individual.dob = validate_date(updated_individual.dob)

        if old_value != new_value:
            log_change(
                session=session,
                model_class=Individual,
                record_id=updated_individual.id,
                field_name=str(field),
                old_label=str(old_value or ""),
                new_label=str(new_value or ""),
                change_reason=str(change_reason or ""),
                session_id=str(session_id or ""),
            )

    session.merge(updated_individual)
    session.commit()
