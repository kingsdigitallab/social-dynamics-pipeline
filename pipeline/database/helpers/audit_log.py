import json
from datetime import datetime, timezone
from typing import Union

from sqlmodel import Session

from pipeline.database.models import AuditLog


def to_json_value(label: str, id_: int | None = None) -> str:
    """Create a JSON string for storing lookup/text field values."""
    data: dict[str, Union[str, int]] = {"label": label}
    if id_ is not None:
        data["id"] = id_
    return json.dumps(data)


def log_change(
    session: Session,
    *,
    table_name: str,
    record_id: int,
    field_name: str,
    field_type: str | None,
    old_label: str,
    new_label: str,
    old_id: int | None = None,
    new_id: int | None = None,
    change_reason: str = "manual",
    session_id: str | None = None,
):
    """Insert an audit log row into the database."""
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
