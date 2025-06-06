from sqlmodel import Session, select

from pipeline.database.models import Individual


def get_individuals(session: Session) -> list[Individual]:
    """Retrieve a list of all individuals sorted by the numeric part of pdf_id"""
    statement = select(Individual)
    individuals = session.exec(statement).all()
    # Sort by numeric part of PDF ID
    return sorted(
        individuals,
        key=lambda ind: (
            int(ind.pdf_id.removeprefix("APV"))
            if ind.pdf_id and ind.pdf_id.startswith("APV")
            else 0
        ),
    )
