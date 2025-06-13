"""Helpers for matching individuals and forms based on heuristics."""

import logging
import string
from typing import Optional

from pipeline.database.models import FormB102r, Individual
from pipeline.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def is_individual_match(individual: Individual, form: FormB102r) -> bool:
    """Return True if the Individual is a perfect match for the data on the B102r form.

    A match is determined by comparing the 2 name fields:
    - lastname
    - firstname

    If both match fields, then the Individual is considered to be a match.

    At the moment these are the only 2 fields that are available in both the Individual
    and B102r tables. This may change in the future.

    Matching is done with a simple string comparison of each field normalised to lower
    case and removing punctuation and white space.
    """

    def normalise(data_str: Optional[str]) -> str:
        """
        Normalise a string to lowercase, removing punctuation and white space.
        """
        if not data_str:
            return ""

        data_str_lower = data_str.strip().lower()
        data_str_az = data_str_lower.translate(
            str.maketrans("", "", string.punctuation)
        )
        data_str_normalised = data_str_az.translate(
            str.maketrans("", "", string.whitespace)
        )
        return data_str_normalised

    i_lastname_norm = normalise(individual.lastname)
    i_firstname_norm = normalise(individual.firstname)
    f_lastname_norm = normalise(form.lastname_raw)
    f_firstname_norm = normalise(form.firstname_raw)

    matches = 0

    logger.info("Match result details for pdf_id=%s...", individual.pdf_id)

    if i_lastname_norm == f_lastname_norm:
        matches += 1
        logger.info(
            "Individual id=%s and FormB102r form_image==%s match on field 'lastname': "
            "%s, %s",
            individual.id,
            form.form_image,
            individual.lastname,
            form.lastname_raw,
        )
    else:
        logger.info(
            "Individual id=%s and FormB102r form_image==%s do not match on field "
            "'lastname': %s, %s",
            individual.id,
            form.form_image,
            individual.lastname,
            form.lastname_raw,
        )

    if i_firstname_norm == f_firstname_norm:
        matches += 1
        logger.info(
            "Individual id=%s and FormB102r form_image==%s match on field 'firstname': "
            "%s, %s",
            individual.id,
            form.form_image,
            individual.firstname,
            form.firstname_raw,
        )
    else:
        logger.info(
            "Individual id=%s and FormB102r form_image==%s do not match on field "
            "'lastname': %s, %s",
            individual.id,
            form.form_image,
            individual.firstname,
            form.firstname_raw,
        )

    logger.info(
        "Match result for pdf_id=%s: " "%s matches.", individual.pdf_id, matches
    )

    if matches == 2:
        return True
    else:
        return False
