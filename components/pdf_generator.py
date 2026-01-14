"""PDF generation component for Organizations Explorer."""

from io import BytesIO
from datetime import datetime
from typing import Dict, Any, List

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

from config import COUNTRIES


def create_styles():
    """Create custom paragraph styles."""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='OrgTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=6,
        textColor=colors.HexColor('#1565C0'),
    ))

    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading2'],
        fontSize=12,
        spaceBefore=12,
        spaceAfter=6,
        textColor=colors.HexColor('#1E88E5'),
    ))

    styles.add(ParagraphStyle(
        name='OrgBodyText',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=4,
    ))

    styles.add(ParagraphStyle(
        name='Label',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#757575'),
    ))

    styles.add(ParagraphStyle(
        name='OrgFooter',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#9E9E9E'),
    ))

    return styles


def safe_str(value) -> str:
    """Safely convert value to string."""
    if value is None:
        return "-"
    return str(value)


def generate_pdf(org: Dict[str, Any], country_code: str) -> BytesIO:
    """Generate PDF for a single organization."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1*cm,
        leftMargin=1*cm,
        topMargin=1*cm,
        bottomMargin=1*cm,
    )

    styles = create_styles()
    story = []

    # Title
    org_name = org.get('name_official') or org.get('name_short') or 'Unknown Organization'
    story.append(Paragraph(org_name, styles['OrgTitle']))

    # Short name if exists
    if org.get('name_short') and org.get('name_official'):
        story.append(Paragraph(f"Short Name: {org['name_short']}", styles['Label']))

    story.append(Spacer(1, 12))

    # Type, Scope, Founded line
    type_str = safe_str(org.get('type_primary'))
    scope_str = safe_str(org.get('organization_scope'))
    founded_str = safe_str(org.get('founding_year'))
    story.append(Paragraph(
        f"Type: {type_str} | Scope: {scope_str} | Founded: {founded_str}",
        styles['OrgBodyText']
    ))

    story.append(Spacer(1, 12))

    # Description
    story.append(Paragraph("DESCRIPTION", styles['SectionHeader']))
    description = org.get('description_en') or "No description available."
    story.append(Paragraph(description, styles['OrgBodyText']))

    story.append(Spacer(1, 12))

    # Contact and Key Person (two columns)
    contact_data = [
        ["CONTACT", "KEY PERSON"],
        [
            f"Email: {safe_str(org.get('email'))}",
            f"Name: {safe_str(org.get('contact_name'))}"
        ],
        [
            f"Phone: {safe_str(org.get('phone'))}",
            f"Position: {safe_str(org.get('contact_position'))}"
        ],
        [
            f"Fax: {safe_str(org.get('fax'))}",
            f"Email: {safe_str(org.get('contact_email'))}"
        ],
    ]

    # Build address
    address_parts = []
    if org.get('street'):
        address_parts.append(org['street'])
    city_parts = []
    if org.get('postal_code'):
        city_parts.append(org['postal_code'])
    if org.get('city'):
        city_parts.append(org['city'])
    if city_parts:
        address_parts.append(' '.join(city_parts))
    if org.get('country_name'):
        address_parts.append(org['country_name'])
    address = ', '.join(address_parts) if address_parts else '-'

    contact_data.append([f"Address: {address}", f"Phone: {safe_str(org.get('contact_phone'))}"])

    contact_table = Table(contact_data, colWidths=[9*cm, 9*cm])
    contact_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1E88E5')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(contact_table)

    story.append(Spacer(1, 12))

    # Disciplines and Research Areas
    tags = org.get('tags', {})
    related = org.get('related', {})

    disciplines = tags.get('disciplines', [])
    research_areas = related.get('research_areas', [])

    disciplines_str = '\n'.join([f"- {d}" for d in disciplines]) if disciplines else "-"
    research_str = '\n'.join([f"- {r}" for r in research_areas]) if research_areas else "-"

    academic_data = [
        ["DISCIPLINES", "RESEARCH AREAS"],
        [disciplines_str, research_str],
    ]

    academic_table = Table(academic_data, colWidths=[9*cm, 9*cm])
    academic_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1E88E5')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(academic_table)

    story.append(Spacer(1, 12))

    # Partners and Social Media
    partners = related.get('partners', [])
    partners_str = '\n'.join([f"- {p}" for p in partners]) if partners else "-"

    social_lines = []
    if org.get('twitter'):
        social_lines.append(f"Twitter: {org['twitter']}")
    if org.get('linkedin'):
        social_lines.append(f"LinkedIn: {org['linkedin']}")
    if org.get('facebook'):
        social_lines.append(f"Facebook: {org['facebook']}")
    if org.get('youtube'):
        social_lines.append(f"YouTube: {org['youtube']}")
    social_str = '\n'.join(social_lines) if social_lines else "-"

    network_data = [
        ["PARTNERS", "SOCIAL MEDIA"],
        [partners_str, social_str],
    ]

    network_table = Table(network_data, colWidths=[9*cm, 9*cm])
    network_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1E88E5')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(network_table)

    story.append(Spacer(1, 12))

    # Website
    story.append(Paragraph("WEBSITE", styles['SectionHeader']))
    url = org.get('url_original') or '-'
    story.append(Paragraph(url, styles['OrgBodyText']))

    story.append(Spacer(1, 24))

    # Footer
    country_name = COUNTRIES.get(country_code, {}).get('name', country_code)
    generated_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    footer_text = f"ID: {org.get('id', '-')} | Acquired from {country_code} - {country_name} database | Generated: {generated_date}"
    story.append(Paragraph(footer_text, styles['OrgFooter']))

    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_multi_pdf(organizations: List[Dict[str, Any]], country_code: str) -> BytesIO:
    """Generate PDF for multiple organizations with page breaks."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1*cm,
        leftMargin=1*cm,
        topMargin=1*cm,
        bottomMargin=1*cm,
    )

    styles = create_styles()
    story = []

    for i, org in enumerate(organizations):
        # Title
        org_name = org.get('name_official') or org.get('name_short') or 'Unknown Organization'
        story.append(Paragraph(org_name, styles['OrgTitle']))

        # Short name if exists
        if org.get('name_short') and org.get('name_official'):
            story.append(Paragraph(f"Short Name: {org['name_short']}", styles['Label']))

        story.append(Spacer(1, 12))

        # Type, Scope, Founded line
        type_str = safe_str(org.get('type_primary'))
        scope_str = safe_str(org.get('organization_scope'))
        founded_str = safe_str(org.get('founding_year'))
        story.append(Paragraph(
            f"Type: {type_str} | Scope: {scope_str} | Founded: {founded_str}",
            styles['OrgBodyText']
        ))

        story.append(Spacer(1, 12))

        # Description
        story.append(Paragraph("DESCRIPTION", styles['SectionHeader']))
        description = org.get('description_en') or "No description available."
        story.append(Paragraph(description, styles['OrgBodyText']))

        story.append(Spacer(1, 12))

        # Contact info
        story.append(Paragraph("CONTACT", styles['SectionHeader']))
        story.append(Paragraph(f"Email: {safe_str(org.get('email'))}", styles['OrgBodyText']))
        story.append(Paragraph(f"Phone: {safe_str(org.get('phone'))}", styles['OrgBodyText']))

        # Build address
        address_parts = []
        if org.get('street'):
            address_parts.append(org['street'])
        city_parts = []
        if org.get('postal_code'):
            city_parts.append(org['postal_code'])
        if org.get('city'):
            city_parts.append(org['city'])
        if city_parts:
            address_parts.append(' '.join(city_parts))
        if org.get('country_name'):
            address_parts.append(org['country_name'])
        address = ', '.join(address_parts) if address_parts else '-'
        story.append(Paragraph(f"Address: {address}", styles['OrgBodyText']))

        story.append(Spacer(1, 12))

        # Website
        story.append(Paragraph("WEBSITE", styles['SectionHeader']))
        url = org.get('url_original') or '-'
        story.append(Paragraph(url, styles['OrgBodyText']))

        story.append(Spacer(1, 24))

        # Footer
        country_name = COUNTRIES.get(country_code, {}).get('name', country_code)
        generated_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        footer_text = f"ID: {org.get('id', '-')} | Acquired from {country_code} - {country_name} database | Generated: {generated_date}"
        story.append(Paragraph(footer_text, styles['OrgFooter']))

        # Page break between organizations (except for the last one)
        if i < len(organizations) - 1:
            story.append(PageBreak())

    doc.build(story)
    buffer.seek(0)
    return buffer
