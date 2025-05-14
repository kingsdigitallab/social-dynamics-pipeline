from pathlib import Path

from sqlmodel import Session, select

from pipeline.database.init_db import engine
from pipeline.database.models import FormB102r, Individual
from pipeline.tasks.db_import_utils import load_json_data


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

    return FormB102r(
        lastname_raw=answers.get("B102r_1_Last_name", {}).get("answer"),
        firstname_raw=answers.get("B102r_2_First_name", {}).get("answer"),
        army_number_raw=answers.get("B102r_3_Army_number", {}).get("answer"),
        regiment_or_corp_raw=answers.get("B102r_4_Regiment", {}).get("answer"),
        engagement_raw=answers.get("B102r_5_Nature_of_engagement", {}).get("answer"),
        date_of_enlistment_raw=answers.get("B102r_6_Joining_date", {}).get("answer"),
        dob_raw=answers.get("B102r_7_DOB", {}).get("answer"),
        nationality_raw=answers.get("B102r_8_Nationality", {}).get("answer"),
        religion_raw=answers.get("B102r_9_Religion", {}).get("answer"),
        industry_group_raw=answers.get("B102r_10_Industry", {}).get("answer"),
        occupation_raw=answers.get("B102r_11_Occupation", {}).get("answer"),
        non_effective_cause_raw=answers.get("B102r_12_Non_effective_cause", {}).get(
            "answer"
        ),
        marital_status_raw=answers.get("B102r_13_Marital_status", {}).get("answer"),
        hometown_raw=answers.get("B102r_14_Hometown", {}).get("answer"),
        location_raw=answers.get("B102r_19_Location", {}).get("answer"),
        rank_raw=answers.get("B102r_A_Rank", {}).get("answer"),
        service_trade_raw=answers.get("B102r_B_Service_trade", {}).get("answer"),
        medical_category_raw=answers.get("B102r_C_Medical_category", {}).get("answer"),
        form_type_raw=answers.get("B102r_Form_type", {}).get("answer"),
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
