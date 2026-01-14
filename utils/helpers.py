"""Helper utilities for Organizations Explorer."""

from typing import Optional


def truncate_text(text: Optional[str], max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length with suffix."""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_url(url: Optional[str], max_length: int = 30) -> str:
    """Format URL for display (truncated)."""
    if not url:
        return ""
    # Remove protocol for display
    display_url = url.replace("https://", "").replace("http://", "")
    # Remove trailing slash
    display_url = display_url.rstrip("/")
    return truncate_text(display_url, max_length)


def format_address(
    street: Optional[str] = None,
    postal_code: Optional[str] = None,
    city: Optional[str] = None,
    state_region: Optional[str] = None,
    country_name: Optional[str] = None,
) -> str:
    """Format address components into a single string."""
    parts = []

    if street:
        parts.append(street)

    city_parts = []
    if postal_code:
        city_parts.append(postal_code)
    if city:
        city_parts.append(city)
    if city_parts:
        parts.append(" ".join(city_parts))

    if state_region:
        parts.append(state_region)

    if country_name:
        parts.append(country_name)

    return ", ".join(parts)


def format_city_country(city: Optional[str], country_name: Optional[str]) -> str:
    """Format city and country for table display."""
    parts = []
    if city:
        parts.append(city)
    if country_name:
        parts.append(country_name)
    return ", ".join(parts) if parts else "-"


def safe_int(value, default: int = 0) -> int:
    """Safely convert value to int."""
    if value is None:
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value, default: float = 0.0) -> float:
    """Safely convert value to float."""
    if value is None:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def bool_to_yes_no(value) -> str:
    """Convert boolean/int to Yes/No string."""
    if value is None:
        return "-"
    return "Yes" if value else "No"


def format_list_as_bullets(items: list) -> str:
    """Format a list as bullet points."""
    if not items:
        return "-"
    return "\n".join([f"- {item}" for item in items])


def format_percentage(value: float) -> str:
    """Format percentage for display."""
    return f"{value:.1f}%"
