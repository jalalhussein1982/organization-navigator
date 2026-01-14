"""Database operations for Organizations Explorer."""

import sqlite3
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Tuple


@contextmanager
def get_connection(db_path: str):
    """Context manager for database connections."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def get_total_records(db_path: str) -> int:
    """Get total number of records in the database."""
    with get_connection(db_path) as conn:
        cursor = conn.execute("SELECT COUNT(*) FROM websites")
        return cursor.fetchone()[0]


def get_statistics(db_path: str) -> Dict[str, List[Tuple[str, int, float]]]:
    """Get statistics for the database."""
    stats = {"cities": [], "types": [], "disciplines": []}

    with get_connection(db_path) as conn:
        # Top 5 cities
        cursor = conn.execute("""
            SELECT city, COUNT(*) as count,
                   ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM websites), 1) as percentage
            FROM websites
            WHERE city IS NOT NULL AND city != ''
            GROUP BY city
            ORDER BY count DESC
            LIMIT 5
        """)
        stats["cities"] = [(row["city"], row["count"], row["percentage"]) for row in cursor.fetchall()]

        # Type distribution
        cursor = conn.execute("""
            SELECT type_primary, COUNT(*) as count,
                   ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM websites), 1) as percentage
            FROM websites
            WHERE type_primary IS NOT NULL AND type_primary != ''
            GROUP BY type_primary
            ORDER BY count DESC
            LIMIT 5
        """)
        stats["types"] = [(row["type_primary"], row["count"], row["percentage"]) for row in cursor.fetchall()]

        # Top disciplines
        cursor = conn.execute("""
            SELECT discipline, COUNT(*) as count,
                   ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM tag_disciplines), 1) as percentage
            FROM tag_disciplines
            GROUP BY discipline
            ORDER BY count DESC
            LIMIT 5
        """)
        stats["disciplines"] = [(row["discipline"], row["count"], row["percentage"]) for row in cursor.fetchall()]

    return stats


def get_distinct_types(db_path: str) -> List[str]:
    """Get distinct organization types."""
    with get_connection(db_path) as conn:
        cursor = conn.execute("""
            SELECT DISTINCT type_primary
            FROM websites
            WHERE type_primary IS NOT NULL AND type_primary != ''
            ORDER BY type_primary
        """)
        return [row["type_primary"] for row in cursor.fetchall()]


def get_distinct_disciplines(db_path: str) -> List[str]:
    """Get distinct disciplines."""
    with get_connection(db_path) as conn:
        cursor = conn.execute("""
            SELECT DISTINCT discipline
            FROM tag_disciplines
            ORDER BY discipline
        """)
        return [row["discipline"] for row in cursor.fetchall()]


def get_distinct_cities(db_path: str) -> List[str]:
    """Get distinct cities."""
    with get_connection(db_path) as conn:
        cursor = conn.execute("""
            SELECT DISTINCT city
            FROM websites
            WHERE city IS NOT NULL AND city != ''
            ORDER BY city
        """)
        return [row["city"] for row in cursor.fetchall()]


def build_query(
    search_term: Optional[str] = None,
    filter_types: Optional[List[str]] = None,
    filter_disciplines: Optional[List[str]] = None,
    filter_cities: Optional[List[str]] = None,
    sort_column: str = "name_official",
    sort_direction: str = "asc",
    limit: int = 20,
    offset: int = 0,
    count_only: bool = False,
) -> Tuple[str, List[Any]]:
    """Build SQL query with filters."""
    params = []

    if count_only:
        select_clause = "SELECT COUNT(DISTINCT w.id)"
    else:
        select_clause = """
            SELECT DISTINCT w.id, w.name_official, w.name_short, w.city, w.country_name,
                   w.type_primary, w.description_en, w.url_original, w.email
        """

    from_clause = "FROM websites w"
    where_clauses = ["1=1"]

    # Search term filter
    if search_term:
        search_fields = [
            "w.name_official", "w.name_short", "w.name_local",
            "w.description_en", "w.description_local", "w.email",
            "w.url_original", "w.contact_name"
        ]
        search_conditions = " OR ".join([f"{field} LIKE ?" for field in search_fields])
        where_clauses.append(f"({search_conditions})")
        search_param = f"%{search_term}%"
        params.extend([search_param] * len(search_fields))

    # Type filter (OR within)
    if filter_types:
        placeholders = ", ".join(["?" for _ in filter_types])
        where_clauses.append(f"w.type_primary IN ({placeholders})")
        params.extend(filter_types)

    # City filter (OR within)
    if filter_cities:
        placeholders = ", ".join(["?" for _ in filter_cities])
        where_clauses.append(f"w.city IN ({placeholders})")
        params.extend(filter_cities)

    # Discipline filter (requires join)
    if filter_disciplines:
        placeholders = ", ".join(["?" for _ in filter_disciplines])
        where_clauses.append(f"""
            w.id IN (
                SELECT website_id FROM tag_disciplines
                WHERE discipline IN ({placeholders})
            )
        """)
        params.extend(filter_disciplines)

    where_clause = " AND ".join(where_clauses)
    query = f"{select_clause} {from_clause} WHERE {where_clause}"

    if not count_only:
        # Add ordering
        valid_columns = {
            "name_official": "w.name_official",
            "name_short": "w.name_short",
            "city": "w.city",
            "country_name": "w.country_name",
            "type_primary": "w.type_primary",
            "description_en": "w.description_en",
            "url_original": "w.url_original",
        }
        order_column = valid_columns.get(sort_column, "w.name_official")
        order_dir = "DESC" if sort_direction.lower() == "desc" else "ASC"
        query += f" ORDER BY {order_column} {order_dir}"

        # Add pagination
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])

    return query, params


def get_organizations(
    db_path: str,
    search_term: Optional[str] = None,
    filter_types: Optional[List[str]] = None,
    filter_disciplines: Optional[List[str]] = None,
    filter_cities: Optional[List[str]] = None,
    sort_column: str = "name_official",
    sort_direction: str = "asc",
    limit: int = 20,
    offset: int = 0,
) -> List[Dict[str, Any]]:
    """Get paginated list of organizations with filters."""
    query, params = build_query(
        search_term=search_term,
        filter_types=filter_types,
        filter_disciplines=filter_disciplines,
        filter_cities=filter_cities,
        sort_column=sort_column,
        sort_direction=sort_direction,
        limit=limit,
        offset=offset,
    )

    with get_connection(db_path) as conn:
        cursor = conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]


def get_filtered_count(
    db_path: str,
    search_term: Optional[str] = None,
    filter_types: Optional[List[str]] = None,
    filter_disciplines: Optional[List[str]] = None,
    filter_cities: Optional[List[str]] = None,
) -> int:
    """Get count of organizations matching filters."""
    query, params = build_query(
        search_term=search_term,
        filter_types=filter_types,
        filter_disciplines=filter_disciplines,
        filter_cities=filter_cities,
        count_only=True,
    )

    with get_connection(db_path) as conn:
        cursor = conn.execute(query, params)
        return cursor.fetchone()[0]


def get_organization_by_id(db_path: str, org_id: int) -> Optional[Dict[str, Any]]:
    """Get full organization record by ID."""
    with get_connection(db_path) as conn:
        cursor = conn.execute("SELECT * FROM websites WHERE id = ?", (org_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None


def get_organization_tags(db_path: str, org_id: int) -> Dict[str, List[str]]:
    """Get all tags for an organization."""
    tags = {
        "disciplines": [],
        "themes": [],
        "geographic": [],
        "audience": [],
        "content_types": [],
    }

    with get_connection(db_path) as conn:
        # Disciplines
        cursor = conn.execute("SELECT discipline FROM tag_disciplines WHERE website_id = ?", (org_id,))
        tags["disciplines"] = [row["discipline"] for row in cursor.fetchall()]

        # Themes
        cursor = conn.execute("SELECT theme FROM tag_themes WHERE website_id = ?", (org_id,))
        tags["themes"] = [row["theme"] for row in cursor.fetchall()]

        # Geographic
        cursor = conn.execute("SELECT region FROM tag_geographic WHERE website_id = ?", (org_id,))
        tags["geographic"] = [row["region"] for row in cursor.fetchall()]

        # Audience
        cursor = conn.execute("SELECT audience FROM tag_audience WHERE website_id = ?", (org_id,))
        tags["audience"] = [row["audience"] for row in cursor.fetchall()]

        # Content types
        cursor = conn.execute("SELECT content_type FROM tag_content_types WHERE website_id = ?", (org_id,))
        tags["content_types"] = [row["content_type"] for row in cursor.fetchall()]

    return tags


def get_organization_related_data(db_path: str, org_id: int) -> Dict[str, Any]:
    """Get all related data for an organization."""
    related = {
        "programs": [],
        "research_areas": [],
        "partners": [],
        "events": [],
        "focus_areas": [],
        "languages": [],
    }

    with get_connection(db_path) as conn:
        # Programs
        cursor = conn.execute("SELECT program FROM programs WHERE website_id = ?", (org_id,))
        related["programs"] = [row["program"] for row in cursor.fetchall()]

        # Research areas
        cursor = conn.execute("SELECT area FROM research_areas WHERE website_id = ?", (org_id,))
        related["research_areas"] = [row["area"] for row in cursor.fetchall()]

        # Partners
        cursor = conn.execute("SELECT partner_name FROM partners WHERE website_id = ?", (org_id,))
        related["partners"] = [row["partner_name"] for row in cursor.fetchall()]

        # Events
        cursor = conn.execute(
            "SELECT name, type, date, recurring FROM events WHERE website_id = ?",
            (org_id,)
        )
        related["events"] = [dict(row) for row in cursor.fetchall()]

        # Focus areas
        cursor = conn.execute("SELECT area FROM focus_areas WHERE website_id = ?", (org_id,))
        related["focus_areas"] = [row["area"] for row in cursor.fetchall()]

        # Languages
        cursor = conn.execute("SELECT language_code FROM website_languages WHERE website_id = ?", (org_id,))
        related["languages"] = [row["language_code"] for row in cursor.fetchall()]

    return related


def get_full_organization_data(db_path: str, org_id: int) -> Optional[Dict[str, Any]]:
    """Get complete organization data including tags and related data."""
    org = get_organization_by_id(db_path, org_id)
    if not org:
        return None

    org["tags"] = get_organization_tags(db_path, org_id)
    org["related"] = get_organization_related_data(db_path, org_id)
    return org


def update_organization(db_path: str, org_id: int, data: Dict[str, Any]) -> bool:
    """Update organization main record."""
    # Build update query dynamically
    fields = [
        "name_official", "name_short", "name_local", "description_en", "description_local",
        "type_primary", "type_secondary", "parent_organization", "founding_year",
        "phone", "fax", "email", "email_press", "email_careers", "contact_page_url",
        "street", "city", "postal_code", "state_region", "country_code", "country_name",
        "raw_address", "contact_name", "contact_position", "contact_position_normalized",
        "contact_email", "contact_phone", "publications_page", "library_archive_url",
        "student_count", "staff_count", "events_page_url", "twitter", "linkedin",
        "facebook", "youtube", "social_other", "latitude", "longitude", "geo_source",
        "geo_confidence", "organization_scope"
    ]

    update_fields = []
    params = []

    for field in fields:
        if field in data:
            update_fields.append(f"{field} = ?")
            params.append(data[field])

    if not update_fields:
        return True  # Nothing to update

    params.append(org_id)
    query = f"UPDATE websites SET {', '.join(update_fields)} WHERE id = ?"

    with get_connection(db_path) as conn:
        conn.execute(query, params)
        conn.commit()
        return True


def update_organization_tags(db_path: str, org_id: int, tag_type: str, values: List[str]):
    """Update organization tags."""
    table_map = {
        "disciplines": ("tag_disciplines", "discipline"),
        "themes": ("tag_themes", "theme"),
        "geographic": ("tag_geographic", "region"),
        "audience": ("tag_audience", "audience"),
        "content_types": ("tag_content_types", "content_type"),
    }

    if tag_type not in table_map:
        return

    table, column = table_map[tag_type]

    with get_connection(db_path) as conn:
        # Delete existing
        conn.execute(f"DELETE FROM {table} WHERE website_id = ?", (org_id,))

        # Insert new
        for value in values:
            if value:
                conn.execute(
                    f"INSERT INTO {table} (website_id, {column}) VALUES (?, ?)",
                    (org_id, value)
                )
        conn.commit()


def update_organization_programs(db_path: str, org_id: int, programs: List[str]):
    """Update organization programs."""
    with get_connection(db_path) as conn:
        conn.execute("DELETE FROM programs WHERE website_id = ?", (org_id,))
        for program in programs:
            if program:
                conn.execute(
                    "INSERT INTO programs (website_id, program) VALUES (?, ?)",
                    (org_id, program)
                )
        conn.commit()


def update_organization_research_areas(db_path: str, org_id: int, areas: List[str]):
    """Update organization research areas."""
    with get_connection(db_path) as conn:
        conn.execute("DELETE FROM research_areas WHERE website_id = ?", (org_id,))
        for area in areas:
            if area:
                conn.execute(
                    "INSERT INTO research_areas (website_id, area) VALUES (?, ?)",
                    (org_id, area)
                )
        conn.commit()


def update_organization_partners(db_path: str, org_id: int, partners: List[str]):
    """Update organization partners."""
    with get_connection(db_path) as conn:
        conn.execute("DELETE FROM partners WHERE website_id = ?", (org_id,))
        for partner in partners:
            if partner:
                conn.execute(
                    "INSERT INTO partners (website_id, partner_name) VALUES (?, ?)",
                    (org_id, partner)
                )
        conn.commit()


def update_organization_events(db_path: str, org_id: int, events: List[Dict[str, Any]]):
    """Update organization events."""
    with get_connection(db_path) as conn:
        conn.execute("DELETE FROM events WHERE website_id = ?", (org_id,))
        for event in events:
            if event.get("name"):
                conn.execute(
                    "INSERT INTO events (website_id, name, type, date, recurring) VALUES (?, ?, ?, ?, ?)",
                    (org_id, event.get("name"), event.get("type"), event.get("date"), event.get("recurring", 0))
                )
        conn.commit()


def delete_organization(db_path: str, org_id: int) -> bool:
    """Delete an organization and all related data."""
    with get_connection(db_path) as conn:
        # Delete from tag tables
        conn.execute("DELETE FROM tag_disciplines WHERE website_id = ?", (org_id,))
        conn.execute("DELETE FROM tag_themes WHERE website_id = ?", (org_id,))
        conn.execute("DELETE FROM tag_geographic WHERE website_id = ?", (org_id,))
        conn.execute("DELETE FROM tag_audience WHERE website_id = ?", (org_id,))
        conn.execute("DELETE FROM tag_content_types WHERE website_id = ?", (org_id,))

        # Delete from related tables
        conn.execute("DELETE FROM programs WHERE website_id = ?", (org_id,))
        conn.execute("DELETE FROM research_areas WHERE website_id = ?", (org_id,))
        conn.execute("DELETE FROM partners WHERE website_id = ?", (org_id,))
        conn.execute("DELETE FROM events WHERE website_id = ?", (org_id,))
        conn.execute("DELETE FROM focus_areas WHERE website_id = ?", (org_id,))
        conn.execute("DELETE FROM website_languages WHERE website_id = ?", (org_id,))

        # Delete main record
        conn.execute("DELETE FROM websites WHERE id = ?", (org_id,))
        conn.commit()
        return True


def delete_organizations(db_path: str, org_ids: List[int]) -> bool:
    """Delete multiple organizations."""
    for org_id in org_ids:
        delete_organization(db_path, org_id)
    return True
