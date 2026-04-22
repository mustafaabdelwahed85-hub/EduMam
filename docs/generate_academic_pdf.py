import re
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


BASE_DIR = Path(__file__).resolve().parent
SOURCE_FILE = BASE_DIR / "ACADEMIC_DOCUMENTATION.md"
OUTPUT_FILE = BASE_DIR / "Mamba_Academic_Documentation.pdf"

BRAND = {
    "navy": "#0f172a",
    "teal": "#0f766e",
    "forest": "#166534",
    "mint": "#d1fae5",
    "light": "#f8fafc",
    "slate": "#475569",
    "text": "#111827",
}


def normalize_inline_markdown(text: str) -> str:
    text = escape(text)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda match: f"{match.group(1)} ({match.group(2)})",
        text,
    )
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(
        r"`([^`]+)`",
        lambda match: f"<font name='Courier'>{match.group(1)}</font>",
        text,
    )
    return text


def build_styles():
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="CoverBrand",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#d1fae5"),
            alignment=TA_CENTER,
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="DocTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=26,
            leading=32,
            textColor=colors.HexColor("#ffffff"),
            alignment=TA_CENTER,
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverLead",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=12,
            leading=18,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#e2e8f0"),
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Meta",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#dbeafe"),
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=22,
            textColor=colors.HexColor(BRAND["navy"]),
            spaceBefore=0,
            spaceAfter=0,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubTitle",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=18,
            textColor=colors.HexColor(BRAND["forest"]),
            spaceBefore=10,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="MinorTitle",
            parent=styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11.5,
            leading=16,
            textColor=colors.HexColor(BRAND["teal"]),
            spaceBefore=8,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyTextCustom",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            spaceAfter=6,
            textColor=colors.HexColor(BRAND["text"]),
        )
    )
    styles.add(
        ParagraphStyle(
            name="BulletText",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            leftIndent=18,
            firstLineIndent=0,
            spaceAfter=4,
            textColor=colors.HexColor(BRAND["text"]),
        )
    )
    styles.add(
        ParagraphStyle(
            name="NumberedText",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            leftIndent=8,
            firstLineIndent=0,
            spaceAfter=4,
            textColor=colors.HexColor(BRAND["text"]),
        )
    )
    return styles


def build_cover_summary():
    summary = Table(
        [
            ["Architecture", "Database", "Deployment"],
            ["Flask Blueprints", "SQLite / PostgreSQL", "PythonAnywhere / Render"],
        ],
        colWidths=[5.2 * cm, 5.2 * cm, 5.2 * cm],
    )
    summary.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(BRAND["mint"])),
                ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#ffffff")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor(BRAND["navy"])),
                ("TEXTCOLOR", (0, 1), (-1, 1), colors.HexColor(BRAND["text"])),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, 1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#9fd8cc")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return summary


def build_section_banner(title, styles):
    banner = Table(
        [[Paragraph(normalize_inline_markdown(title), styles["SectionTitle"])]],
        colWidths=[16.8 * cm],
    )
    banner.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), colors.HexColor(BRAND["mint"])),
                ("LINEBEFORE", (0, 0), (0, 0), 4, colors.HexColor(BRAND["teal"])),
                ("BOX", (0, 0), (0, 0), 0.5, colors.HexColor("#b6e3db")),
                ("TOPPADDING", (0, 0), (0, 0), 6),
                ("BOTTOMPADDING", (0, 0), (0, 0), 6),
                ("LEFTPADDING", (0, 0), (0, 0), 10),
                ("RIGHTPADDING", (0, 0), (0, 0), 10),
            ]
        )
    )
    return banner


def build_cover_story(styles):
    story = []
    story.append(Spacer(1, 5.2 * cm))
    story.append(Paragraph("Mamba", styles["CoverBrand"]))
    story.append(Paragraph("Academic Project Documentation", styles["DocTitle"]))
    story.append(
        Paragraph(
            "Full-Stack Educational Platform Using Flask",
            styles["CoverLead"],
        )
    )
    story.append(
        Paragraph(
            "A complete university-style project report covering architecture, functionality, data design, implementation, and deployment.",
            styles["CoverLead"],
        )
    )
    story.append(Spacer(1, 0.45 * cm))
    story.append(build_cover_summary())
    story.append(Spacer(1, 0.7 * cm))
    story.append(
        Paragraph(
            f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            styles["Meta"],
        )
    )
    story.append(PageBreak())
    return story


def is_heading(line: str) -> bool:
    return bool(re.match(r"^#{1,4}\s+", line))


def is_bullet(line: str) -> bool:
    return line.startswith("- ")


def is_numbered(line: str) -> bool:
    return bool(re.match(r"^\d+\.\s+", line))


