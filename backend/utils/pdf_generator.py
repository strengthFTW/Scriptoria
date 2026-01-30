from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io

def generate_pdf(data):
    """
    Generates a production script PDF from the provided data.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=inch, rightMargin=inch, topMargin=inch, bottomMargin=inch)
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        alignment=1, # Center
        spaceAfter=20,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Heading2'],
        fontSize=14,
        alignment=1, # Center
        spaceAfter=40,
        fontName='Helvetica-Oblique',
        textColor=colors.grey
    )
    
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=15,
        spaceAfter=10,
        color=colors.teal,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'SubheadingStyle',
        parent=styles['Heading3'],
        fontSize=12,
        spaceBefore=10,
        spaceAfter=5,
        fontName='Helvetica-Bold'
    )
    
    body_style = styles['BodyText']
    
    elements = []
    
    # TITLE PAGE
    elements.append(Spacer(1, 2 * inch))
    elements.append(Paragraph(data['screenplay'].get('title', 'Untitled Script').upper(), title_style))
    elements.append(Paragraph(f"GENRE: {data['screenplay'].get('genre', 'Unknown')}", subtitle_style))
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph(f"LOGLINE: {data['screenplay'].get('logline', 'No logline available.')}", body_style))
    elements.append(Spacer(1, 1 * inch))
    elements.append(Paragraph("SCRIPTORIA PRODUCTION PACKAGE", subtitle_style))
    elements.append(PageBreak())
    
    # CHARACTERS
    elements.append(Paragraph("CHARACTER PROFILES", heading_style))
    for char in data.get('characters', []):
        elements.append(Paragraph(char.get('name', 'Unknown'), subheading_style))
        elements.append(Paragraph(f"<b>ROLE:</b> {char.get('role', 'Unknown')}", body_style))
        elements.append(Paragraph(f"<b>ARC:</b> {char.get('arc', 'No arc description.')}", body_style))
        elements.append(Paragraph(f"<b>TRAITS:</b> {', '.join(char.get('traits', []))}", body_style))
        elements.append(Spacer(1, 15))
    elements.append(PageBreak())
    
    # SCREENPLAY OUTLINE
    elements.append(Paragraph("SCREENPLAY OUTLINE", heading_style))
    for act_key, act_data in data['screenplay'].get('threeActStructure', {}).items():
        elements.append(Paragraph(act_data.get('title', act_key.upper()), subheading_style))
        elements.append(Paragraph(act_data.get('description', ''), body_style))
        
        event_list = act_data.get('keyEvents', [])
        for event in event_list:
            elements.append(Paragraph(f"• {event}", body_style))
        elements.append(Spacer(1, 10))
    elements.append(PageBreak())
    
    # SCENE BREAKDOWN
    elements.append(Paragraph("SCENE BREAKDOWN", heading_style))
    for scene in data.get('scenes', []):
        elements.append(Paragraph(f"SCENE {scene.get('sceneNumber', '')}: {scene.get('location', '')} - {scene.get('timeOfDay', '')}", subheading_style))
        elements.append(Paragraph(f"<b>CHARACTERS:</b> {', '.join(scene.get('characters', []))}", body_style))
        elements.append(Paragraph(scene.get('action', ''), body_style))
        elements.append(Paragraph(f"<b>EST. DURATION:</b> {scene.get('duration', '2.5')} MIN", body_style))
        elements.append(Spacer(1, 15))
    elements.append(PageBreak())
    
    # SOUND DESIGN
    elements.append(Paragraph("SOUND DESIGN", heading_style))
    sound = data.get('soundDesign', {})
    if sound:
        music = sound.get('musicTheme', {})
        elements.append(Paragraph("MUSIC THEME", subheading_style))
        elements.append(Paragraph(f"<b>STYLE:</b> {music.get('style', 'Unknown')}", body_style))
        elements.append(Paragraph(f"<b>MOOD:</b> {music.get('mood', 'Unknown')}", body_style))
        elements.append(Paragraph(f"<b>INSTRUMENTS:</b> {', '.join(music.get('instruments', []))}", body_style))
        
        elements.append(Paragraph("AMBIENCE", subheading_style))
        for amb in sound.get('ambience', []):
            elements.append(Paragraph(f"• {amb.get('location', '')}: {amb.get('description', '')} ({amb.get('mood', '')})", body_style))
            
        elements.append(Paragraph("KEY SOUND MOMENTS", subheading_style))
        for moment in sound.get('keyMoments', []):
            elements.append(Paragraph(f"• SCN {moment.get('scene')}: {moment.get('moment')} - <i>{moment.get('soundDesign')}</i>", body_style))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
