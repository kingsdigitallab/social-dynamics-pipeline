import pytest
from sqlmodel import Session, SQLModel, create_engine

from pipeline.database.helpers.individual import get_individuals
from pipeline.database.models import Individual


@pytest.fixture
def populated_session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    # At this stage in project all PDFs have "APV" prefix
    test_individuals = [
        Individual(pdf_id=None),
        Individual(pdf_id="APV001118621"),
        Individual(pdf_id="APV900031890"),
        Individual(pdf_id="APV002036895"),
    ]
    with Session(engine) as session:
        session.add_all(test_individuals)
        session.commit()
        yield session


class TestGetIndividuals:
    def test_individuals_sorted_by_pdf_id(self, populated_session):
        result = get_individuals(populated_session)
        assert [ind.pdf_id for ind in result] == [
            None,
            "APV001118621",
            "APV002036895",
            "APV900031890",
        ]
