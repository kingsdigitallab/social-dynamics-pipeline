# ruff: noqa: E501
# type: ignore

import json
import random
import string
from datetime import date, timedelta
from pathlib import Path

# Constants
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "data" / "public" / "json"
OUTPUT_DIR.mkdir(exist_ok=True)

HASHES = {
    "B102r_1_Last_name": "What is the surname of the person recorded on this form? Answer only with the surname.",
    "B102r_2_First_name": "What is the christian name of the person recorded on this form? Answer only with the christian names.",
    "B102r_3_Army_number": "What is the army number of the person recorded on this form? Answer only with the army number and remove any puncutation.",
    "B102r_4_Regiment": "What is the name of the regiment or corps of the recorded person on this form? Answer only with the regiment or corp identifier.",
    "B102r_5_Nature_of_engagement": "What is the nature of engagement recorded on this form? Answer only with the nature of engagement.",
    "B102r_6_Joining_date": "What is the date of joining or date of enlistment of the person recorded on this form? Answer only with the date in the form DD/MM/YYYY",
    "B102r_7_DOB": "What is the date of birth of the person recorded on this form? Answer only with the date in the form DD/MM/YYYY",
    "B102r_8_Nationality": "What is the nationality or dual nationality of the person recorded on this form? Answer only with the nationality identifier.",
    "B102r_9_Religion": "What is the religion of the person recorded on this form? Answer only with the religion identifier.",
    "B102r_10_Industry": "What is the industry group recorded for the person on this form? Answer only with the industry group identifier.",
    "B102r_11_Occupation": "What is the occupational classification of the person on this form? Answer only with the occupational classification.",
    "B102r_12_Non_effective_cause": "What is the cause of becoming non-effective for person recorded on this form? Answer only with the cause.",
    "B102r_13_Marital_status": "What is the single or married status of the person recorded on this form? Answer only with the single or married status.",
    "B102r_14_Hometown": "What is the hometown and county of the person recorded on this form? Answer only with the hometown and county.",
    "B102r_19_Location": "What is the location of the person recorded on this form? Answer only with the location.",
    "B102r_A_Rank": "What is the rank of the person recorded on this form? Answer only with the rank.",
    "B102r_B_Service_trade": "What is the service trade of the person recorded on this form? Answer only with the service trade.",
    "B102r_C_Medical_category": "What is the medical category of the person recorded on this form? Answer only with the medical category.",
    "B102r_Text_json": "Extract all the text from the image into a JSON object. Answer only with a valid JSON object and include no newlines or markdown. Ensure each key is a printed question or label and each value is the corresponding handwritten response.",
    "B102r_Form_type": "What is this form type? Answer only with the exact form number.",
}

# Some example data
LASTNAMES = ["SMITH", "JONES", "TAYLOR", "BROWN", "JOHNSON", "DAVIS"]
FIRSTNAMES = ["John", "Robert", "Michael", "William", "David", "James"]
REGIMENTS = ["RA", "RE", "RAMC", "RASC", "RHA", "RWF"]
NATIONALITIES = ["E", "S", "W", "I"]
RELIGIONS = ["C of E", "R.C.", "M", "J"]
INDUSTRIES = ["V.H.", "C.T.", "M.L."]
OCCUPATIONS = ["336/47", "874/12", "122/19"]
CAUSES = ["Class 2(T) Res", "Discharged", "Killed in Action"]
LOCATIONS = ["London", "Manchester", "Belfast", "Glasgow"]
RANKS = ["Pte", "Cpl", "Sgt"]
TRADES = ["Cook", "Clerk", "Driver"]
MED_CATS = ["A-1", "B-2", "C-3"]
MARITALS = ["S", "M"]
FORM_TYPE = "A.F.B. 102"

PDFS = [f"APV0{i}" for i in range(1, 11)]


def random_date(start: date, end: date) -> date:
    """Return a random date between start and end (inclusive)."""
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)


for i in PDFS:
    dob = random_date(date(1920, 1, 1), date(1930, 12, 31)).strftime("%d/%m/%Y")
    doe = random_date(date(1937, 1, 1), date(1947, 12, 31)).strftime("%d/%m/%Y")

    questions = {
        "B102r_1_Last_name": {
            "answer": random.choice(LASTNAMES),
            "hash": HASHES["B102r_1_Last_name"],
        },
        "B102r_2_First_name": {
            "answer": random.choice(FIRSTNAMES),
            "hash": HASHES["B102r_2_First_name"],
        },
        "B102r_3_Army_number": {
            "answer": str(random.randint(3000000, 4000000)),
            "hash": HASHES["B102r_3_Army_number"],
        },
        "B102r_4_Regiment": {
            "answer": random.choice(REGIMENTS),
            "hash": HASHES["B102r_4_Regiment"],
        },
        "B102r_5_Nature_of_engagement": {
            "answer": "TA",
            "hash": HASHES["B102r_5_Nature_of_engagement"],
        },
        "B102r_6_Joining_date": {
            "answer": f"{doe}",
            "hash": HASHES["B102r_6_Joining_date"],
        },
        "B102r_7_DOB": {
            "answer": f"{dob}",
            "hash": HASHES["B102r_7_DOB"],
        },
        "B102r_8_Nationality": {
            "answer": random.choice(NATIONALITIES),
            "hash": HASHES["B102r_8_Nationality"],
        },
        "B102r_9_Religion": {
            "answer": random.choice(RELIGIONS),
            "hash": HASHES["B102r_9_Religion"],
        },
        "B102r_10_Industry": {
            "answer": random.choice(INDUSTRIES),
            "hash": HASHES["B102r_10_Industry"],
        },
        "B102r_11_Occupation": {
            "answer": random.choice(OCCUPATIONS),
            "hash": HASHES["B102r_11_Occupation"],
        },
        "B102r_12_Non_effective_cause": {
            "answer": random.choice(CAUSES),
            "hash": HASHES["B102r_12_Non_effective_cause"],
        },
        "B102r_13_Marital_status": {
            "answer": random.choice(MARITALS),
            "hash": HASHES["B102r_13_Marital_status"],
        },
        "B102r_14_Hometown": {
            "answer": random.choice(LOCATIONS),
            "hash": HASHES["B102r_14_Hometown"],
        },
        "B102r_19_Location": {
            "answer": random.choice(LOCATIONS),
            "hash": HASHES["B102r_19_Location"],
        },
        "B102r_A_Rank": {
            "answer": random.choice(RANKS),
            "hash": HASHES["B102r_A_Rank"],
        },
        "B102r_B_Service_trade": {
            "answer": random.choice(TRADES),
            "hash": HASHES["B102r_B_Service_trade"],
        },
        "B102r_C_Medical_category": {
            "answer": random.choice(MED_CATS),
            "hash": HASHES["B102r_C_Medical_category"],
        },
        "B102r_Text_json": {"answer": "{}", "hash": HASHES["B102r_Text_json"]},
        "B102r_Form_type": {"answer": FORM_TYPE, "hash": HASHES["B102r_Form_type"]},
    }

    output = {
        "meta": {"started": 0, "version": "0.2.0"},
        "models": {"Qwen/Qwen2.5-VL-3B-Instruct:": {"questions": questions}},
    }

    with open(
        OUTPUT_DIR
        / f"{i}_page{random.choice(string.digits)}_img1_b102r.jpg_{str(random.randint(100000, 900000))}.qas.json",
        "w",
    ) as f:
        json.dump(output, f, indent=2)

print(f"Created 10 sample JSON files in: {OUTPUT_DIR}")
