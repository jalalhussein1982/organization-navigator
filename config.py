"""Configuration constants for Organizations Explorer."""

from pathlib import Path

# Country codes with names and flags
COUNTRIES = {
    "AF": {"name": "Afghanistan", "flag": "\U0001F1E6\U0001F1EB"},
    "AL": {"name": "Albania", "flag": "\U0001F1E6\U0001F1F1"},
    "DZ": {"name": "Algeria", "flag": "\U0001F1E9\U0001F1FF"},
    "AD": {"name": "Andorra", "flag": "\U0001F1E6\U0001F1E9"},
    "AO": {"name": "Angola", "flag": "\U0001F1E6\U0001F1F4"},
    "AR": {"name": "Argentina", "flag": "\U0001F1E6\U0001F1F7"},
    "AM": {"name": "Armenia", "flag": "\U0001F1E6\U0001F1F2"},
    "AU": {"name": "Australia", "flag": "\U0001F1E6\U0001F1FA"},
    "AT": {"name": "Austria", "flag": "\U0001F1E6\U0001F1F9"},
    "AZ": {"name": "Azerbaijan", "flag": "\U0001F1E6\U0001F1FF"},
    "BH": {"name": "Bahrain", "flag": "\U0001F1E7\U0001F1ED"},
    "BD": {"name": "Bangladesh", "flag": "\U0001F1E7\U0001F1E9"},
    "BY": {"name": "Belarus", "flag": "\U0001F1E7\U0001F1FE"},
    "BE": {"name": "Belgium", "flag": "\U0001F1E7\U0001F1EA"},
    "BA": {"name": "Bosnia and Herzegovina", "flag": "\U0001F1E7\U0001F1E6"},
    "BR": {"name": "Brazil", "flag": "\U0001F1E7\U0001F1F7"},
    "BG": {"name": "Bulgaria", "flag": "\U0001F1E7\U0001F1EC"},
    "CA": {"name": "Canada", "flag": "\U0001F1E8\U0001F1E6"},
    "CL": {"name": "Chile", "flag": "\U0001F1E8\U0001F1F1"},
    "CN": {"name": "China", "flag": "\U0001F1E8\U0001F1F3"},
    "CO": {"name": "Colombia", "flag": "\U0001F1E8\U0001F1F4"},
    "HR": {"name": "Croatia", "flag": "\U0001F1ED\U0001F1F7"},
    "CY": {"name": "Cyprus", "flag": "\U0001F1E8\U0001F1FE"},
    "CZ": {"name": "Czech Republic", "flag": "\U0001F1E8\U0001F1FF"},
    "DK": {"name": "Denmark", "flag": "\U0001F1E9\U0001F1F0"},
    "EG": {"name": "Egypt", "flag": "\U0001F1EA\U0001F1EC"},
    "EE": {"name": "Estonia", "flag": "\U0001F1EA\U0001F1EA"},
    "FI": {"name": "Finland", "flag": "\U0001F1EB\U0001F1EE"},
    "FR": {"name": "France", "flag": "\U0001F1EB\U0001F1F7"},
    "GE": {"name": "Georgia", "flag": "\U0001F1EC\U0001F1EA"},
    "DE": {"name": "Germany", "flag": "\U0001F1E9\U0001F1EA"},
    "GR": {"name": "Greece", "flag": "\U0001F1EC\U0001F1F7"},
    "HK": {"name": "Hong Kong", "flag": "\U0001F1ED\U0001F1F0"},
    "HU": {"name": "Hungary", "flag": "\U0001F1ED\U0001F1FA"},
    "IS": {"name": "Iceland", "flag": "\U0001F1EE\U0001F1F8"},
    "IN": {"name": "India", "flag": "\U0001F1EE\U0001F1F3"},
    "ID": {"name": "Indonesia", "flag": "\U0001F1EE\U0001F1E9"},
    "IR": {"name": "Iran", "flag": "\U0001F1EE\U0001F1F7"},
    "IQ": {"name": "Iraq", "flag": "\U0001F1EE\U0001F1F6"},
    "IE": {"name": "Ireland", "flag": "\U0001F1EE\U0001F1EA"},
    "IL": {"name": "Israel", "flag": "\U0001F1EE\U0001F1F1"},
    "IT": {"name": "Italy", "flag": "\U0001F1EE\U0001F1F9"},
    "JP": {"name": "Japan", "flag": "\U0001F1EF\U0001F1F5"},
    "JO": {"name": "Jordan", "flag": "\U0001F1EF\U0001F1F4"},
    "KZ": {"name": "Kazakhstan", "flag": "\U0001F1F0\U0001F1FF"},
    "KE": {"name": "Kenya", "flag": "\U0001F1F0\U0001F1EA"},
    "KW": {"name": "Kuwait", "flag": "\U0001F1F0\U0001F1FC"},
    "LV": {"name": "Latvia", "flag": "\U0001F1F1\U0001F1FB"},
    "LB": {"name": "Lebanon", "flag": "\U0001F1F1\U0001F1E7"},
    "LT": {"name": "Lithuania", "flag": "\U0001F1F1\U0001F1F9"},
    "LU": {"name": "Luxembourg", "flag": "\U0001F1F1\U0001F1FA"},
    "MY": {"name": "Malaysia", "flag": "\U0001F1F2\U0001F1FE"},
    "MT": {"name": "Malta", "flag": "\U0001F1F2\U0001F1F9"},
    "MX": {"name": "Mexico", "flag": "\U0001F1F2\U0001F1FD"},
    "MD": {"name": "Moldova", "flag": "\U0001F1F2\U0001F1E9"},
    "MA": {"name": "Morocco", "flag": "\U0001F1F2\U0001F1E6"},
    "NL": {"name": "Netherlands", "flag": "\U0001F1F3\U0001F1F1"},
    "NZ": {"name": "New Zealand", "flag": "\U0001F1F3\U0001F1FF"},
    "NG": {"name": "Nigeria", "flag": "\U0001F1F3\U0001F1EC"},
    "NO": {"name": "Norway", "flag": "\U0001F1F3\U0001F1F4"},
    "OM": {"name": "Oman", "flag": "\U0001F1F4\U0001F1F2"},
    "PK": {"name": "Pakistan", "flag": "\U0001F1F5\U0001F1F0"},
    "PS": {"name": "Palestine", "flag": "\U0001F1F5\U0001F1F8"},
    "PE": {"name": "Peru", "flag": "\U0001F1F5\U0001F1EA"},
    "PH": {"name": "Philippines", "flag": "\U0001F1F5\U0001F1ED"},
    "PL": {"name": "Poland", "flag": "\U0001F1F5\U0001F1F1"},
    "PT": {"name": "Portugal", "flag": "\U0001F1F5\U0001F1F9"},
    "QA": {"name": "Qatar", "flag": "\U0001F1F6\U0001F1E6"},
    "RO": {"name": "Romania", "flag": "\U0001F1F7\U0001F1F4"},
    "RU": {"name": "Russia", "flag": "\U0001F1F7\U0001F1FA"},
    "SA": {"name": "Saudi Arabia", "flag": "\U0001F1F8\U0001F1E6"},
    "RS": {"name": "Serbia", "flag": "\U0001F1F7\U0001F1F8"},
    "SG": {"name": "Singapore", "flag": "\U0001F1F8\U0001F1EC"},
    "SK": {"name": "Slovakia", "flag": "\U0001F1F8\U0001F1F0"},
    "SI": {"name": "Slovenia", "flag": "\U0001F1F8\U0001F1EE"},
    "ZA": {"name": "South Africa", "flag": "\U0001F1FF\U0001F1E6"},
    "KR": {"name": "South Korea", "flag": "\U0001F1F0\U0001F1F7"},
    "ES": {"name": "Spain", "flag": "\U0001F1EA\U0001F1F8"},
    "SE": {"name": "Sweden", "flag": "\U0001F1F8\U0001F1EA"},
    "CH": {"name": "Switzerland", "flag": "\U0001F1E8\U0001F1ED"},
    "SY": {"name": "Syria", "flag": "\U0001F1F8\U0001F1FE"},
    "TW": {"name": "Taiwan", "flag": "\U0001F1F9\U0001F1FC"},
    "TH": {"name": "Thailand", "flag": "\U0001F1F9\U0001F1ED"},
    "TN": {"name": "Tunisia", "flag": "\U0001F1F9\U0001F1F3"},
    "TR": {"name": "Turkey", "flag": "\U0001F1F9\U0001F1F7"},
    "UA": {"name": "Ukraine", "flag": "\U0001F1FA\U0001F1E6"},
    "AE": {"name": "United Arab Emirates", "flag": "\U0001F1E6\U0001F1EA"},
    "GB": {"name": "United Kingdom", "flag": "\U0001F1EC\U0001F1E7"},
    "US": {"name": "United States", "flag": "\U0001F1FA\U0001F1F8"},
    "VN": {"name": "Vietnam", "flag": "\U0001F1FB\U0001F1F3"},
    "YE": {"name": "Yemen", "flag": "\U0001F1FE\U0001F1EA"},
}

