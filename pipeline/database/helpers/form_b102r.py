from sqlmodel import Session, select

from pipeline.database.models import FormB102r


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
    form = session.get(FormB102r.id, form_id)
    return form
