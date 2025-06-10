# mypy: disable-error-code=call-arg

from datetime import date, datetime, timezone
from pathlib import Path
from typing import List, Optional

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel

from pipeline.database.validators import validate_date


# ------------------------
# Core Individual
# ------------------------
class Individual(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pdf_id: Optional[str] = Field(default=None)
    lastname: Optional[str] = Field(default=None)
    firstname: Optional[str] = Field(default=None)
    army_number: Optional[str] = Field(default=None)
    dob: Optional[date] = Field(default=None)

    b102rs: List["FormB102r"] = Relationship(back_populates="individual")


# ------------------------
# Lookup Tables
# ------------------------
class Regiment(SQLModel, table=True):
    id: int = Field(primary_key=True)
    label: str
    desc: Optional[str] = None


class Rank(SQLModel, table=True):
    id: int = Field(primary_key=True)
    label: str
    desc: Optional[str] = None


class Engagement(SQLModel, table=True):
    id: int = Field(primary_key=True)
    label: str
    desc: Optional[str] = None


class Nationality(SQLModel, table=True):
    id: int = Field(primary_key=True)
    label: str
    desc: Optional[str] = None


class Religion(SQLModel, table=True):
    id: int = Field(primary_key=True)
    label: str
    desc: Optional[str] = None


class Industry(SQLModel, table=True):
    id: int = Field(primary_key=True)
    label: str
    desc: Optional[str] = None


class Occupation(SQLModel, table=True):
    id: int = Field(primary_key=True)
    label: str
    desc: Optional[str] = None


class ServiceTrade(SQLModel, table=True):
    id: int = Field(primary_key=True)
    label: str
    desc: Optional[str] = None


class MaritalStatus(SQLModel, table=True):
    id: int = Field(primary_key=True)
    label: str
    desc: Optional[str] = None


class MedicalCategory(SQLModel, table=True):
    id: int = Field(primary_key=True)
    label: str
    desc: Optional[str] = None


class Place(SQLModel, table=True):
    id: int = Field(primary_key=True)
    label: str
    desc: Optional[str] = None
    lat: Optional[float] = None
    long: Optional[float] = None
    external_uri: Optional[str] = Field(default=None, unique=True)


# ------------------------
# Form: B102r
# ------------------------
class FormB102r(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    form_image: Optional[Path] = Field(
        default=None, description="Path to the file with an image of this form"
    )
    form_type_raw: Optional[str] = Field(
        default=None, description="Form type as imported from raw source data"
    )
    form_type: Optional[str] = Field(default=None, description="Corrected form type")

    # Link to individual
    individual_id: int = Field(
        foreign_key="individual.id", description="Individual to which this form belongs"
    )
    individual: Optional[Individual] = Relationship(back_populates="b102rs")

    # Personal Info
    lastname_raw: Optional[str] = Field(
        default=None,
        description="Last name of individual as imported from raw source data",
    )
    lastname: Optional[str] = Field(
        default=None, description="Corrected last name of individual"
    )

    firstname_raw: Optional[str] = Field(
        default=None,
        description="First name of individual as imported from raw source data",
    )
    firstname: Optional[str] = Field(
        default=None, description="Corrected first name of individual"
    )

    army_number_raw: Optional[str] = Field(
        default=None,
        description="Army number as imported from raw source data",
    )
    army_number: Optional[str] = Field(
        default=None, description="Corrected army number"
    )

    registration_number_raw: Optional[str] = Field(
        default=None,
        description="Registration number as imported from raw source data",
    )
    registration_number: Optional[int] = Field(
        default=None, description="Corrected registration number"
    )

    dob_raw: Optional[str] = Field(
        default=None,
        description="Date of birth as imported from raw source data",
    )
    dob: Optional[str] = Field(
        default=None,
        description="Corrected date of birth",
    )
    dob_date: Optional[date] = Field(
        default=None,
        description="Date of birth normalised to valid date",
    )

    # noinspection PyNestedDecorators
    @field_validator("dob_date", mode="before")
    @classmethod
    def validate_date(cls, value):
        return validate_date(value)

    date_of_enlistment_raw: Optional[str] = Field(
        default=None,
        description="Date of enlistment as imported from raw source data",
    )
    date_of_enlistment: Optional[str] = Field(
        default=None,
        description="Corrected date of enlistment",
    )
    date_of_enlistment_date: Optional[date] = Field(
        default=None,
        description="Date of enlistment normalised to valid date",
    )

    non_effective_cause_raw: Optional[str] = Field(
        default=None,
        description="Non-effective cause as imported from raw source data",
    )
    non_effective_cause: Optional[str] = Field(
        default=None,
        description="Corrected non-effective cause",
    )

    location_raw: Optional[str] = Field(
        default=None,
        description="Location as imported from raw source data",
    )
    location: Optional[str] = Field(
        default=None,
        description="Corrected location",
    )

    # Categorical fields with raw + FK
    regiment_or_corp_raw: Optional[str] = Field(
        default=None,
        description="Regiment or corp as imported from raw source data",
    )
    regiment_or_corp: Optional[str] = Field(
        default=None,
        description="Corrected regiment or corp",
    )
    regiment_or_corp_id: Optional[int] = Field(
        default=None,
        foreign_key="regiment.id",
        description="Normalised regiment or corps value",
    )

    rank_raw: Optional[str] = Field(
        default=None,
        description="Rank as imported from raw source data",
    )
    rank: Optional[str] = Field(
        default=None,
        description="Corrected rank",
    )
    rank_id: Optional[int] = Field(
        default=None,
        foreign_key="rank.id",
        description="Normalised rank value",
    )

    engagement_raw: Optional[str] = Field(
        default=None,
        description="Engagement as imported from raw source data",
    )
    engagement: Optional[str] = Field(
        default=None,
        description="Corrected engagement",
    )
    engagement_id: Optional[int] = Field(
        default=None,
        foreign_key="engagement.id",
        description="Normalised engagement value",
    )

    nationality_raw: Optional[str] = Field(
        default=None,
        description="Nationality as imported from raw source data",
    )
    nationality: Optional[str] = Field(
        default=None,
        description="Corrected nationality",
    )
    nationality_id: Optional[int] = Field(
        default=None,
        foreign_key="nationality.id",
        description="Normalised nationality value",
    )

    religion_raw: Optional[str] = Field(
        default=None,
        description="Religion as imported from raw source data",
    )
    religion: Optional[str] = Field(
        default=None,
        description="Corrected religion",
    )
    religion_id: Optional[int] = Field(
        default=None,
        foreign_key="religion.id",
        description="Normalised religion value",
    )

    industry_group_raw: Optional[str] = Field(
        default=None,
        description="Industry as imported from raw source data",
    )
    industry_group: Optional[str] = Field(
        default=None,
        description="Corrected industry",
    )
    industry_group_id: Optional[int] = Field(
        default=None,
        foreign_key="industry.id",
        description="Normalised industry value",
    )

    occupation_raw: Optional[str] = Field(
        default=None,
        description="Occupation as imported from raw source data",
    )
    occupation: Optional[str] = Field(
        default=None,
        description="Corrected occupation",
    )
    occupation_id: Optional[int] = Field(
        default=None,
        foreign_key="occupation.id",
        description="Normalised occupation value",
    )

    service_trade_raw: Optional[str] = Field(
        default=None,
        description="Service trade as imported from raw source data",
    )
    service_trade: Optional[str] = Field(
        default=None,
        description="Corrected service trade",
    )
    service_trade_id: Optional[int] = Field(
        default=None,
        foreign_key="servicetrade.id",
        description="Normalised service trade value",
    )

    marital_status_raw: Optional[str] = Field(
        default=None,
        description="Marital status as imported from raw source data",
    )
    marital_status: Optional[str] = Field(
        default=None,
        description="Corrected marital status",
    )
    marital_status_id: Optional[int] = Field(
        default=None,
        foreign_key="maritalstatus.id",
        description="Normalised marital status value",
    )

    medical_category_raw: Optional[str] = Field(
        default=None,
        description="Medical category as imported from raw source data",
    )
    medical_category: Optional[str] = Field(
        default=None,
        description="Corrected medical category",
    )
    medical_category_id: Optional[int] = Field(
        default=None,
        foreign_key="medicalcategory.id",
        description="Normalised medical category value",
    )

    hometown_raw: Optional[str] = Field(
        default=None,
        description="Home town as imported from raw source data",
    )
    hometown: Optional[str] = Field(
        default=None,
        description="Corrected home town",
    )
    hometown_id: Optional[int] = Field(
        default=None,
        foreign_key="place.id",
        description="Normalised home town value",
    )


# ------------------------
# Audit log of changes to data
# ------------------------
class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    table_name: str = Field(index=True)
    record_id: int = Field(index=True)
    field_name: str
    field_type: Optional[str] = Field(
        default=None,
        description="Field datatype or lookup table name if this is a foreign key "
        "field",
    )

    # These strings should be JSON in the form:
    # {"label": "Married", "id": 2} for lookups
    # {"label": "Married"} for text fields
    old_value: Optional[str] = Field(
        default=None, description="Old field value: string should be in JSON format"
    )
    new_value: Optional[str] = Field(
        default=None, description="New field value: string should be in JSON format"
    )

    change_reason: Optional[str] = Field(default="manual")
    session_id: Optional[str] = Field(default=None)

    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
