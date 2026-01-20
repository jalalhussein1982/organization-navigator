"""Header component for Organizations Explorer."""

import streamlit as st
from typing import Dict, Any

from config import get_available_databases
from utils.session import reset_all_state


def render_header(total_records: int = 0):
    """Render the header with title, country selector, and stats."""
    # Header row with title
    st.title("Organizations Explorer")

    # Country selector row
    available_dbs = get_available_databases()

    if not available_dbs:
        st.warning("No databases found. Please add database files (.db) to the 'db/' folder.")
        st.info("Files should be named with ISO country codes (e.g., NL.db, DE.db)")
        return False

    col1, col2 = st.columns([2, 2])

    with col1:
        # Create options for selectbox, sorted alphabetically by country name
        options = sorted(available_dbs.keys(), key=lambda code: available_dbs[code]['name'])
        display_options = [
            f"{available_dbs[code]['flag']} {available_dbs[code]['name']}"
            for code in options
        ]

        # Get current index
        current_index = 0
        if st.session_state.selected_country in options:
            current_index = options.index(st.session_state.selected_country)
        elif options:
            st.session_state.selected_country = options[0]

        selected_display = st.selectbox(
            "Select Country",
            options=display_options,
            index=current_index,
            key="country_selector",
            label_visibility="collapsed",
        )

        # Get the selected code
        if selected_display:
            selected_index = display_options.index(selected_display)
            new_country = options[selected_index]

            # Check if country changed
            if new_country != st.session_state.selected_country:
                st.session_state.selected_country = new_country
                reset_all_state()
                st.rerun()

    with col2:
        st.markdown(
            f"<div style='text-align: right; padding-top: 8px; font-size: 1.1em;'>"
            f"<strong>Total Records:</strong> {total_records:,}</div>",
            unsafe_allow_html=True
        )

    return True


def render_statistics(stats: Dict[str, Any]):
    """Render the collapsible statistics panel."""
    with st.expander("Statistics", expanded=False):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Top 5 Cities**")
            if stats.get("cities"):
                for city, count, percentage in stats["cities"]:
                    st.markdown(f"- {city}: {percentage:.1f}%")
            else:
                st.markdown("*No data*")

        with col2:
            st.markdown("**By Type**")
            if stats.get("types"):
                for type_name, count, percentage in stats["types"]:
                    display_name = type_name.replace("_", " ").title()
                    st.markdown(f"- {display_name}: {percentage:.1f}%")
            else:
                st.markdown("*No data*")

        with col3:
            st.markdown("**Top 5 Disciplines**")
            if stats.get("disciplines"):
                for discipline, count, percentage in stats["disciplines"]:
                    display_name = discipline.replace("_", " ").title()
                    st.markdown(f"- {display_name}: {percentage:.1f}%")
            else:
                st.markdown("*No data*")
