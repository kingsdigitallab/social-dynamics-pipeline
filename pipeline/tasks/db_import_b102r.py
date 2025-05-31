from pathlib import Path
from typing import Optional

from sqlmodel import Session, select

from pipeline.database.init_db import engine
from pipeline.database.models import FormB102r, Individual
from pipeline.tasks.utils.db_import_utils import load_json_data


def get_image_name(source_filename: Path):
    img_path = Path(source_filename)
    img_frags = img_path.stem.split(".")
    img_stem = img_frags[0]
    img_ext = img_frags[1].split("_")[0]
    image_name = img_stem + "." + img_ext
    return image_name


def extract_b102r_data(source_filename: Path, json_data: dict) -> FormB102r:
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
        form_image=get_image_name(source_filename),
    )


def get_or_create_individual(
    session: Session, record: FormB102r, source_filename: str
) -> Individual:
    pdf_id = Path(source_filename).name.split("_")[0]  # type: ignore

    # @TODO account for 2 individuals in 1 PDF later
    stmt = select(Individual).where(
        Individual.pdf_id == pdf_id,  # Simple match on PDF ID
    )
    existing = session.exec(stmt).first()  # type: ignore
    if existing:
        return existing

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
