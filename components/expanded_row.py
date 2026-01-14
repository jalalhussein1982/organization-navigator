"""Expanded row component for Organizations Explorer."""

import streamlit as st

from config import get_available_databases
from database import get_full_organization_data
from utils.helpers import format_address, bool_to_yes_no


def render_expanded_row(org_id: int):
    """Render the expanded view for an organization."""
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
        return

    with st.container():
        st.markdown("---")

        # Identity Section
        st.markdown("#### Identity")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Official Name:** {org.get('name_official') or '-'}")
            st.markdown(f"**Local Name:** {org.get('name_local') or '-'}")
            st.markdown(f"**Parent Organization:** {org.get('parent_organization') or '-'}")
        with col2:
            st.markdown(f"**Short Name:** {org.get('name_short') or '-'}")
            type_str = f"{org.get('type_primary', '-')} | {org.get('type_secondary', '-')}"
            st.markdown(f"**Type:** {type_str}")
            st.markdown(f"**Scope:** {org.get('organization_scope') or '-'} | **Founded:** {org.get('founding_year') or '-'}")

        if org.get('description_en'):
            st.markdown(f"**Description (EN):** {org.get('description_en')}")
        if org.get('description_local'):
            st.markdown(f"**Description (Local):** {org.get('description_local')}")

        st.markdown("---")

        # Contact Section
        st.markdown("#### Contact")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Email:** {org.get('email') or '-'}")
            st.markdown(f"**Press Email:** {org.get('email_press') or '-'}")
            st.markdown(f"**Careers Email:** {org.get('email_careers') or '-'}")
            st.markdown(f"**Phone:** {org.get('phone') or '-'}")
            st.markdown(f"**Fax:** {org.get('fax') or '-'}")
        with col2:
            address = format_address(
                org.get('street'),
                org.get('postal_code'),
                org.get('city'),
                org.get('state_region'),
                org.get('country_name'),
            )
            st.markdown(f"**Address:** {address or '-'}")
            if org.get('raw_address'):
                st.markdown(f"**Raw Address:** {org.get('raw_address')}")
            if org.get('contact_page_url'):
                st.markdown(f"**Contact Page:** [{org.get('contact_page_url')}]({org.get('contact_page_url')})")

        st.markdown("---")

        # Key Person Section
        st.markdown("#### Key Person")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Name:** {org.get('contact_name') or '-'}")
            position = org.get('contact_position') or '-'
            normalized = org.get('contact_position_normalized')
            if normalized and normalized != position:
                position = f"{position} ({normalized})"
            st.markdown(f"**Position:** {position}")
        with col2:
            st.markdown(f"**Email:** {org.get('contact_email') or '-'}")
            st.markdown(f"**Phone:** {org.get('contact_phone') or '-'}")

        st.markdown("---")

        # Academic Section
        st.markdown("#### Academic")
        col1, col2 = st.columns(2)
        with col1:
            programs = org.get('related', {}).get('programs', [])
            if programs:
                st.markdown("**Programs:**")
                for prog in programs:
                    st.markdown(f"- {prog}")
            else:
                st.markdown("**Programs:** -")

            research_areas = org.get('related', {}).get('research_areas', [])
            if research_areas:
                st.markdown("**Research Areas:**")
                for area in research_areas:
                    st.markdown(f"- {area}")
            else:
                st.markdown("**Research Areas:** -")
        with col2:
            if org.get('publications_page'):
                st.markdown(f"**Publications:** [{org.get('publications_page')}]({org.get('publications_page')})")
            else:
                st.markdown("**Publications:** -")
            if org.get('library_archive_url'):
                st.markdown(f"**Library/Archive:** [{org.get('library_archive_url')}]({org.get('library_archive_url')})")
            else:
                st.markdown("**Library/Archive:** -")
            st.markdown(f"**Students:** {org.get('student_count') or '-'}")
            st.markdown(f"**Staff:** {org.get('staff_count') or '-'}")

        st.markdown("---")

        # Network Section
        st.markdown("#### Network")
        col1, col2 = st.columns(2)
        with col1:
            partners = org.get('related', {}).get('partners', [])
            if partners:
                st.markdown("**Partners:**")
                for partner in partners:
                    st.markdown(f"- {partner}")
            else:
                st.markdown("**Partners:** -")
        with col2:
            events = org.get('related', {}).get('events', [])
            if events:
                st.markdown("**Events:**")
                for event in events:
                    recurring = "Yes" if event.get('recurring') else "No"
                    st.markdown(f"- {event.get('name', '-')} ({event.get('type', '-')}) - {event.get('date', '-')} - Recurring: {recurring}")
            else:
                st.markdown("**Events:** -")
            if org.get('events_page_url'):
                st.markdown(f"**Events Page:** [{org.get('events_page_url')}]({org.get('events_page_url')})")

        st.markdown("---")

        # Tags Section
        st.markdown("#### Tags")
        tags = org.get('tags', {})
        col1, col2, col3 = st.columns(3)
        with col1:
            disciplines = tags.get('disciplines', [])
            st.markdown(f"**Disciplines:** {', '.join(disciplines) if disciplines else '-'}")
            themes = tags.get('themes', [])
            st.markdown(f"**Themes:** {', '.join(themes) if themes else '-'}")
        with col2:
            geographic = tags.get('geographic', [])
            st.markdown(f"**Geographic Focus:** {', '.join(geographic) if geographic else '-'}")
            audience = tags.get('audience', [])
            st.markdown(f"**Audience:** {', '.join(audience) if audience else '-'}")
        with col3:
            content_types = tags.get('content_types', [])
            st.markdown(f"**Content Types:** {', '.join(content_types) if content_types else '-'}")
            languages = org.get('related', {}).get('languages', [])
            st.markdown(f"**Languages:** {', '.join(languages) if languages else '-'}")

        st.markdown("---")

        # Social Media Section
        st.markdown("#### Social Media")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if org.get('twitter'):
                st.markdown(f"**Twitter:** [{org.get('twitter')}]({org.get('twitter')})")
            else:
                st.markdown("**Twitter:** -")
        with col2:
            if org.get('linkedin'):
                st.markdown(f"**LinkedIn:** [{org.get('linkedin')}]({org.get('linkedin')})")
            else:
                st.markdown("**LinkedIn:** -")
        with col3:
            if org.get('facebook'):
                st.markdown(f"**Facebook:** [{org.get('facebook')}]({org.get('facebook')})")
            else:
                st.markdown("**Facebook:** -")
        with col4:
            if org.get('youtube'):
                st.markdown(f"**YouTube:** [{org.get('youtube')}]({org.get('youtube')})")
            else:
                st.markdown("**YouTube:** -")

        if org.get('social_other'):
            st.markdown(f"**Other Social:** {org.get('social_other')}")

        st.markdown("---")

        # Geolocation Section
        st.markdown("#### Geolocation")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Latitude:** {org.get('latitude') or '-'}")
            st.markdown(f"**Longitude:** {org.get('longitude') or '-'}")
        with col2:
            st.markdown(f"**Source:** {org.get('geo_source') or '-'}")
            st.markdown(f"**Confidence:** {org.get('geo_confidence') or '-'}")

        st.markdown("---")

        # Technical Section
        st.markdown("#### Technical")
        col1, col2 = st.columns(2)
        with col1:
            if org.get('url_resolved'):
                st.markdown(f"**Resolved URL:** [{org.get('url_resolved')}]({org.get('url_resolved')})")
            else:
                st.markdown("**Resolved URL:** -")
            st.markdown(f"**SSL Valid:** {bool_to_yes_no(org.get('ssl_valid'))}")
            st.markdown(f"**CMS:** {org.get('cms_detected') or '-'}")
        with col2:
            st.markdown(f"**Response Time:** {org.get('response_time_ms') or '-'} ms")
            st.markdown(f"**Extracted At:** {org.get('extracted_at') or '-'}")
            st.markdown(f"**Confidence Score:** {org.get('confidence_score') or '-'}")

        st.markdown("---")
