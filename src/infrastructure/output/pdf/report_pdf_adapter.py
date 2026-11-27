from asyncio import to_thread

from domain.model.report import Report
from domain.spi.report_pdf_port import ReportPdfPort
from infrastructure.output.pdf.report_pdf import render_report_pdf
from infrastructure.output.storage.s3_report_pdf_storage import S3ReportPdfStorage

REPORT_PDF_LAYOUT_VERSION = "v2"


class ReportPdfAdapter(ReportPdfPort):
    def __init__(self, storage: S3ReportPdfStorage):
        self.storage = storage

    async def get_or_create(self, report: Report) -> bytes:
        return await to_thread(
            self.storage.get_or_create,
            f"reports/{REPORT_PDF_LAYOUT_VERSION}/{report.id}.pdf",
            lambda: render_report_pdf(report),
        )
