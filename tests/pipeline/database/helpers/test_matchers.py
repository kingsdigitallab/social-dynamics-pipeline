import pytest

from pipeline.database.helpers.matchers import is_individual_match
from pipeline.database.models import FormB102r, Individual


@pytest.mark.parametrize(
    "individual_fields, form_fields, expected_result",
    [
        # Exactly two matching fields
        (
            {
                "id": "1",
                "pdf_id": "APV0001",
                "lastname": "Smith",
                "firstname": "John",
            },
            {
                "id": "1",
                "lastname_raw": "Smith",
                "firstname_raw": "John",
            },
            True,
        ),
        # Only one matching field
        (
            {
                "id": "2",
                "pdf_id": "APV0001",
                "lastname": "Brown",
                "firstname": "Felix",
            },
            {
                "id": "2",
                "lastname_raw": "Brown",
                "firstname_raw": "James",
            },
            False,
        ),
        (
            {
                "id": "3",
                "pdf_id": "APV0001",
                "lastname": "Carter",
                "firstname": "Felix",
            },
            {
                "id": "3",
                "lastname_raw": "Brown",
                "firstname_raw": "Felix",
            },
            False,
        ),
        # No matching fields
        (
            {
                "id": "4",
                "pdf_id": "APV0001",
                "lastname": "Taylor",
                "firstname": "Robert",
            },
            {
                "id": "4",
                "lastname_raw": "Smith",
                "firstname_raw": "James",
            },
            False,
        ),
        # Match after lowercasing
        (
            {
                "id": "5",
                "pdf_id": "APV0001",
                "lastname": "smith",
                "firstname": "john",
            },
            {
                "id": "5",
                "lastname_raw": "SMITH",
                "firstname_raw": "JOHN",
            },
            True,
        ),
        # Match after stripping whitespace
        (
            {
                "id": "6",
                "pdf_id": "APV0001",
                "lastname": "Smith",
                "firstname": "John",
            },
            {
                "id": "6",
                "lastname_raw": " Smith ",
                "firstname_raw": "  John ",
            },
            True,
        ),
        # Match after removing punctuation
        (
            {
                "id": "7",
                "pdf_id": "APV0001",
                "lastname": "ODonnell",
                "firstname": "John",
            },
            {
                "id": "7",
                "lastname_raw": "O'Donnell",
                "firstname_raw": "John",
            },
            True,
        ),
        # Match after lowercase + punctuation strip + whitespace strip
        (
            {
                "id": "8",
                "pdf_id": "APV0001",
                "lastname": "o donnell",
                "firstname": "john",
            },
            {
                "id": "8",
                "lastname_raw": " O'DONNELL ",
                "firstname_raw": " JOHN ",
            },
            True,
        ),
    ],
)
def test_is_individual_match(individual_fields, form_fields, expected_result):
    individual = Individual(**individual_fields)
    form = FormB102r(**form_fields)
    assert is_individual_match(individual, form) == expected_result
