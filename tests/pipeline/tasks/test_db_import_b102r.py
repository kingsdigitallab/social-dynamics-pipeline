import pytest
from sqlmodel import Session, SQLModel, create_engine

from pipeline.database.models import FormB102r, Individual
from pipeline.tasks.db_import_b102r import get_or_create_individual


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


class TestGetOrCreateIndividual:
    def test_get_or_create_individual_creates(self, session):
        form = FormB102r(id=1, lastname_raw="Smith", firstname_raw="John")
        result = get_or_create_individual(
            session, form, "APV0001_page8_img1_b102r.jpg_644894.qas.json"
        )

        assert result.pdf_id == "APV0001"
        assert result.lastname == "Smith"
        assert result.firstname == "John"

    def test_get_or_create_individual_returns_existing(self, session):
        # Create existing individual
        ind = Individual(pdf_id="APV0002", lastname="Smith", firstname="John")
        session.add(ind)
        session.commit()
        session.refresh(ind)

        # Use matching form
        form = FormB102r(id=2, lastname_raw="Smith", firstname_raw="John")
        result = get_or_create_individual(
            session, form, "APV0002_page8_img1_b102r.jpg_644894.qas.json"
        )

        assert result.id == ind.id
