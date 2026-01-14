"""Floating action bar component for Organizations Explorer."""

import streamlit as st
from typing import List, Callable

from utils.session import select_all_rows, deselect_all_rows, get_selected_count


def render_floating_bar(
    current_page_ids: List[int],
    on_download_selected: Callable[[], None],
    on_delete_selected: Callable[[], None],
):
    """Render the floating multi-select action bar."""
    selected_count = get_selected_count()

    if selected_count == 0:
        return

    # Create a container with custom styling for the floating bar
    st.markdown(
        """
        <style>
        .floating-bar {
            position: fixed;
            top: 60px;
            left: 50%;
            transform: translateX(-50%);
            background-color: #1E88E5;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Render the floating bar content
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

    with col1:
        if st.button("Select All (Page)", key="select_all_btn"):
            select_all_rows(current_page_ids)
            st.rerun()

    with col2:
        if st.button("Deselect All", key="deselect_all_btn"):
            deselect_all_rows()
            st.rerun()

    with col3:
        st.markdown(f"**{selected_count} selected**")

    with col4:
        if st.button("Download PDF", key="download_selected_btn", type="primary"):
            on_download_selected()

    with col5:
        if st.button("Delete", key="delete_selected_btn"):
            on_delete_selected()


def render_delete_confirmation(
    org_name: str,
    on_confirm: Callable[[], None],
    on_cancel: Callable[[], None],
):
    """Render delete confirmation dialog."""
    st.warning(f"Are you sure you want to delete '{org_name}'?")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Delete", type="primary", key="confirm_delete"):
            on_confirm()
    with col2:
        if st.button("Cancel", key="cancel_delete"):
            on_cancel()


def render_multi_delete_confirmation(
    count: int,
    on_confirm: Callable[[], None],
    on_cancel: Callable[[], None],
):
    """Render multi-delete confirmation dialog."""
    st.warning(f"Are you sure you want to delete {count} records?")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Delete All", type="primary", key="confirm_multi_delete"):
            on_confirm()
    with col2:
        if st.button("Cancel", key="cancel_multi_delete"):
            on_cancel()
