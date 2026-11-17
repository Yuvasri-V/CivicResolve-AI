"""Lightweight column checks for local MySQL prototypes."""

from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


def ensure_complaint_columns(engine: Engine) -> None:
    inspector = inspect(engine)
    if "complaints" not in inspector.get_table_names():
        return

    existing = {col["name"] for col in inspector.get_columns("complaints")}
    additions = {
        "assigned_team": "VARCHAR(120) NULL",
        "response_at": "DATETIME NULL",
        "resolved_at": "DATETIME NULL",
        "resolution_notes": "TEXT NULL",
        "resolution_deadline": "DATETIME NULL",
        "verified_at": "DATETIME NULL",
    }

    with engine.begin() as conn:
        for name, ddl in additions.items():
            if name not in existing:
                conn.execute(
                    text(f"ALTER TABLE complaints ADD COLUMN {name} {ddl}")
                )
