from datetime import date

import pytest
from sqlmodel import Session, SQLModel, create_engine, select

from pipeline.database.helpers.audit_log import log_change
from pipeline.database.models import AuditLog, FormB102r, Individual


@pytest.fixture
def populated_session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    test_individuals = [
        Individual(id=1, dob=date(1901, 1, 1)),
        Individual(id=2, dob=date(1902, 2, 2)),
        Individual(id=3, dob=date(1903, 3, 3)),
    ]

    test_forms = [
        FormB102r(id=11, individual_id=1, lastname="Apple"),
        FormB102r(id=12, individual_id=2, lastname="Banana"),
        FormB102r(id=13, individual_id=3, lastname="Carrot"),
    ]
    with Session(engine) as session:
        session.add_all(test_individuals)
        session.add_all(test_forms)
        session.commit()
        yield session


class TestLogChange:
    def test_log_change_to_text_field_in_formb102r(self, populated_session):
        log_change(
            populated_session,
            model_class=FormB102r,
            record_id=11,
            field_name="lastname",
            old_label="Apple",
            new_label="Acai",
            change_reason="test",
        )

        audit_rows = populated_session.exec(select(AuditLog)).all()
        assert len(audit_rows) == 1
        row = audit_rows[0]
        assert row.table_name == "FormB102r".lower()
        assert row.record_id == 11
        assert row.field_name == "lastname"
        assert row.field_type == "str"
        assert row.old_value == '{"label": "Apple"}'
        assert row.new_value == '{"label": "Acai"}'
        assert row.change_reason == "test"

    def test_log_change_to_date_field_in_individual(self, populated_session):
        old_dob = date(1901, 1, 1)
        new_dob = date(1910, 12, 12)
        log_change(
            populated_session,
            model_class=Individual,
            record_id=1,
            field_name="dob",
            old_label=old_dob.strftime("%d/%m/%Y"),
            new_label=new_dob.strftime("%d/%m/%Y"),
            change_reason="test",
        )
        audit_rows = populated_session.exec(select(AuditLog)).all()
        assert len(audit_rows) == 1
        row = audit_rows[0]
        assert row.table_name == "Individual".lower()
        assert row.record_id == 1
        assert row.field_name == "dob"
        assert row.field_type == "date"
        assert row.old_value == '{"label": "01/01/1901"}'
        assert row.new_value == '{"label": "12/12/1910"}'
        assert row.change_reason == "test"