def parse_list(lines, start_index, numbered=False):
    items = []
    current = None
    index = start_index

    while index < len(lines):
        line = lines[index]

        if not line.strip():
            if current:
                items.append(current.strip())
                current = None
            break

        if numbered and is_numbered(line):
            if current:
                items.append(current.strip())
            current = line.strip()
            index += 1
            continue

        if not numbered and is_bullet(line):
            if current:
                items.append(current.strip())
            current = line[2:].strip()
            index += 1
            continue

        if is_heading(line) or (numbered and is_bullet(line)) or (not numbered and is_numbered(line)):
            break

        stripped = line.strip()
        if current is not None and stripped:
            current += " " + stripped
        index += 1

    if current:
        items.append(current.strip())

    return items, index


def parse_paragraph(lines, start_index):
    parts = []
    index = start_index

    while index < len(lines):
        line = lines[index]
        if not line.strip() or is_heading(line) or is_bullet(line) or is_numbered(line):
            break
        parts.append(line.strip())
        index += 1

    return " ".join(parts).strip(), index


def markdown_to_story(markdown_text: str, styles):
    story = build_cover_story(styles)
    lines = markdown_text.splitlines()
    index = 0

    while index < len(lines):
        line = lines[index]

        if not line.strip():
            index += 1
            continue

        if line.startswith("# "):
            index += 1
            continue

        if line.startswith("## "):
            story.append(build_section_banner(line[3:].strip(), styles))
            story.append(Spacer(1, 0.15 * cm))
            index += 1
            continue

        if line.startswith("### "):
            story.append(Paragraph(normalize_inline_markdown(line[4:].strip()), styles["SubTitle"]))
            index += 1
            continue

        if line.startswith("#### "):
            story.append(Paragraph(normalize_inline_markdown(line[5:].strip()), styles["MinorTitle"]))
            index += 1
            continue

        if is_bullet(line):
            items, index = parse_list(lines, index, numbered=False)
            for item in items:
                story.append(
                    Paragraph(
                        normalize_inline_markdown(item),
                        styles["BulletText"],
                        bulletText="•",
                    )
                )
            story.append(Spacer(1, 0.08 * cm))
            continue

        if is_numbered(line):
            items, index = parse_list(lines, index, numbered=True)
            for item in items:
                story.append(Paragraph(normalize_inline_markdown(item), styles["NumberedText"]))
            story.append(Spacer(1, 0.08 * cm))
            continue

        paragraph, index = parse_paragraph(lines, index)
        if paragraph:
            story.append(Paragraph(normalize_inline_markdown(paragraph), styles["BodyTextCustom"]))

    return story


def draw_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawRightString(doc.pagesize[0] - 2 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()


def draw_cover(canvas, doc):
    width, height = doc.pagesize
    canvas.saveState()

    canvas.setFillColor(colors.HexColor(BRAND["light"]))
    canvas.rect(0, 0, width, height, stroke=0, fill=1)

    canvas.setFillColor(colors.HexColor(BRAND["navy"]))
    canvas.rect(0, height - 10.4 * cm, width, 10.4 * cm, stroke=0, fill=1)

    canvas.setFillColor(colors.HexColor(BRAND["teal"]))
    canvas.circle(width - 1.5 * cm, height - 1.8 * cm, 3.8 * cm, stroke=0, fill=1)

    canvas.setFillColor(colors.HexColor(BRAND["forest"]))
    canvas.circle(width - 5.7 * cm, height - 4.1 * cm, 2.6 * cm, stroke=0, fill=1)

    canvas.setFillColor(colors.HexColor("#0b3b35"))
    canvas.roundRect(1.8 * cm, 1.7 * cm, width - 3.6 * cm, 0.65 * cm, 0.2 * cm, stroke=0, fill=1)

    canvas.restoreState()


def draw_content_chrome(canvas, doc):
    width, height = doc.pagesize
    canvas.saveState()

    canvas.setFillColor(colors.HexColor(BRAND["navy"]))
    canvas.rect(0, height - 1.1 * cm, width, 1.1 * cm, stroke=0, fill=1)

    canvas.setFillColor(colors.HexColor(BRAND["teal"]))
    canvas.rect(0, height - 1.1 * cm, 2.8 * cm, 1.1 * cm, stroke=0, fill=1)

    canvas.setFillColor(colors.HexColor("#dbeafe"))
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(2 * cm, height - 0.72 * cm, "Mamba Academic Report")

    canvas.setStrokeColor(colors.HexColor("#cbd5e1"))
    canvas.setLineWidth(0.6)
    canvas.line(2 * cm, 1.7 * cm, width - 2 * cm, 1.7 * cm)

    canvas.setFillColor(colors.HexColor(BRAND["slate"]))
    canvas.setFont("Helvetica", 9)
    canvas.drawString(2 * cm, 1.15 * cm, "Educational platform documentation")

    draw_page_number(canvas, doc)
    canvas.restoreState()


def main():
    styles = build_styles()
    markdown_text = SOURCE_FILE.read_text(encoding="utf-8")
    story = markdown_to_story(markdown_text, styles)

    doc = SimpleDocTemplate(
        str(OUTPUT_FILE),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2.4 * cm,
        bottomMargin=2 * cm,
        title="Mamba Academic Project Documentation",
        author="OpenAI Codex",
    )
    doc.build(story, onFirstPage=draw_cover, onLaterPages=draw_content_chrome)
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
