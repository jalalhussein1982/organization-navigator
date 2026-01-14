"""Filter bar component for Organizations Explorer."""

import streamlit as st
from typing import List

from utils.session import reset_filters


def render_filters(
    types: List[str],
    disciplines: List[str],
    cities: List[str],
):
    """Render the filter bar with search, type, discipline, and city filters."""

    # First row: Search and Type filter
    col1, col2, col3 = st.columns([2, 2, 2])

    with col1:
        search_term = st.text_input(
            "Search",
            value=st.session_state.search_term,
            placeholder="Search organizations...",
            key="search_input",
        )

    with col2:
        # Format type options for display
        type_options = [t.replace("_", " ").title() for t in types]
        type_map = {t.replace("_", " ").title(): t for t in types}

        selected_type_display = st.multiselect(
            "Type",
            options=type_options,
            default=[t.replace("_", " ").title() for t in st.session_state.filter_types if t in types],
            key="type_filter",
        )

    with col3:
        # Format discipline options for display
        discipline_options = [d.replace("_", " ").title() for d in disciplines]
        discipline_map = {d.replace("_", " ").title(): d for d in disciplines}

        selected_discipline_display = st.multiselect(
            "Discipline",
            options=discipline_options,
            default=[d.replace("_", " ").title() for d in st.session_state.filter_disciplines if d in disciplines],
            key="discipline_filter",
        )

    # Second row: City filter and buttons
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        selected_cities = st.multiselect(
            "City",
            options=cities,
            default=[c for c in st.session_state.filter_cities if c in cities],
            key="city_filter",
        )

    with col2:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        apply_clicked = st.button("Apply Filters", type="primary", use_container_width=True)

    with col3:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        clear_clicked = st.button("Clear All", use_container_width=True)

    # Handle apply
    if apply_clicked:
        st.session_state.search_term = search_term
        st.session_state.filter_types = [type_map[t] for t in selected_type_display]
        st.session_state.filter_disciplines = [discipline_map[d] for d in selected_discipline_display]
        st.session_state.filter_cities = selected_cities
        st.session_state.current_page = 1
        st.rerun()

    # Handle clear
    if clear_clicked:
        reset_filters()
        st.rerun()

    # Show active filters indicator
    active_filters = []
    if st.session_state.search_term:
        active_filters.append(f"Search: '{st.session_state.search_term}'")
    if st.session_state.filter_types:
        active_filters.append(f"Types: {len(st.session_state.filter_types)}")
    if st.session_state.filter_disciplines:
        active_filters.append(f"Disciplines: {len(st.session_state.filter_disciplines)}")
    if st.session_state.filter_cities:
        active_filters.append(f"Cities: {len(st.session_state.filter_cities)}")

    if active_filters:
        st.caption(f"Active filters: {', '.join(active_filters)}")
