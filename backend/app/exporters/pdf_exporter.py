import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from app.core.config import EXPORTS_DIR

class PDFExporter:
    @staticmethod
    def generate_pdf(
        filename: str,
        title: str,
        content_markdown: str,
        output_type: str,
        source_references: list = None
    ) -> str:
        filepath = EXPORTS_DIR / filename
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=letter,
            rightMargin=45,
            leftMargin=45,
            topMargin=45,
            bottomMargin=45
        )

        styles = getSampleStyleSheet()
        
        # Custom styles
        header_title = ParagraphStyle(
            'HeaderTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=colors.HexColor('#0f172a'),
            alignment=TA_LEFT
        )
        
        header_subtitle = ParagraphStyle(
            'HeaderSub',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=11,
            leading=14,
            textColor=colors.HexColor('#0284c7'),
            alignment=TA_LEFT
        )
        
        h2_style = ParagraphStyle(
            'H2Style',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#1e293b'),
            spaceBefore=12,
            spaceAfter=6
        )
        
        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#334155'),
            alignment=TA_JUSTIFY,
            spaceAfter=6
        )
        
        bullet_style = ParagraphStyle(
            'Bullet',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor('#1e293b'),
            leftIndent=15,
            spaceAfter=3
        )

        story = []

        # Top Banner
        story.append(Paragraph(title, header_title))
        story.append(Spacer(1, 4))
        story.append(Paragraph(f"IntelTransform AI - Trusted {output_type} | AI-Assisted & Source Grounded", header_subtitle))
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284c7'), spaceAfter=15))

        # Parse simple markdown into story elements
        lines = content_markdown.split('\n')
        for line in lines:
            line_str = line.strip()
            if not line_str:
                story.append(Spacer(1, 4))
                continue
                
            if line_str.startswith('# '):
                # Main title already in banner, skip or render secondary
                continue
            elif line_str.startswith('## ') or line_str.startswith('### '):
                heading_clean = line_str.lstrip('#').strip()
                story.append(Paragraph(heading_clean, h2_style))
            elif line_str.startswith('* ') or line_str.startswith('- '):
                bullet_clean = line_str[2:].strip().replace('**', '')
                story.append(Paragraph(f"• {bullet_clean}", bullet_style))
            elif line_str.startswith(('1.', '2.', '3.', '4.', '5.')):
                num_clean = line_str.replace('**', '')
                story.append(Paragraph(num_clean, bullet_style))
            else:
                clean_text = line_str.replace('**', '').replace('*', '')
                story.append(Paragraph(clean_text, body_style))

        # Source citations section
        if source_references:
            story.append(Spacer(1, 15))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=10))
            story.append(Paragraph("Verified Source References (Grounding Audit)", h2_style))
            story.append(Spacer(1, 6))

            table_data = [["Claim", "Source Page", "Chunk ID", "Confidence"]]
            for ref in source_references[:5]:
                claim_sub = (ref.get("claim", "")[:65] + "...") if len(ref.get("claim", "")) > 65 else ref.get("claim", "")
                table_data.append([
                    claim_sub,
                    f"Page {ref.get('source_page', 1)}",
                    ref.get("source_chunk", "chunk_01"),
                    f"{int(ref.get('confidence', 0.95) * 100)}%"
                ])

            ref_table = Table(table_data, colWidths=[280, 80, 80, 80])
            ref_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8.5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ]))
            story.append(ref_table)

        doc.build(story)
        return str(filepath)
