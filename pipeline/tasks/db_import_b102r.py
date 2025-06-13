import logging
from pathlib import Path
from typing import Optional

from sqlmodel import Session, select

from pipeline.database.helpers.matchers import is_individual_match
from pipeline.database.init_db import engine
from pipeline.database.models import FormB102r, Individual
from pipeline.logging_config import setup_logging
from pipeline.tasks.utils.db_import_utils import get_image_path, load_json_data

setup_logging()
logger = logging.getLogger(__name__)


def extract_b102r_data(source_filename: Path, json_data: dict) -> FormB102r:
    """Extract B102r data from a BVQA json file and return an instantiated FormB102r."""
    # @TODO handle more than 1 model section in JSON
    model_data = next(iter(json_data["models"].values()))  # First model section
    answers = model_data["questions"]

    def answer(key: str) -> Optional[str]:
        return answers.get(key, {}).get("answer")

    return FormB102r(
        lastname_raw=answer("B102r_1_Last_name"),
        lastname=answer("B102r_1_Last_name"),
        firstname_raw=answer("B102r_2_First_name"),
        firstname=answer("B102r_2_First_name"),
        army_number_raw=answer("B102r_3_Army_number"),
        army_number=answer("B102r_3_Army_number"),
        regiment_or_corp_raw=answer("B102r_4_Regiment"),
        regiment_or_corp=answer("B102r_4_Regiment"),
        engagement_raw=answer("B102r_5_Nature_of_engagement"),
        engagement=answer("B102r_5_Nature_of_engagement"),
        date_of_enlistment_raw=answer("B102r_6_Joining_date"),
        date_of_enlistment=answer("B102r_6_Joining_date"),
        dob_raw=answer("B102r_7_DOB"),
        dob=answer("B102r_7_DOB"),
        nationality_raw=answer("B102r_8_Nationality"),
        nationality=answer("B102r_8_Nationality"),
        religion_raw=answer("B102r_9_Religion"),
        religion=answer("B102r_9_Religion"),
        industry_group_raw=answer("B102r_10_Industry"),
        industry_group=answer("B102r_10_Industry"),
        occupation_raw=answer("B102r_11_Occupation"),
        occupation=answer("B102r_11_Occupation"),
        non_effective_cause_raw=answer("B102r_12_Non_effective_cause"),
        non_effective_cause=answer("B102r_12_Non_effective_cause"),
        marital_status_raw=answer("B102r_13_Marital_status"),
        marital_status=answer("B102r_13_Marital_status"),
        hometown_raw=answer("B102r_14_Hometown"),
        hometown=answer("B102r_14_Hometown"),
        location_raw=answer("B102r_19_Location"),
        location=answer("B102r_19_Location"),
        rank_raw=answer("B102r_A_Rank"),
        rank=answer("B102r_A_Rank"),
        service_trade_raw=answer("B102r_B_Service_trade"),
        service_trade=answer("B102r_B_Service_trade"),
        medical_category_raw=answer("B102r_C_Medical_category"),
        medical_category=answer("B102r_C_Medical_category"),
        form_type_raw=answer("B102r_Form_type"),
        form_type=answer("B102r_Form_type"),
        form_image=get_image_path(source_filename),
    )


def get_or_create_individual(
    session: Session, record: FormB102r, source_filename: str
) -> Individual:
    """
    Check if a matching Individual exists for the PDF filename identifier; if not
    create one.

    Individuals are considered a "match" if they match on PDF filename identifier.

    Log if record matches individual on lastname and firstname, or not, for further
    analysis. At the moment, the function does not use this to supplement matching
    because the heuristic is not accurate enough. Log analysis can be used to identify
    and manually fix cases where there are 2 individuals in 1 PDF.

    @TODO improve heuristic to allow for more accurate matching.
    """
    pdf_id = Path(source_filename).name.split("_")[0]  # type: ignore

    # Find any existing Individuals with the same PDF number
    stmt = select(Individual).where(
        Individual.pdf_id == pdf_id,
    )
    existing: list[Individual] = list(session.exec(stmt))  # type: ignore

    if existing:
        num_matches = len(existing)
        logger.info("%s existing Individual found for pdf_id=%s", num_matches, pdf_id)

        # Check and log (only) if any existing individuals also match on name fields
        for existing_individual in existing:
            if is_individual_match(existing_individual, record):
                logger.info(
                    "Individual id=%s and FormB102r form_image=%s match on name "
                    "fields.",
                    existing_individual.id,
                    record.form_image,
                )
            else:
                logger.info(
                    "Individual id=%s and FormB102r form_image=%s do not match on "
                    "name fields.",
                    existing_individual.id,
                    record.form_image,
                )

        if num_matches == 1:
            return existing[0]
        elif num_matches > 1:
            # This case is currently rare so just return first match for now and log
            logger.warning(
                "More than one matching Individual found for pdf_id=%s", pdf_id
            )
            return existing[0]

    # Otherwise there is no existing individual, so create one
    individual = Individual(
        pdf_id=pdf_id,
        lastname=record.lastname_raw,
        firstname=record.firstname_raw,
    )
    session.add(individual)
    session.commit()
    session.refresh(individual)
    return individual


def import_b102r_json(json_path: Path, session: Session):
    data = load_json_data(json_path)
    form_record = extract_b102r_data(json_path, data)
    individual = get_or_create_individual(
        session, form_record, source_filename=str(json_path)
    )
    form_record.individual = individual
    session.add(form_record)
    session.commit()


def import_all_in_dir(folder: Path):
    with Session(engine) as session:
        for file in folder.glob("*.json"):
            import_b102r_json(file, session)
