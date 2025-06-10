from sqlmodel import Session, select

from pipeline.database.helpers.audit_log import log_change
from pipeline.database.models import FormB102r, Individual
from pipeline.database.validators import validate_date


def get_forms(session: Session) -> list[FormB102r]:
    """Retrieve a list of all B102r forms"""
    statement = select(FormB102r)
    forms = session.exec(statement).all()
    return sorted(
        forms,
        key=lambda fm: fm.lastname or "",
    )


def get_form(session: Session, form_id: int) -> FormB102r | None:
    """Retrieve one B102r form by form_id"""
    form = session.get(FormB102r, form_id)
    return form


def save_form(session: Session, form: FormB102r) -> None:
    """Persist changes to a B102r form"""
    session.merge(form)
    session.commit()


def save_form_with_log(
    session: Session,
    *,
    updated_form: FormB102r,
    original_form: FormB102r,
    change_reason: str | None = None,
    session_id: str | None = None,
):
    """
    Persist changes to a B102r form, logging any changes in AuditLog.
    @TODO Log changes to lookup ids
    """
    for field in FormB102r.model_fields.keys():

        # Skip "_raw" fields as these should not be changed
        # Skip "id" field because we won't be updating the PK
        if field.endswith("_raw") or field == "id":
            continue

        old_value = getattr(original_form, field)
        new_value = getattr(updated_form, field)

        assert updated_form.id is not None, "Form must have an ID to be saved"

        updated_form.dob_date = validate_date(updated_form.dob_date)

        if old_value != new_value:
            log_change(
                session=session,
                model_class=FormB102r,
                record_id=updated_form.id,
                field_name=str(field),
                old_label=str(old_value or ""),
                new_label=str(new_value or ""),
                change_reason=str(change_reason or ""),
                session_id=str(session_id or ""),
            )

    session.merge(updated_form)
    session.commit()


def get_individual_by_form_id(session: Session, form_id: int) -> Individual | None:
    """Retrieve the Individual attached to the B102r form by form_id"""
    individual = session.get(Individual, form_id)
    return individual
