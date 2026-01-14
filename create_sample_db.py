"""Script to create a sample database for testing."""

import sqlite3
import random
from pathlib import Path
from datetime import datetime, timedelta


def create_sample_database(db_path: str, num_records: int = 50):
    """Create a sample database with test data."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS websites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_original TEXT,
            url_resolved TEXT,
            extracted_at TEXT,
            status TEXT,
            confidence_score REAL,
            name_official TEXT,
            name_short TEXT,
            name_local TEXT,
            description_en TEXT,
            description_local TEXT,
            type_primary TEXT,
            type_secondary TEXT,
            parent_organization TEXT,
            founding_year INTEGER,
            phone TEXT,
            fax TEXT,
            email TEXT,
            email_press TEXT,
            email_careers TEXT,
            contact_page_url TEXT,
            street TEXT,
            city TEXT,
            postal_code TEXT,
            state_region TEXT,
            country_code TEXT,
            country_name TEXT,
            raw_address TEXT,
            latitude REAL,
            longitude REAL,
            geo_source TEXT,
            geo_confidence REAL,
            contact_name TEXT,
            contact_position TEXT,
            contact_position_normalized TEXT,
            contact_email TEXT,
            contact_phone TEXT,
            publications_page TEXT,
            library_archive_url TEXT,
            student_count INTEGER,
            staff_count INTEGER,
            events_page_url TEXT,
            twitter TEXT,
            linkedin TEXT,
            facebook TEXT,
            youtube TEXT,
            social_other TEXT,
            ssl_valid INTEGER,
            cms_detected TEXT,
            response_time_ms INTEGER,
            last_modified TEXT,
            organization_scope TEXT,
            created_at TEXT
        )
    """)

    # Create tag tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tag_disciplines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website_id INTEGER,
            discipline TEXT,
            FOREIGN KEY (website_id) REFERENCES websites(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tag_themes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website_id INTEGER,
            theme TEXT,
            FOREIGN KEY (website_id) REFERENCES websites(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tag_geographic (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website_id INTEGER,
            region TEXT,
            FOREIGN KEY (website_id) REFERENCES websites(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tag_audience (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website_id INTEGER,
            audience TEXT,
            FOREIGN KEY (website_id) REFERENCES websites(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tag_content_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website_id INTEGER,
            content_type TEXT,
            FOREIGN KEY (website_id) REFERENCES websites(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS programs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website_id INTEGER,
            program TEXT,
            FOREIGN KEY (website_id) REFERENCES websites(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS research_areas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website_id INTEGER,
            area TEXT,
            FOREIGN KEY (website_id) REFERENCES websites(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS partners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website_id INTEGER,
            partner_name TEXT,
            FOREIGN KEY (website_id) REFERENCES websites(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website_id INTEGER,
            name TEXT,
            type TEXT,
            date TEXT,
            recurring INTEGER,
            FOREIGN KEY (website_id) REFERENCES websites(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS focus_areas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website_id INTEGER,
            area TEXT,
            FOREIGN KEY (website_id) REFERENCES websites(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS website_languages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website_id INTEGER,
            language_code TEXT,
            FOREIGN KEY (website_id) REFERENCES websites(id)
        )
    """)

    # Sample data
    cities = ["Amsterdam", "Rotterdam", "The Hague", "Utrecht", "Eindhoven", "Groningen", "Tilburg", "Almere", "Breda", "Nijmegen"]
    types = ["university", "think_tank", "research_institute", "ngo", "foundation", "government_agency"]
    scopes = ["local", "national", "regional", "european", "international", "global"]
    disciplines = ["political_science", "economics", "law", "international_relations", "sociology", "public_policy", "history", "philosophy"]
    themes = ["eu_integration", "democracy", "climate_change", "migration", "security", "human_rights", "trade", "digital_transformation"]
    regions = ["europe", "netherlands", "eu", "western_europe", "global"]

    # Generate sample records
    for i in range(1, num_records + 1):
        city = random.choice(cities)
        org_type = random.choice(types)
        name_base = f"Sample Organization {i}"

        if org_type == "university":
            name_base = f"University of {city} {i}"
        elif org_type == "think_tank":
            name_base = f"{city} Institute for Policy Research {i}"
        elif org_type == "research_institute":
            name_base = f"{city} Research Center {i}"
        elif org_type == "ngo":
            name_base = f"{city} Foundation for Progress {i}"

        cursor.execute("""
            INSERT INTO websites (
                url_original, url_resolved, extracted_at, status, confidence_score,
                name_official, name_short, name_local, description_en, description_local,
                type_primary, type_secondary, parent_organization, founding_year,
                phone, fax, email, email_press, email_careers, contact_page_url,
                street, city, postal_code, state_region, country_code, country_name, raw_address,
                latitude, longitude, geo_source, geo_confidence,
                contact_name, contact_position, contact_position_normalized, contact_email, contact_phone,
                publications_page, library_archive_url, student_count, staff_count, events_page_url,
                twitter, linkedin, facebook, youtube, social_other,
                ssl_valid, cms_detected, response_time_ms, last_modified, organization_scope, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"https://example{i}.nl",
            f"https://www.example{i}.nl",
            datetime.now().isoformat(),
            "success",
            random.uniform(0.7, 1.0),
            name_base,
            f"ORG{i}",
            f"Organisatie {i}",
            f"This is a sample organization ({name_base}) focused on research and education in the Netherlands. It was established to promote excellence in academic and policy research.",
            f"Dit is een voorbeeldorganisatie ({name_base}) gericht op onderzoek en onderwijs in Nederland.",
            org_type,
            random.choice(["academic", "policy", "applied", None]),
            None if random.random() > 0.3 else f"Parent Org {random.randint(1, 10)}",
            random.randint(1900, 2020),
            f"+31 {random.randint(10, 99)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
            f"+31 {random.randint(10, 99)} {random.randint(100, 999)} {random.randint(1000, 9999)}" if random.random() > 0.5 else None,
            f"info@example{i}.nl",
            f"press@example{i}.nl" if random.random() > 0.5 else None,
            f"careers@example{i}.nl" if random.random() > 0.5 else None,
            f"https://example{i}.nl/contact",
            f"Street {random.randint(1, 200)}",
            city,
            f"{random.randint(1000, 9999)} AB",
            "North Holland" if city in ["Amsterdam", "Almere"] else "South Holland" if city in ["Rotterdam", "The Hague"] else None,
            "NL",
            "Netherlands",
            f"Street {random.randint(1, 200)}, {random.randint(1000, 9999)} AB {city}, Netherlands",
            52.0 + random.uniform(-0.5, 0.5),
            4.5 + random.uniform(-0.5, 0.5),
            "nominatim",
            random.uniform(0.8, 1.0),
            f"John Doe {i}",
            random.choice(["Director", "President", "CEO", "Dean", "Chair"]),
            random.choice(["director", "president", "ceo", "dean", "chair"]),
            f"contact{i}@example{i}.nl",
            f"+31 {random.randint(10, 99)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
            f"https://example{i}.nl/publications" if random.random() > 0.3 else None,
            f"https://example{i}.nl/library" if random.random() > 0.5 else None,
            random.randint(100, 50000) if org_type == "university" else None,
            random.randint(10, 5000),
            f"https://example{i}.nl/events" if random.random() > 0.4 else None,
            f"https://twitter.com/example{i}" if random.random() > 0.3 else None,
            f"https://linkedin.com/company/example{i}" if random.random() > 0.3 else None,
            f"https://facebook.com/example{i}" if random.random() > 0.5 else None,
            f"https://youtube.com/example{i}" if random.random() > 0.6 else None,
            None,
            1,
            random.choice(["WordPress", "Drupal", "Custom", None]),
            random.randint(50, 2000),
            datetime.now().isoformat(),
            random.choice(scopes),
            datetime.now().isoformat(),
        ))

        website_id = cursor.lastrowid

        # Add disciplines
        for _ in range(random.randint(1, 4)):
            cursor.execute(
                "INSERT INTO tag_disciplines (website_id, discipline) VALUES (?, ?)",
                (website_id, random.choice(disciplines))
            )

        # Add themes
        for _ in range(random.randint(1, 3)):
            cursor.execute(
                "INSERT INTO tag_themes (website_id, theme) VALUES (?, ?)",
                (website_id, random.choice(themes))
            )

        # Add geographic focus
        for _ in range(random.randint(1, 2)):
            cursor.execute(
                "INSERT INTO tag_geographic (website_id, region) VALUES (?, ?)",
                (website_id, random.choice(regions))
            )

        # Add programs (for universities)
        if org_type == "university":
            programs = ["BA Political Science", "MA International Relations", "PhD Economics", "BA Law", "MA European Studies"]
            for prog in random.sample(programs, random.randint(2, 4)):
                cursor.execute(
                    "INSERT INTO programs (website_id, program) VALUES (?, ?)",
                    (website_id, prog)
                )

        # Add research areas
        areas = ["European Governance", "Climate Policy", "Migration Studies", "Digital Economy", "Security Studies"]
        for area in random.sample(areas, random.randint(1, 3)):
            cursor.execute(
                "INSERT INTO research_areas (website_id, area) VALUES (?, ?)",
                (website_id, area)
            )

        # Add partners
        partner_names = ["LSE", "Sciences Po", "Harvard Kennedy School", "Brookings", "RAND", "Chatham House"]
        for partner in random.sample(partner_names, random.randint(0, 3)):
            cursor.execute(
                "INSERT INTO partners (website_id, partner_name) VALUES (?, ?)",
                (website_id, partner)
            )

        # Add events
        if random.random() > 0.5:
            event_types = ["conference", "seminar", "workshop", "lecture"]
            for _ in range(random.randint(1, 3)):
                event_date = (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d")
                cursor.execute(
                    "INSERT INTO events (website_id, name, type, date, recurring) VALUES (?, ?, ?, ?, ?)",
                    (website_id, f"Annual Event {random.randint(1, 10)}", random.choice(event_types), event_date, random.randint(0, 1))
                )

        # Add languages
        languages = ["en", "nl", "de", "fr"]
        for lang in random.sample(languages, random.randint(1, 3)):
            cursor.execute(
                "INSERT INTO website_languages (website_id, language_code) VALUES (?, ?)",
                (website_id, lang)
            )

    conn.commit()
    conn.close()
    print(f"Created sample database with {num_records} records at {db_path}")


if __name__ == "__main__":
    # Create db folder if it doesn't exist
    db_folder = Path(__file__).parent / "db"
    db_folder.mkdir(exist_ok=True)

    # Create sample NL database
    db_path = db_folder / "NL.db"
    create_sample_database(str(db_path), num_records=100)

    print("Sample database created successfully!")
    print(f"Database location: {db_path}")
    print("\nTo run the application:")
    print("  cd organizations_explorer")
    print("  streamlit run app.py")
