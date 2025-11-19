"""
Report generation routes
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from app.database import get_db
from app import models, auth

router = APIRouter()


@router.get("/generate-pdf")
async def generate_pdf_report(
    days: int = 30,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Generate PDF report"""
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    # Get analyses
    analyses = db.query(models.Analysis)\
        .filter(
            models.Analysis.user_id == current_user.id,
            models.Analysis.created_at >= cutoff_date
        )\
        .order_by(models.Analysis.created_at.desc())\
        .all()
    
    if not analyses:
        raise HTTPException(status_code=404, detail="No data found for report")
    
    # Calculate statistics
    total_analyses = len(analyses)
    avg_health = sum(a.plant_health_score or 0 for a in analyses) / total_analyses
    avg_water = sum(a.water_needs or 0 for a in analyses) / total_analyses
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2d5016'),
        spaceAfter=30,
        alignment=1  # Center
    )
    story.append(Paragraph("SmartFarm AI Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # User info
    story.append(Paragraph(f"<b>User:</b> {current_user.full_name or current_user.username}", styles['Normal']))
    story.append(Paragraph(f"<b>Report Period:</b> Last {days} days", styles['Normal']))
    story.append(Paragraph(f"<b>Generated:</b> {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Summary statistics
    story.append(Paragraph("<b>Summary Statistics</b>", styles['Heading2']))
    summary_data = [
        ['Metric', 'Value'],
        ['Total Analyses', str(total_analyses)],
        ['Average Plant Health', f"{avg_health:.2f}"],
        ['Average Water Needs (L/day)', f"{avg_water:.2f}"],
    ]
    
    summary_table = Table(summary_data, colWidths=[4*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a7c59')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Recent analyses
    story.append(Paragraph("<b>Recent Analyses</b>", styles['Heading2']))
    analysis_data = [['Date', 'Health Score', 'Water Needs', 'Soil Quality']]
    
    for analysis in analyses[:10]:  # Last 10
        date_str = analysis.created_at.strftime('%Y-%m-%d')
        health = f"{analysis.plant_health_score:.2f}" if analysis.plant_health_score else "N/A"
        water = f"{analysis.water_needs:.2f}L" if analysis.water_needs else "N/A"
        soil = analysis.soil_quality or "N/A"
        analysis_data.append([date_str, health, water, soil])
    
    analysis_table = Table(analysis_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    analysis_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a7c59')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9)
    ]))
    story.append(analysis_table)
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    return Response(
        content=buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=smartfarm_report_{datetime.utcnow().strftime('%Y%m%d')}.pdf"}
    )

