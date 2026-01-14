"""Edit dialog component for Organizations Explorer."""

import streamlit as st
from typing import Dict, Any, List
import json

from config import get_available_databases, ORGANIZATION_TYPES, ORGANIZATION_SCOPES
from database import (
    get_full_organization_data,
    update_organization,
    update_organization_tags,
    update_organization_programs,
    update_organization_research_areas,
    update_organization_partners,
    update_organization_events,
)
from utils.session import set_editing_row
from utils.logger import log_edit, calculate_changes


def parse_tags_input(text: str) -> List[str]:
    """Parse comma-separated tags input."""
    if not text:
        return []
    return [t.strip() for t in text.split(",") if t.strip()]


def render_edit_dialog(org_id: int):
    """Render the edit dialog for an organization."""
    # Get database path
    available_dbs = get_available_databases()
    country_code = st.session_state.selected_country

    if country_code not in available_dbs:
        st.error("Database not found")
        return

    db_path = available_dbs[country_code]["path"]

    # Get full organization data
    org = get_full_organization_data(db_path, org_id)

    if not org:
        st.error("Organization not found")
        set_editing_row(None)
        return

    org_name = org.get("name_official") or org.get("name_short") or "Unknown"

    st.markdown(f"### Edit: {org_name}")

    # Create form
    with st.form(key=f"edit_form_{org_id}"):
        # Identity Section
        st.markdown("#### Identity")
        col1, col2 = st.columns(2)
        with col1:
            name_official = st.text_input("Official Name", value=org.get("name_official") or "")
            name_local = st.text_input("Local Name", value=org.get("name_local") or "")
            parent_organization = st.text_input("Parent Organization", value=org.get("parent_organization") or "")
        with col2:
            name_short = st.text_input("Short Name", value=org.get("name_short") or "")

            # Type dropdown
            type_options = [""] + ORGANIZATION_TYPES
            current_type = org.get("type_primary") or ""
            type_index = type_options.index(current_type) if current_type in type_options else 0
            type_primary = st.selectbox("Type (Primary)", options=type_options, index=type_index)

            type_secondary = st.text_input("Type (Secondary)", value=org.get("type_secondary") or "")

        col1, col2 = st.columns(2)
        with col1:
            # Scope dropdown
            scope_options = [""] + ORGANIZATION_SCOPES
            current_scope = org.get("organization_scope") or ""
            scope_index = scope_options.index(current_scope) if current_scope in scope_options else 0
            organization_scope = st.selectbox("Scope", options=scope_options, index=scope_index)
        with col2:
            founding_year = st.number_input(
                "Founding Year",
                min_value=1000,
                max_value=2100,
                value=org.get("founding_year") or 2000,
                step=1,
            )

        description_en = st.text_area("Description (English)", value=org.get("description_en") or "", height=100)
        description_local = st.text_area("Description (Local)", value=org.get("description_local") or "", height=100)

        st.markdown("---")

        # Contact Section
        st.markdown("#### Contact")
        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("Email", value=org.get("email") or "")
            email_press = st.text_input("Press Email", value=org.get("email_press") or "")
            email_careers = st.text_input("Careers Email", value=org.get("email_careers") or "")
            phone = st.text_input("Phone", value=org.get("phone") or "")
            fax = st.text_input("Fax", value=org.get("fax") or "")
        with col2:
            street = st.text_input("Street", value=org.get("street") or "")
            city = st.text_input("City", value=org.get("city") or "")
            postal_code = st.text_input("Postal Code", value=org.get("postal_code") or "")
            state_region = st.text_input("State/Region", value=org.get("state_region") or "")
            country_name = st.text_input("Country", value=org.get("country_name") or "")

        raw_address = st.text_area("Raw Address", value=org.get("raw_address") or "")
        contact_page_url = st.text_input("Contact Page URL", value=org.get("contact_page_url") or "")

        st.markdown("---")

        # Key Person Section
        st.markdown("#### Key Person")
        col1, col2 = st.columns(2)
        with col1:
            contact_name = st.text_input("Contact Name", value=org.get("contact_name") or "")
            contact_position = st.text_input("Position", value=org.get("contact_position") or "")
            contact_position_normalized = st.text_input("Position (Normalized)", value=org.get("contact_position_normalized") or "")
        with col2:
            contact_email = st.text_input("Contact Email", value=org.get("contact_email") or "")
            contact_phone = st.text_input("Contact Phone", value=org.get("contact_phone") or "")

        st.markdown("---")

        # Academic Section
        st.markdown("#### Academic")
        programs_str = ", ".join(org.get("related", {}).get("programs", []))
        programs_input = st.text_area("Programs (comma-separated)", value=programs_str)

        research_areas_str = ", ".join(org.get("related", {}).get("research_areas", []))
        research_areas_input = st.text_area("Research Areas (comma-separated)", value=research_areas_str)

        col1, col2 = st.columns(2)
        with col1:
            publications_page = st.text_input("Publications Page URL", value=org.get("publications_page") or "")
            student_count = st.number_input("Student Count", min_value=0, value=org.get("student_count") or 0)
        with col2:
            library_archive_url = st.text_input("Library/Archive URL", value=org.get("library_archive_url") or "")
            staff_count = st.number_input("Staff Count", min_value=0, value=org.get("staff_count") or 0)

        st.markdown("---")

        # Network Section
        st.markdown("#### Network")
        partners_str = ", ".join(org.get("related", {}).get("partners", []))
        partners_input = st.text_area("Partners (comma-separated)", value=partners_str)

        events_page_url = st.text_input("Events Page URL", value=org.get("events_page_url") or "")

        # Events table (simplified - as text for now)
        events = org.get("related", {}).get("events", [])
        events_json = json.dumps(events, indent=2) if events else "[]"
        events_input = st.text_area(
            "Events (JSON format: [{\"name\": \"\", \"type\": \"\", \"date\": \"\", \"recurring\": false}])",
            value=events_json,
            height=100,
        )

        st.markdown("---")

        # Tags Section
        st.markdown("#### Tags")
        tags = org.get("tags", {})

        disciplines_str = ", ".join(tags.get("disciplines", []))
        disciplines_input = st.text_area("Disciplines (comma-separated)", value=disciplines_str)

        themes_str = ", ".join(tags.get("themes", []))
        themes_input = st.text_area("Themes (comma-separated)", value=themes_str)

        geographic_str = ", ".join(tags.get("geographic", []))
        geographic_input = st.text_area("Geographic Focus (comma-separated)", value=geographic_str)

        audience_str = ", ".join(tags.get("audience", []))
        audience_input = st.text_area("Audience (comma-separated)", value=audience_str)

        content_types_str = ", ".join(tags.get("content_types", []))
        content_types_input = st.text_area("Content Types (comma-separated)", value=content_types_str)

        st.markdown("---")

        # Social Media Section
        st.markdown("#### Social Media")
        col1, col2 = st.columns(2)
        with col1:
            twitter = st.text_input("Twitter URL", value=org.get("twitter") or "")
            linkedin = st.text_input("LinkedIn URL", value=org.get("linkedin") or "")
        with col2:
            facebook = st.text_input("Facebook URL", value=org.get("facebook") or "")
            youtube = st.text_input("YouTube URL", value=org.get("youtube") or "")

        social_other = st.text_input("Other Social (JSON)", value=org.get("social_other") or "")

        st.markdown("---")

        # Geolocation Section
        st.markdown("#### Geolocation")
        col1, col2 = st.columns(2)
        with col1:
            latitude = st.number_input("Latitude", value=float(org.get("latitude") or 0), format="%.6f")
            geo_source = st.text_input("Geo Source", value=org.get("geo_source") or "")
        with col2:
            longitude = st.number_input("Longitude", value=float(org.get("longitude") or 0), format="%.6f")
            geo_confidence = st.number_input("Geo Confidence", value=float(org.get("geo_confidence") or 0), format="%.2f")

        st.markdown("---")

        # Technical Section (Read-only)
        st.markdown("#### Technical (Read-only)")
        st.info(f"""
        **URL Original:** {org.get('url_original') or '-'}
        **URL Resolved:** {org.get('url_resolved') or '-'}
        **SSL Valid:** {'Yes' if org.get('ssl_valid') else 'No'}
        **CMS Detected:** {org.get('cms_detected') or '-'}
        **Response Time:** {org.get('response_time_ms') or '-'} ms
        **Extracted At:** {org.get('extracted_at') or '-'}
        **Confidence Score:** {org.get('confidence_score') or '-'}
        """)

        st.markdown("---")

        # Form buttons
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Save Changes", type="primary", use_container_width=True)
        with col2:
            cancelled = st.form_submit_button("Cancel", use_container_width=True)

        if submitted:
            # Build update data
            update_data = {
                "name_official": name_official or None,
                "name_short": name_short or None,
                "name_local": name_local or None,
                "description_en": description_en or None,
                "description_local": description_local or None,
                "type_primary": type_primary or None,
                "type_secondary": type_secondary or None,
                "parent_organization": parent_organization or None,
                "founding_year": founding_year if founding_year else None,
                "organization_scope": organization_scope or None,
                "email": email or None,
                "email_press": email_press or None,
                "email_careers": email_careers or None,
                "phone": phone or None,
                "fax": fax or None,
                "street": street or None,
                "city": city or None,
                "postal_code": postal_code or None,
                "state_region": state_region or None,
                "country_name": country_name or None,
                "raw_address": raw_address or None,
                "contact_page_url": contact_page_url or None,
                "contact_name": contact_name or None,
                "contact_position": contact_position or None,
                "contact_position_normalized": contact_position_normalized or None,
                "contact_email": contact_email or None,
                "contact_phone": contact_phone or None,
                "publications_page": publications_page or None,
                "library_archive_url": library_archive_url or None,
                "student_count": student_count if student_count else None,
                "staff_count": staff_count if staff_count else None,
                "events_page_url": events_page_url or None,
                "twitter": twitter or None,
                "linkedin": linkedin or None,
                "facebook": facebook or None,
                "youtube": youtube or None,
                "social_other": social_other or None,
                "latitude": latitude if latitude else None,
                "longitude": longitude if longitude else None,
                "geo_source": geo_source or None,
                "geo_confidence": geo_confidence if geo_confidence else None,
            }

            try:
                # Update main record
                update_organization(db_path, org_id, update_data)

                # Update tags
                update_organization_tags(db_path, org_id, "disciplines", parse_tags_input(disciplines_input))
                update_organization_tags(db_path, org_id, "themes", parse_tags_input(themes_input))
                update_organization_tags(db_path, org_id, "geographic", parse_tags_input(geographic_input))
                update_organization_tags(db_path, org_id, "audience", parse_tags_input(audience_input))
                update_organization_tags(db_path, org_id, "content_types", parse_tags_input(content_types_input))

                # Update related data
                update_organization_programs(db_path, org_id, parse_tags_input(programs_input))
                update_organization_research_areas(db_path, org_id, parse_tags_input(research_areas_input))
                update_organization_partners(db_path, org_id, parse_tags_input(partners_input))

                # Parse and update events
                try:
                    events_list = json.loads(events_input) if events_input else []
                    update_organization_events(db_path, org_id, events_list)
                except json.JSONDecodeError:
                    st.warning("Invalid events JSON format. Events not updated.")

                # Get updated data for logging
                updated_org = get_full_organization_data(db_path, org_id)
                changes = calculate_changes(org, updated_org)

                # Log the edit
                log_edit(
                    country_code=country_code,
                    record_id=org_id,
                    organization_name=org_name,
                    full_record_before=org,
                    changes=changes,
                )

                st.success("Changes saved successfully!")
                set_editing_row(None)
                st.rerun()

            except Exception as e:
                st.error(f"Error saving changes: {str(e)}")

        if cancelled:
            set_editing_row(None)
            st.rerun()
