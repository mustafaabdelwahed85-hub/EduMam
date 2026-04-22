import re
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


BASE_DIR = Path(__file__).resolve().parent
SOURCE_FILE = BASE_DIR / "ACADEMIC_DOCUMENTATION.md"
OUTPUT_FILE = BASE_DIR / "Mamba_Academic_Documentation.pdf"


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
            name="DocTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=30,
            textColor=colors.HexColor("#0f172a"),
            alignment=TA_CENTER,
            spaceAfter=18,
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
            textColor=colors.HexColor("#475569"),
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
            textColor=colors.HexColor("#0f172a"),
            spaceBefore=12,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubTitle",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=18,
            textColor=colors.HexColor("#166534"),
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
            textColor=colors.HexColor("#0f766e"),
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
            textColor=colors.HexColor("#111827"),
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
            textColor=colors.HexColor("#111827"),
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
            textColor=colors.HexColor("#111827"),
        )
    )
    return styles


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
    story = []
    lines = markdown_text.splitlines()
    index = 0

    story.append(Paragraph("Mamba Academic Project Documentation", styles["DocTitle"]))
    story.append(
        Paragraph(
            f"Generated from project sources on {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            styles["Meta"],
        )
    )
    story.append(Spacer(1, 0.5 * cm))

    while index < len(lines):
        line = lines[index]

        if not line.strip():
            index += 1
            continue

        if line.startswith("# "):
            index += 1
            continue

        if line.startswith("## "):
            story.append(Paragraph(normalize_inline_markdown(line[3:].strip()), styles["SectionTitle"]))
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


def main():
    styles = build_styles()
    markdown_text = SOURCE_FILE.read_text(encoding="utf-8")
    story = markdown_to_story(markdown_text, styles)

    doc = SimpleDocTemplate(
        str(OUTPUT_FILE),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="Mamba Academic Project Documentation",
        author="OpenAI Codex",
    )
    doc.build(story, onFirstPage=draw_page_number, onLaterPages=draw_page_number)
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
