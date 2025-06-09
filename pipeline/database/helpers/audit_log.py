import json
from datetime import datetime, timezone
from typing import Optional, Union, get_args, get_origin

from sqlmodel import Session, SQLModel

from pipeline.database.models import AuditLog


def to_json_value(label: str, id_: int | None = None) -> str:
    """Create a JSON string for storing lookup/text field values."""
    data: dict[str, Union[str, int]] = {"label": label}
    if id_ is not None:
        data["id"] = id_
    return json.dumps(data)


def infer_field_type(model: type[SQLModel], field_name: str) -> Optional[str]:
    """
    Infers the type of a field so it can be stored in the AuditLog field_type.
    Written by GPT-4o (gpt-4o-2024-06-03); verified by author
    """
    field_info = model.model_fields.get(field_name)
    if not field_info:
        return None  # field doesn't exist

    outer_type = field_info.annotation

    # Handle Optional[Something]
    if get_origin(outer_type) is Union:
        args = [t for t in get_args(outer_type) if t is not type(None)]
        if args:
            outer_type = args[0]  # type: ignore

    # Foreign key fields are usually ints and end with _id
    if field_name.endswith("_id") and outer_type is int:
        # Use the field name minus _id as a guess for table name
        return field_name[:-3]  # e.g. "rank_id" → "rank"

    # Otherwise, just use the type name
    return outer_type.__name__


def log_change(
    session: Session,
    *,
    model_class: type[SQLModel],
    record_id: int,
    field_name: str,
    old_label: str,
    new_label: str,
    old_id: int | None = None,
    new_id: int | None = None,
    change_reason: str = "manual",
    session_id: str | None = None,
):
    """Insert an audit log row into the database."""
    field_type = infer_field_type(model_class, field_name)
    table_name = model_class.__tablename__

    audit_log = AuditLog(
        table_name=table_name,
        record_id=record_id,
        field_name=field_name,
        field_type=field_type,
        old_value=to_json_value(old_label, old_id),
        new_value=to_json_value(new_label, new_id),
        change_reason=change_reason,
        session_id=session_id,
        timestamp=datetime.now(timezone.utc),
    )
    session.add(audit_log)
    session.commit()
