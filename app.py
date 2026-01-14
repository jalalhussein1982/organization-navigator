"""Organizations Explorer - Main Streamlit Application."""

import streamlit as st
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Organizations Explorer",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🏛️</text></svg>",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from config import get_available_databases, DARK_THEME
from database import (
    get_total_records,
    get_statistics,
    get_distinct_types,
    get_distinct_disciplines,
    get_distinct_cities,
    get_organizations,
    get_filtered_count,
    get_full_organization_data,
    get_organization_by_id,
    delete_organization,
    delete_organizations,
)
from components.header import render_header, render_statistics
from components.filters import render_filters
from components.data_table import render_data_table
from components.edit_dialog import render_edit_dialog
from components.floating_bar import (
    render_floating_bar,
    render_delete_confirmation,
    render_multi_delete_confirmation,
)
from components.pdf_generator import generate_pdf, generate_multi_pdf
from utils.session import (
    init_session_state,
    get_current_filters,
    deselect_all_rows,
    set_delete_confirm,
    set_editing_row,
)
from utils.logger import log_delete, log_delete_batch


def inject_custom_css():
    """Inject custom CSS for styling."""
    theme = DARK_THEME

    css = f"""
    <style>
        /* Root background - applied for both light and dark modes */
        .stApp {{
            background-color: {theme['background']} !important;
        }}

        /* Main content area */
        .main {{
            background-color: {theme['background']} !important;
        }}

        /* Main container */
        .main .block-container {{
            padding-top: 2rem;
            max-width: 1400px;
            background-color: {theme['background']} !important;
        }}

        /* Header styling */
        h1 {{
            color: {theme['primary_dark']} !important;
        }}

        /* All text elements */
        .stApp p, .stApp span, .stApp div, .stApp label {{
            color: {theme['text_primary']};
        }}

        /* Headers */
        .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {{
            color: {theme['text_primary']} !important;
        }}

        /* Markdown text */
        .stMarkdown {{
            font-size: 0.9rem;
            color: {theme['text_primary']};
        }}

        .stMarkdown p {{
            color: {theme['text_primary']} !important;
        }}

        /* Divider styling */
        hr {{
            margin: 0.5rem 0;
            border-color: {theme['border']} !important;
        }}

        /* Selection bar */
        .selection-bar {{
            background-color: {theme['primary']};
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            margin-bottom: 1rem;
        }}

        /* Expanded row */
        .expanded-row {{
            background-color: {theme['background_secondary']};
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
        }}

        /* Input fields */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stTextArea > div > div > textarea {{
            background-color: {theme['background_secondary']} !important;
            color: {theme['text_primary']} !important;
            border-color: {theme['border']} !important;
        }}

        /* Selectbox */
        .stSelectbox > div > div {{
            background-color: {theme['background_secondary']} !important;
            color: {theme['text_primary']} !important;
        }}

        .stSelectbox [data-baseweb="select"] {{
            background-color: {theme['background_secondary']} !important;
        }}

        .stSelectbox [data-baseweb="select"] > div {{
            background-color: {theme['background_secondary']} !important;
            border-color: {theme['border']} !important;
            color: {theme['text_primary']} !important;
        }}

        /* Multiselect */
        .stMultiSelect > div > div {{
            background-color: {theme['background_secondary']} !important;
            color: {theme['text_primary']} !important;
        }}

        .stMultiSelect [data-baseweb="select"] {{
            background-color: {theme['background_secondary']} !important;
        }}

        .stMultiSelect [data-baseweb="select"] > div {{
            background-color: {theme['background_secondary']} !important;
            border-color: {theme['border']} !important;
            color: {theme['text_primary']} !important;
        }}

        /* Expander */
        .streamlit-expanderHeader {{
            background-color: {theme['background_secondary']} !important;
            color: {theme['text_primary']} !important;
        }}

        .streamlit-expanderContent {{
            background-color: {theme['background_secondary']} !important;
            border-color: {theme['border']} !important;
        }}

        [data-testid="stExpander"] {{
            background-color: {theme['background_secondary']} !important;
            border-color: {theme['border']} !important;
        }}

        [data-testid="stExpander"] details {{
            background-color: {theme['background_secondary']} !important;
        }}

        [data-testid="stExpander"] summary {{
            color: {theme['text_primary']} !important;
        }}

        [data-testid="stExpander"] summary span {{
            color: {theme['text_primary']} !important;
        }}

        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {theme['background_secondary']} !important;
        }}

        [data-testid="stSidebar"] .stMarkdown {{
            color: {theme['text_primary']} !important;
        }}

        /* Buttons */
        .stButton > button {{
            border-radius: 4px;
            background-color: {theme['background_secondary']} !important;
            color: {theme['text_primary']} !important;
            border-color: {theme['border']} !important;
        }}

        .stButton > button:hover {{
            background-color: {theme['border']} !important;
            border-color: {theme['primary']} !important;
        }}

        /* Download button */
        .stDownloadButton > button {{
            background-color: {theme['background_secondary']} !important;
            color: {theme['text_primary']} !important;
            border-color: {theme['border']} !important;
        }}

        /* Checkbox */
        .stCheckbox > label {{
            color: {theme['text_primary']} !important;
        }}

        /* Metric */
        [data-testid="stMetricValue"] {{
            color: {theme['text_primary']} !important;
        }}

        [data-testid="stMetricLabel"] {{
            color: {theme['text_secondary']} !important;
        }}

        /* Info/Warning/Error/Success boxes */
        .stAlert {{
            background-color: {theme['background_secondary']} !important;
        }}

        /* Dataframe/Table */
        .stDataFrame {{
            background-color: {theme['background_secondary']} !important;
        }}

        [data-testid="stDataFrame"] {{
            background-color: {theme['background_secondary']} !important;
        }}

        /* Popover/Dropdown menus */
        [data-baseweb="popover"] {{
            background-color: {theme['background_secondary']} !important;
        }}

        [data-baseweb="menu"] {{
            background-color: {theme['background_secondary']} !important;
        }}

        [data-baseweb="menu"] li {{
            color: {theme['text_primary']} !important;
        }}

        /* Form submit button */
        .stFormSubmitButton > button {{
            background-color: {theme['primary']} !important;
            color: white !important;
        }}

        /* Header container */
        [data-testid="stHeader"] {{
            background-color: {theme['background']} !important;
        }}

        /* Bottom container */
        [data-testid="stBottom"] {{
            background-color: {theme['background']} !important;
        }}

        /* App view container */
        .appview-container {{
            background-color: {theme['background']} !important;
        }}

        /* Block container */
        [data-testid="stAppViewBlockContainer"] {{
            background-color: {theme['background']} !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def handle_single_download(org_id: int):
    """Handle single organization PDF download."""
    available_dbs = get_available_databases()
    country_code = st.session_state.selected_country

    if country_code not in available_dbs:
        st.error("Database not found")
        return

    db_path = available_dbs[country_code]["path"]
    org = get_full_organization_data(db_path, org_id)

    if not org:
        st.error("Organization not found")
        return

    pdf_buffer = generate_pdf(org, country_code)
    org_name = org.get("name_official") or org.get("name_short") or "organization"
    filename = f"{org_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    st.download_button(
        label="Download PDF",
        data=pdf_buffer,
        file_name=filename,
        mime="application/pdf",
        key=f"download_pdf_{org_id}_{datetime.now().timestamp()}",
    )


def handle_multi_download():
    """Handle multi-organization PDF download."""
    available_dbs = get_available_databases()
    country_code = st.session_state.selected_country

    if country_code not in available_dbs:
        st.error("Database not found")
        return

    db_path = available_dbs[country_code]["path"]
    selected_ids = list(st.session_state.selected_rows)

    if not selected_ids:
        st.warning("No organizations selected")
        return

    organizations = []
    for org_id in selected_ids:
        org = get_full_organization_data(db_path, org_id)
        if org:
            organizations.append(org)

    if not organizations:
        st.error("No organizations found")
        return

    pdf_buffer = generate_multi_pdf(organizations, country_code)
    filename = f"organizations_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    st.download_button(
        label="Download Selected as PDF",
        data=pdf_buffer,
        file_name=filename,
        mime="application/pdf",
        key=f"download_multi_pdf_{datetime.now().timestamp()}",
    )


def handle_single_delete(org_id: int):
    """Handle single organization deletion."""
    available_dbs = get_available_databases()
    country_code = st.session_state.selected_country

    if country_code not in available_dbs:
        st.error("Database not found")
        return

    db_path = available_dbs[country_code]["path"]
    org = get_full_organization_data(db_path, org_id)

    if not org:
        st.error("Organization not found")
        return

    org_name = org.get("name_official") or org.get("name_short") or "Unknown"

    # Log the deletion
    log_delete(
        country_code=country_code,
        record_id=org_id,
        organization_name=org_name,
        full_record=org,
    )

    # Delete from database
    delete_organization(db_path, org_id)

    st.success(f"Deleted: {org_name}")
    set_delete_confirm(None)
    st.rerun()


def handle_multi_delete():
    """Handle multi-organization deletion."""
    available_dbs = get_available_databases()
    country_code = st.session_state.selected_country

    if country_code not in available_dbs:
        st.error("Database not found")
        return

    db_path = available_dbs[country_code]["path"]
    selected_ids = list(st.session_state.selected_rows)

    # Collect all records for batch logging
    records_to_log = []
    for org_id in selected_ids:
        org = get_full_organization_data(db_path, org_id)
        if org:
            org_name = org.get("name_official") or org.get("name_short") or "Unknown"
            records_to_log.append({
                "record_id": org_id,
                "organization_name": org_name,
                "full_record": org,
            })

    # Log all deletions in a single batch
    if records_to_log:
        log_delete_batch(country_code=country_code, records=records_to_log)

    delete_organizations(db_path, selected_ids)

    st.success(f"Deleted {len(selected_ids)} organizations")
    deselect_all_rows()
    st.session_state.delete_multi_confirm = False
    st.rerun()


def main():
    """Main application entry point."""
    # Initialize session state
    init_session_state()

    # Inject custom CSS
    inject_custom_css()

    # Get available databases
    available_dbs = get_available_databases()

    # Render header
    if not available_dbs:
        st.title("Organizations Explorer")
        st.warning("No databases found.")
        st.info("Please add database files (.db) to the 'db/' folder. Files should be named with ISO country codes (e.g., NL.db, DE.db)")
        return

    # Set default country if not set
    if st.session_state.selected_country is None or st.session_state.selected_country not in available_dbs:
        st.session_state.selected_country = list(available_dbs.keys())[0]

    country_code = st.session_state.selected_country
    db_path = available_dbs[country_code]["path"]

    # Get total records
    total_records = get_total_records(db_path)

    # Render header with country selector
    has_db = render_header(total_records)
    if not has_db:
        return

    # Get statistics
    stats = get_statistics(db_path)
    render_statistics(stats)

    st.divider()

    # Cache filter options
    if st.session_state.cached_types is None:
        st.session_state.cached_types = get_distinct_types(db_path)
    if st.session_state.cached_disciplines is None:
        st.session_state.cached_disciplines = get_distinct_disciplines(db_path)
    if st.session_state.cached_cities is None:
        st.session_state.cached_cities = get_distinct_cities(db_path)

    # Render filters
    render_filters(
        types=st.session_state.cached_types,
        disciplines=st.session_state.cached_disciplines,
        cities=st.session_state.cached_cities,
    )

    st.divider()

    # Check if editing
    if st.session_state.editing_row is not None:
        render_edit_dialog(st.session_state.editing_row)
        return

    # Check for delete confirmation
    if st.session_state.delete_confirm is not None:
        org_id = st.session_state.delete_confirm
        org = get_organization_by_id(db_path, org_id)
        if org:
            org_name = org.get("name_official") or org.get("name_short") or "Unknown"
            render_delete_confirmation(
                org_name=org_name,
                on_confirm=lambda: handle_single_delete(org_id),
                on_cancel=lambda: set_delete_confirm(None) or st.rerun(),
            )
            return

    # Check for multi-delete confirmation
    if st.session_state.delete_multi_confirm:
        count = len(st.session_state.selected_rows)
        render_multi_delete_confirmation(
            count=count,
            on_confirm=handle_multi_delete,
            on_cancel=lambda: setattr(st.session_state, 'delete_multi_confirm', False) or st.rerun(),
        )
        return

    # Get current filters
    filters = get_current_filters()

    # Get filtered count
    filtered_count = get_filtered_count(
        db_path,
        search_term=filters["search_term"],
        filter_types=filters["filter_types"],
        filter_disciplines=filters["filter_disciplines"],
        filter_cities=filters["filter_cities"],
    )

    # Get organizations for current page
    offset = (st.session_state.current_page - 1) * st.session_state.per_page
    organizations = get_organizations(
        db_path,
        search_term=filters["search_term"],
        filter_types=filters["filter_types"],
        filter_disciplines=filters["filter_disciplines"],
        filter_cities=filters["filter_cities"],
        sort_column=st.session_state.sort_column,
        sort_direction=st.session_state.sort_direction,
        limit=st.session_state.per_page,
        offset=offset,
    )

    # Get current page IDs for select all
    current_page_ids = [org["id"] for org in organizations]

    # Render floating bar if selections exist
    if st.session_state.selected_rows:
        render_floating_bar(
            current_page_ids=current_page_ids,
            on_download_selected=handle_multi_download,
            on_delete_selected=lambda: setattr(st.session_state, 'delete_multi_confirm', True) or st.rerun(),
        )

    # Render data table
    render_data_table(
        organizations=organizations,
        total_count=filtered_count,
        on_download=handle_single_download,
    )


if __name__ == "__main__":
    main()