# Light theme colors
LIGHT_THEME = {
    "primary": "#1E88E5",
    "primary_dark": "#1565C0",
    "primary_light": "#E3F2FD",
    "background": "#FFFFFF",
    "background_secondary": "#F5F9FF",
    "text_primary": "#212121",
    "text_secondary": "#757575",
    "border": "#E0E0E0",
    "success": "#4CAF50",
    "warning": "#FF9800",
    "error": "#F44336",
    "footer_gray": "#9E9E9E",
}

# Dark theme colors
DARK_THEME = {
    "primary": "#64B5F6",
    "primary_dark": "#1E88E5",
    "primary_light": "#1A237E",
    "background": "#121212",
    "background_secondary": "#1E1E1E",
    "text_primary": "#E0E0E0",
    "text_secondary": "#9E9E9E",
    "border": "#333333",
    "success": "#81C784",
    "warning": "#FFB74D",
    "error": "#E57373",
    "footer_gray": "#757575",
}

# Organization types
ORGANIZATION_TYPES = [
    "university",
    "think_tank",
    "research_institute",
    "ngo",
    "foundation",
    "government_agency",
    "international_organization",
    "professional_association",
    "media_outlet",
    "other",
]

# Organization scopes
ORGANIZATION_SCOPES = [
    "local",
    "national",
    "regional",
    "european",
    "international",
    "global",
]

# Default database folder
DB_FOLDER = Path(__file__).parent / "db"

# Logs folder
LOGS_FOLDER = Path(__file__).parent / "logs"

# Pagination options
PER_PAGE_OPTIONS = [10, 20, 50, 100]
DEFAULT_PER_PAGE = 20


def get_available_databases(db_folder=None):
    """Scan db folder for available database files."""
    if db_folder is None:
        db_folder = DB_FOLDER
    db_folder = Path(db_folder)

    available = {}
    if db_folder.exists():
        for file in db_folder.glob("*.db"):
            code = file.stem.upper()
            if code in COUNTRIES:
                available[code] = {
                    **COUNTRIES[code],
                    "path": str(file),
                }
    return available


def get_theme(dark_mode=False):
    """Get the appropriate theme based on dark mode setting."""
    return DARK_THEME if dark_mode else LIGHT_THEME
