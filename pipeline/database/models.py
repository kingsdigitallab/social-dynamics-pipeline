# mypy: disable-error-code=call-arg

from datetime import date
from pathlib import Path
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


# ------------------------
# Core Individual
# ------------------------
class Individual(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pdf_id: Optional[str] = Field(default=None)
    lastname: Optional[str] = Field(default=None)
    firstname: Optional[str] = Field(default=None)
    army_number: Optional[int] = Field(default=None)
    dob: Optional[date] = Field(default=None)

    b102rs: List["FormB102r"] = Relationship(back_populates="individual")


# ------------------------
# Lookup Tables
# ------------------------
class Regiment(SQLModel, table=True):
    id: int = Field(primary_key=True)
    desc: str


class Rank(SQLModel, table=True):
    id: int = Field(primary_key=True)
    desc: str


class Engagement(SQLModel, table=True):
    id: int = Field(primary_key=True)
    type: str
    expanded_form: Optional[str] = None


class Nationality(SQLModel, table=True):
    id: int = Field(primary_key=True)
    desc: str


class Religion(SQLModel, table=True):
    id: int = Field(primary_key=True)
    desc: str


class Industry(SQLModel, table=True):
    id: int = Field(primary_key=True)
    desc: str


class Occupation(SQLModel, table=True):
    id: int = Field(primary_key=True)
    desc: str


class ServiceTrade(SQLModel, table=True):
    id: int = Field(primary_key=True)
    desc: str


class MaritalStatus(SQLModel, table=True):
    id: int = Field(primary_key=True)
    desc: str


class MedicalCategory(SQLModel, table=True):
    id: int = Field(primary_key=True)
    desc: str


class Place(SQLModel, table=True):
    id: int = Field(primary_key=True)
    toponym: str
    lat: Optional[float] = None
    long: Optional[float] = None
    external_uri: Optional[str] = Field(default=None, unique=True)


# ------------------------
# Form: B102r
# ------------------------
class FormB102r(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    form_type_raw: Optional[str] = None
    form_image: Optional[Path] = None

    # Link to individual
    individual_id: int = Field(foreign_key="individual.id")
    individual: Optional[Individual] = Relationship(back_populates="b102rs")

    # Personal Info
    lastname_raw: Optional[str] = None
    lastname: Optional[str] = None
    firstname_raw: Optional[str] = None
    firstname: Optional[str] = None
    army_number_raw: Optional[str] = None
    army_number: Optional[int] = None
    registration_number_raw: Optional[str] = None
    registration_number: Optional[int] = None
    dob_raw: Optional[str] = None
    dob: Optional[date] = None
    date_of_enlistment_raw: Optional[str] = None
    date_of_enlistment: Optional[date] = None
    non_effective_cause_raw: Optional[str] = None
    non_effective_cause: Optional[str] = None
    location_raw: Optional[str] = None
    location: Optional[str] = None

    # Categorical fields with raw + FK
    regiment_or_corp_raw: Optional[str] = None
    regiment_or_corp_id: Optional[int] = Field(default=None, foreign_key="regiment.id")

    rank_raw: Optional[str] = None
    rank_id: Optional[int] = Field(default=None, foreign_key="rank.id")

    engagement_raw: Optional[str] = None
    engagement_id: Optional[int] = Field(default=None, foreign_key="engagement.id")

    nationality_raw: Optional[str] = None
    nationality_id: Optional[int] = Field(default=None, foreign_key="nationality.id")

    religion_raw: Optional[str] = None
    religion_id: Optional[int] = Field(default=None, foreign_key="religion.id")

    industry_group_raw: Optional[str] = None
    industry_group_id: Optional[int] = Field(default=None, foreign_key="industry.id")

    occupation_raw: Optional[str] = None
    occupation_id: Optional[int] = Field(default=None, foreign_key="occupation.id")

    service_trade_raw: Optional[str] = None
    service_trade_id: Optional[int] = Field(default=None, foreign_key="servicetrade.id")

    marital_status_raw: Optional[str] = None
    marital_status_id: Optional[int] = Field(
        default=None, foreign_key="maritalstatus.id"
    )

    medical_category_raw: Optional[str] = None
    medical_category_id: Optional[int] = Field(
        default=None, foreign_key="medicalcategory.id"
    )

    hometown_raw: Optional[str] = None
    hometown_id: Optional[int] = Field(default=None, foreign_key="place.id")
