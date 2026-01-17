"""Data table component for Organizations Explorer."""

import streamlit as st
from typing import List, Dict, Any, Callable

from config import PER_PAGE_OPTIONS
from utils.helpers import truncate_text, format_url, format_city_country
from utils.session import (
    set_sort,
    toggle_row_selection,
    set_expanded_row,
    set_editing_row,
    set_delete_confirm,
    set_page,
    set_per_page,
)


def render_pagination(total_count: int, current_page: int, per_page: int):
    """Render pagination controls."""
    total_pages = max(1, (total_count + per_page - 1) // per_page)

    # Results counter
    start_idx = (current_page - 1) * per_page + 1
    end_idx = min(current_page * per_page, total_count)

    col1, col2, col3 = st.columns([2, 2, 2])

    with col1:
        if total_count > 0:
            st.markdown(f"Showing **{start_idx:,}-{end_idx:,}** of **{total_count:,}** results")
        else:
            st.markdown("No results found")

    with col2:
        # Per page selector
        per_page_cols = st.columns(len(PER_PAGE_OPTIONS))
        for i, option in enumerate(PER_PAGE_OPTIONS):
            with per_page_cols[i]:
                button_type = "primary" if per_page == option else "secondary"
                if st.button(str(option), key=f"per_page_{option}", type=button_type):
                    set_per_page(option)
                    st.rerun()

    with col3:
        # Page navigation
        if total_pages > 1:
            nav_cols = st.columns([1, 2, 1])

            with nav_cols[0]:
                if st.button("<", disabled=current_page <= 1, key="prev_page"):
                    set_page(current_page - 1)
                    st.rerun()

            with nav_cols[1]:
                # Page number input
                new_page = st.number_input(
                    "Page",
                    min_value=1,
                    max_value=total_pages,
                    value=current_page,
                    key="page_input",
                    label_visibility="collapsed",
                )
                if new_page != current_page:
                    set_page(new_page)
                    st.rerun()
                st.caption(f"of {total_pages}")

            with nav_cols[2]:
                if st.button(">", disabled=current_page >= total_pages, key="next_page"):
                    set_page(current_page + 1)
                    st.rerun()


def render_sort_header(column: str, display_name: str, current_sort: str, sort_dir: str):
    """Render a sortable column header."""
    indicator = ""
    if current_sort == column:
        indicator = " ^" if sort_dir == "asc" else " v"

    if st.button(f"{display_name}{indicator}", key=f"sort_{column}", use_container_width=True):
        set_sort(column)
        st.rerun()


def render_data_table(
    organizations: List[Dict[str, Any]],
    total_count: int,
    on_download: Callable[[int], None],
):
    """Render the main data table."""
    current_page = st.session_state.current_page
    per_page = st.session_state.per_page
    sort_column = st.session_state.sort_column
    sort_direction = st.session_state.sort_direction
    selected_rows = st.session_state.selected_rows
    expanded_row = st.session_state.expanded_row

    if not organizations:
        st.info("No organizations found matching your criteria.")
        if st.button("Clear All Filters"):
            from utils.session import reset_filters
            reset_filters()
            st.rerun()
        return

    # Table header
    header_cols = st.columns([0.5, 2.5, 1.5, 1, 2, 1.5, 1.5])

    with header_cols[0]:
        st.button("Sel", key="header_sel", use_container_width=True, disabled=True)
    with header_cols[1]:
        render_sort_header("name_official", "Name", sort_column, sort_direction)
    with header_cols[2]:
        render_sort_header("city", "City & Country", sort_column, sort_direction)
    with header_cols[3]:
        render_sort_header("type_primary", "Type", sort_column, sort_direction)
    with header_cols[4]:
        st.button("Description", key="header_desc", use_container_width=True, disabled=True)
    with header_cols[5]:
        st.button("Website", key="header_website", use_container_width=True, disabled=True)
    with header_cols[6]:
        st.button("Actions", key="header_actions", use_container_width=True, disabled=True)

    st.divider()

    # Table rows
    for org in organizations:
        org_id = org["id"]
        is_selected = org_id in selected_rows
        is_expanded = expanded_row == org_id

        # Main row
        row_cols = st.columns([0.5, 2.5, 1.5, 1, 2, 1.5, 1.5])

        with row_cols[0]:
            if st.checkbox("", value=is_selected, key=f"select_{org_id}", label_visibility="collapsed"):
                if not is_selected:
                    toggle_row_selection(org_id)
                    st.rerun()
            elif is_selected:
                toggle_row_selection(org_id)
                st.rerun()

        with row_cols[1]:
            name = org.get("name_official") or org.get("name_short") or "-"
            st.markdown(f"**{name}**")

        with row_cols[2]:
            city_country = format_city_country(org.get("city"), org.get("country_name"))
            st.markdown(truncate_text(city_country, 25))

        with row_cols[3]:
            type_primary = org.get("type_primary") or "-"
            st.markdown(type_primary.replace("_", " ").title()[:15])

        with row_cols[4]:
            description = org.get("description_en") or "-"
            st.markdown(truncate_text(description, 150))

        with row_cols[5]:
            url = org.get("url_original")
            if url:
                display_url = format_url(url, 20)
                st.markdown(f"[{display_url}]({url})")
            else:
                st.markdown("-")

        with row_cols[6]:
            if st.button("Edit", key=f"edit_{org_id}", help="Edit organization", use_container_width=True):
                set_editing_row(org_id)
                st.rerun()
            if st.button("Delete", key=f"delete_{org_id}", help="Delete organization", use_container_width=True):
                set_delete_confirm(org_id)
                st.rerun()
            if st.button("PDF", key=f"download_{org_id}", help="Download as PDF", use_container_width=True):
                on_download(org_id)
            expand_label = "Less" if is_expanded else "More"
            if st.button(expand_label, key=f"expand_{org_id}", help="Show details", use_container_width=True):
                set_expanded_row(org_id)
                st.rerun()

        # Expanded row content
        if is_expanded:
            from components.expanded_row import render_expanded_row
            render_expanded_row(org_id)

        st.divider()

    # Pagination at bottom
    render_pagination(total_count, current_page, per_page)
