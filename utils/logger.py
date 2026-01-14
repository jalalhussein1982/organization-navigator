"""Logging utilities for Organizations Explorer."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from config import LOGS_FOLDER, COUNTRIES


def ensure_logs_folder():
    """Ensure logs folder exists."""
    LOGS_FOLDER.mkdir(parents=True, exist_ok=True)


def generate_log_filename(country_code: str, action: str) -> str:
    """Generate log filename with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}_{country_code}_{action}.json"


def log_edit(
    country_code: str,
    record_id: int,
    organization_name: str,
    full_record_before: Dict[str, Any],
    changes: Dict[str, Dict[str, Any]],
) -> bool:
    """Log an edit action."""
    ensure_logs_folder()

    country_name = COUNTRIES.get(country_code, {}).get("name", country_code)

    log_data = {
        "action": "edit",
        "timestamp": datetime.now().isoformat(),
        "database": country_code,
        "database_name": country_name,
        "record_id": record_id,
        "organization_name": organization_name,
        "full_record_before": full_record_before,
        "changes": changes,
    }

    filename = generate_log_filename(country_code, "edit")
    filepath = LOGS_FOLDER / filename

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False, default=str)
        return True
    except Exception as e:
        print(f"Error writing log: {e}")
        return False


def log_delete(
    country_code: str,
    record_id: int,
    organization_name: str,
    full_record: Dict[str, Any],
) -> bool:
    """Log a delete action."""
    ensure_logs_folder()

    country_name = COUNTRIES.get(country_code, {}).get("name", country_code)

    log_data = {
        "action": "delete",
        "timestamp": datetime.now().isoformat(),
        "database": country_code,
        "database_name": country_name,
        "record_id": record_id,
        "organization_name": organization_name,
        "full_record": full_record,
    }

    filename = generate_log_filename(country_code, "delete")
    filepath = LOGS_FOLDER / filename

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False, default=str)
        return True
    except Exception as e:
        print(f"Error writing log: {e}")
        return False


def log_delete_batch(
    country_code: str,
    records: List[Dict[str, Any]],
) -> bool:
    """Log a batch delete action for multiple records."""
    ensure_logs_folder()

    country_name = COUNTRIES.get(country_code, {}).get("name", country_code)

    log_data = {
        "action": "delete_batch",
        "timestamp": datetime.now().isoformat(),
        "database": country_code,
        "database_name": country_name,
        "count": len(records),
        "records": records,
    }

    filename = generate_log_filename(country_code, "delete")
    filepath = LOGS_FOLDER / filename

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False, default=str)
        return True
    except Exception as e:
        print(f"Error writing log: {e}")
        return False


def calculate_changes(
    before: Dict[str, Any],
    after: Dict[str, Any],
    prefix: str = "",
) -> Dict[str, Dict[str, Any]]:
    """Calculate the changes between two records with deep comparison.

    Returns a flat dict with dot-notation keys for nested changes.
    E.g., {"related.partners": {"before": [...], "after": [...]}}
    """
    changes = {}

    all_keys = set(before.keys()) | set(after.keys())

    for key in all_keys:
        full_key = f"{prefix}.{key}" if prefix else key
        before_val = before.get(key)
        after_val = after.get(key)

        # Skip if values are equal
        if before_val == after_val:
            continue

        # If both are dicts, recurse for deep comparison
        if isinstance(before_val, dict) and isinstance(after_val, dict):
            nested_changes = calculate_changes(before_val, after_val, full_key)
            changes.update(nested_changes)
        else:
            # Record the change at this level
            changes[full_key] = {
                "before": before_val,
                "after": after_val,
            }

    return changes
