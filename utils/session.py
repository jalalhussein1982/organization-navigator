"""Session state management for Organizations Explorer."""

import streamlit as st
from typing import Any, Dict, List, Optional

from config import DEFAULT_PER_PAGE


def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        "selected_country": None,
        "per_page": DEFAULT_PER_PAGE,
        "current_page": 1,
        "search_term": "",
        "filter_types": [],
        "filter_disciplines": [],
        "filter_cities": [],
        "sort_column": "name_official",
        "sort_direction": "asc",
        "selected_rows": set(),
        "expanded_row": None,
        "editing_row": None,
        "delete_confirm": None,
        "delete_multi_confirm": False,
        # Cache for filter options
        "cached_types": None,
        "cached_disciplines": None,
        "cached_cities": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_filters():
    """Reset all filters and search."""
    st.session_state.search_term = ""
    st.session_state.filter_types = []
    st.session_state.filter_disciplines = []
    st.session_state.filter_cities = []
    st.session_state.current_page = 1


def reset_all_state():
    """Reset all state except dark_mode (for country change)."""
    st.session_state.per_page = DEFAULT_PER_PAGE
    st.session_state.current_page = 1
    st.session_state.search_term = ""
    st.session_state.filter_types = []
    st.session_state.filter_disciplines = []
    st.session_state.filter_cities = []
    st.session_state.sort_column = "name_official"
    st.session_state.sort_direction = "asc"
    st.session_state.selected_rows = set()
    st.session_state.expanded_row = None
    st.session_state.editing_row = None
    st.session_state.delete_confirm = None
    st.session_state.delete_multi_confirm = False
    # Clear cache
    st.session_state.cached_types = None
    st.session_state.cached_disciplines = None
    st.session_state.cached_cities = None


def get_current_filters() -> Dict[str, Any]:
    """Get current filter values."""
    return {
        "search_term": st.session_state.search_term or None,
        "filter_types": st.session_state.filter_types or None,
        "filter_disciplines": st.session_state.filter_disciplines or None,
        "filter_cities": st.session_state.filter_cities or None,
    }


def set_sort(column: str):
    """Set sort column, toggle direction if same column."""
    if st.session_state.sort_column == column:
        st.session_state.sort_direction = (
            "desc" if st.session_state.sort_direction == "asc" else "asc"
        )
    else:
        st.session_state.sort_column = column
        st.session_state.sort_direction = "asc"


def toggle_row_selection(row_id: int):
    """Toggle selection state of a row."""
    if row_id in st.session_state.selected_rows:
        st.session_state.selected_rows.discard(row_id)
    else:
        st.session_state.selected_rows.add(row_id)


def select_all_rows(row_ids: List[int]):
    """Select all provided row IDs."""
    st.session_state.selected_rows = set(row_ids)


def deselect_all_rows():
    """Deselect all rows."""
    st.session_state.selected_rows = set()


def get_selected_count() -> int:
    """Get count of selected rows."""
    return len(st.session_state.selected_rows)


def has_selections() -> bool:
    """Check if any rows are selected."""
    return len(st.session_state.selected_rows) > 0


def set_expanded_row(row_id: Optional[int]):
    """Set the expanded row ID."""
    if st.session_state.expanded_row == row_id:
        st.session_state.expanded_row = None
    else:
        st.session_state.expanded_row = row_id


def set_editing_row(row_id: Optional[int]):
    """Set the row being edited."""
    st.session_state.editing_row = row_id


def set_delete_confirm(row_id: Optional[int]):
    """Set the row awaiting delete confirmation."""
    st.session_state.delete_confirm = row_id


def set_page(page: int):
    """Set current page."""
    st.session_state.current_page = page


def set_per_page(per_page: int):
    """Set items per page and reset to page 1."""
    st.session_state.per_page = per_page
    st.session_state.current_page = 1
