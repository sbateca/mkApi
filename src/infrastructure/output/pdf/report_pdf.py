from functools import partial
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    LongTable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    TableStyle,
)

from domain.model.report import Report

NAVY = colors.HexColor("#1c2876")
INK = colors.HexColor("#19254a")
MUTED = colors.HexColor("#465472")
LINE = colors.HexColor("#d2dfec")
PALE = colors.HexColor("#e2f3fc")
STRIPE = colors.HexColor("#f6faff")
ACCENT = colors.HexColor("#40a8c7")
LOGO_PATH = Path(__file__).with_name("assets") / "microlab-logo.png"

HEADER_TITLE = ParagraphStyle(
    "HeaderTitle",
    fontName="Helvetica-Bold",
    fontSize=16,
    leading=19,
    textColor=NAVY,
    alignment=TA_CENTER,
)
HEADER_SUBTITLE = ParagraphStyle(
    "HeaderSubtitle", fontSize=8, leading=11, textColor=MUTED, alignment=TA_CENTER
)
FOOTER = ParagraphStyle("Footer", fontSize=8, leading=11, textColor=INK)


TITLE = ParagraphStyle(
    "Title", fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=NAVY
)
SECTION = ParagraphStyle(
    "Section", fontName="Helvetica-Bold", fontSize=12, leading=16, textColor=NAVY
)
TEXT = ParagraphStyle("Text", fontSize=9, leading=13, textColor=INK)
LABEL = ParagraphStyle(
    "Label", fontName="Helvetica-Bold", fontSize=8.5, leading=12, textColor=MUTED
)
COLUMN = ParagraphStyle(
    "Column",
    fontName="Helvetica-Bold",
    fontSize=8.5,
    leading=11,
    textColor=colors.white,
)


def _text(value: str, style: ParagraphStyle = TEXT) -> Paragraph:
    return Paragraph(escape(value).replace("\n", "<br/>"), style)


def _table(rows: list, widths: list[int], *, header: bool = False) -> LongTable:
    table = LongTable(rows, colWidths=widths, repeatRows=int(header), splitInRow=1)
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("ROWBACKGROUNDS", (0, int(header)), (-1, -1), [colors.white, STRIPE]),
        ("LINEBELOW", (0, 0), (-1, -1), 0.45, LINE),
    ]
    if header:
        style.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
    else:
        style.append(("BACKGROUND", (0, 0), (0, -1), PALE))
    table.setStyle(TableStyle(style))
    return table


def _draw_paragraph(canvas, value, style, x, top, width) -> None:
    paragraph = _text(value, style)
    _, height = paragraph.wrap(width, 0)
    paragraph.drawOn(canvas, x, top - height)


def _page_frame(canvas, document, *, logo: ImageReader, report_date: str) -> None:
    canvas.saveState()

    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.7)
    canvas.setFillColor(PALE)
    canvas.roundRect(42, 699, 528, 59, 6, fill=1, stroke=1)
    canvas.line(164, 699, 164, 758)
    canvas.line(448, 699, 448, 758)
    canvas.drawImage(
        logo, 54, 706, width=98, height=45, mask="auto", preserveAspectRatio=True
    )
    _draw_paragraph(canvas, "Informe de ensayo", HEADER_TITLE, 175, 744, 262)
    _draw_paragraph(
        canvas, "MICROLAB DEL NORTE MK S.A.S.", HEADER_SUBTITLE, 175, 721, 262
    )
    _draw_paragraph(canvas, "Fecha del informe", LABEL, 460, 742, 96)
    _draw_paragraph(canvas, report_date, TEXT, 460, 727, 96)

    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(1.2)
    canvas.line(42, 77, 570, 77)
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.7)
    canvas.line(285, 32, 285, 67)
    canvas.line(459, 32, 459, 67)
    _draw_paragraph(canvas, "Dirección y teléfonos", LABEL, 42, 66, 233)
    _draw_paragraph(
        canvas,
        "Calle 2 # 10 E 71, oficina 202, Quinta Oriental\n"
        "Cúcuta, Colombia · 305 360 16 03 / 312 478 64 69",
        FOOTER,
        42,
        52,
        233,
    )
    _draw_paragraph(canvas, "Correo del laboratorio", LABEL, 297, 66, 152)
    _draw_paragraph(
        canvas, "laboratorioanalisismicrobio@gmail.com", FOOTER, 297, 52, 152
    )
    _draw_paragraph(canvas, "NIT", LABEL, 471, 66, 99)
    _draw_paragraph(canvas, "901 713 142 - 6", FOOTER, 471, 52, 99)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(
        42, 18, "Resultados correspondientes a la muestra identificada en este informe."
    )
    canvas.drawRightString(570, 18, f"Página {document.page}")
    canvas.restoreState()


def render_report_pdf(report: Report) -> bytes:
    sample = report.sample
    report_date = report.report_date.strftime("%d/%m/%Y")
    details = [
        ("Dirigido a", sample.client.name),
        ("Código de muestra", sample.sample_code),
        ("Tipo de muestra", sample.sample_type.name),
        ("Muestra y lugar de toma", sample.sample_location),
        ("Responsable de la toma", sample.responsable),
        ("Fecha de toma", sample.get_sample_date.strftime("%d/%m/%Y")),
        ("Fecha de recepción", sample.reception_date.strftime("%d/%m/%Y")),
        ("Fecha de análisis", sample.analysis_date.strftime("%d/%m/%Y")),
        ("Fecha del informe", report_date),
    ]
    results = [
        [
            _text(title, COLUMN)
            for title in ("Ensayo", "Método", "Resultado", "Valor de referencia")
        ]
    ]
    results.extend(
        [
            _text(test.analyte.name),
            _text(test.analysis_method.name),
            _text(test.result),
            _text(test.criteria.name),
        ]
        for test in report.tests
    )
    output = BytesIO()
    document = SimpleDocTemplate(
        output,
        pagesize=letter,
        leftMargin=42,
        rightMargin=42,
        topMargin=110,
        bottomMargin=92,
        title=f"Informe de ensayo {report.report_number}",
        author="Microlab MK",
    )
    story = [
        _text(f"Informe N.º {report.report_number}", TITLE),
        Spacer(1, 19),
        _text("Datos de la muestra", SECTION),
        Spacer(1, 7),
        _table(
            [[_text(label, LABEL), _text(value)] for label, value in details],
            [172, 356],
        ),
        Spacer(1, 23),
        _text("Resultados", SECTION),
        Spacer(1, 7),
    ]
    if report.tests:
        story.append(_table(results, [150, 117, 124, 137], header=True))
    else:
        story.append(_text("El reporte no contiene ensayos registrados."))
    page_frame = partial(
        _page_frame, logo=ImageReader(LOGO_PATH), report_date=report_date
    )
    document.build(story, onFirstPage=page_frame, onLaterPages=page_frame)
    return output.getvalue()
