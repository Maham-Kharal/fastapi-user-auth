import io
import os
import logging
from datetime import datetime, timedelta
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
import asyncpg
from arq import cron
from arq.connections import RedisSettings
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("arq_worker")


async def fetch_yesterday_stats(db_url: str) -> dict:
    """Fetch yesterday's loan/return stats and current active/overdue totals from Postgres."""
    yesterday = datetime.utcnow().date() - timedelta(days=1)
    now = datetime.utcnow()

    # Convert sqlalchemy url if needed
    raw_url = db_url.replace("postgresql+psycopg2://", "postgresql://")

    try:
        conn = await asyncpg.connect(raw_url)
        try:
            loans_yesterday = await conn.fetchval(
                "SELECT COUNT(*) FROM loans WHERE DATE(borrowed_at) = $1", yesterday
            )
            returns_yesterday = await conn.fetchval(
                "SELECT COUNT(*) FROM loans WHERE DATE(returned_at) = $1", yesterday
            )
            total_active_loans = await conn.fetchval(
                "SELECT COUNT(*) FROM loans WHERE status = 'borrowed'"
            )
            overdue_count = await conn.fetchval(
                "SELECT COUNT(*) FROM loans WHERE status = 'borrowed' AND due_date < $1", now
            )
            total_books = await conn.fetchval(
                "SELECT COUNT(*) FROM books"
            )
            return {
                "loans_yesterday": loans_yesterday or 0,
                "returns_yesterday": returns_yesterday or 0,
                "total_active_loans": total_active_loans or 0,
                "overdue": overdue_count or 0,
                "total_books": total_books or 0,
                "yesterday": str(yesterday),
            }
        finally:
            await conn.close()
    except Exception as err:
        logger.warning(f"Database query fallback due to: {err}")
        return {
            "loans_yesterday": 0,
            "returns_yesterday": 0,
            "total_active_loans": 0,
            "overdue": 0,
            "total_books": 0,
            "yesterday": str(yesterday),
        }


def build_pdf_in_memory(yesterday_str: str, stats: dict) -> bytes:
    """Generate a PDF report entirely in memory using ReportLab (no disk writes)."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.fontSize = 20
    title_style.leading = 24

    story = [
        Paragraph("Library Activity Daily Report", title_style),
        Spacer(1, 12),
        Paragraph(f"<b>Report Date (Yesterday):</b> {yesterday_str}", styles["Normal"]),
        Spacer(1, 18),
    ]

    table_data = [
        ["Metric Description", "Count"],
        ["Books Borrowed Yesterday", str(stats.get("loans_yesterday", 0))],
        ["Books Returned Yesterday", str(stats.get("returns_yesterday", 0))],
        ["Currently Active Loans", str(stats.get("total_active_loans", 0))],
        ["Overdue Books", str(stats.get("overdue", 0))],
        ["Total Books in Catalog", str(stats.get("total_books", 0))],
    ]

    tbl = Table(table_data, colWidths=[260, 140])
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E293B")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("TOPPADDING", (0, 0), (-1, 0), 8),
                ("ALIGN", (1, 0), (1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ("TOPPADDING", (0, 1), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
            ]
        )
    )

    story.append(tbl)
    doc.build(story)
    return buffer.getvalue()


async def generate_and_email_report(ctx):
    """ARQ async background task to generate PDF report and email it."""
    logger.info("ARQ Worker: Starting generate_and_email_report task...")

    # 1. Fetch stats from database
    stats = await fetch_yesterday_stats(settings.DATABASE_URL)
    yesterday_str = stats.get("yesterday", str(datetime.utcnow().date() - timedelta(days=1)))
    logger.info(f"Fetched stats for {yesterday_str}: {stats}")

    # 2. Build PDF in memory
    pdf_bytes = build_pdf_in_memory(yesterday_str, stats)
    logger.info(f"Built PDF in memory successfully ({len(pdf_bytes)} bytes)")

    # 2b. Save PDF copy to disk in static/reports/
    os.makedirs("static/reports", exist_ok=True)
    report_filename = f"library_report_{yesterday_str}.pdf"
    saved_pdf_path = os.path.join("static", "reports", report_filename)
    try:
        with open(saved_pdf_path, "wb") as f:
            f.write(pdf_bytes)
        logger.info(f"Saved PDF copy to disk at: {saved_pdf_path}")
    except Exception as err:
        logger.warning(f"Failed to save PDF copy to disk: {err}")

    # 3. Email PDF as attachment
    recipient = settings.REPORT_EMAIL_TO or "admin@library.com"
    subject = f"Daily Library Activity Report - {yesterday_str}"

    msg = MIMEMultipart()
    msg["From"] = settings.SMTP_USER or "reports@library.com"
    msg["To"] = recipient
    msg["Subject"] = subject

    body_text = f"Hello,\n\nPlease find attached yesterday's library activity report for {yesterday_str}.\n\nBest regards,\nLibrary Management System"
    msg.attach(MIMEText(body_text, "plain"))

    part = MIMEBase("application", "pdf")
    part.set_payload(pdf_bytes)
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f'attachment; filename="library_report_{yesterday_str}.pdf"',
    )
    msg.attach(part)

    try:
        if settings.SMTP_PASSWORD and settings.SMTP_PASSWORD != "dummy_password":
            await aiosmtplib.send(
                msg,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                start_tls=True,
                username=settings.SMTP_USER,
                password=settings.SMTP_PASSWORD,
            )
            logger.info(f"Email sent successfully to {recipient}")
        else:
            logger.info(
                f"[DEV MOCK EMAIL] Report email created with PDF attachment ({len(pdf_bytes)} bytes) for {recipient}. (Skipped live SMTP send because dummy_password is set)."
            )
    except Exception as err:
        logger.error(f"Failed to deliver email: {err}")

    logger.info("ARQ Worker: Completed generate_and_email_report task successfully.")
    return {"status": "success", "pdf_size_bytes": len(pdf_bytes), "stats": stats}


from app.core.database import SessionLocal
from app.models.models import Document
from app.services.document_parser import (
    extract_pdf_chunks,
    extract_docx_chunks,
    extract_txt_chunks,
    extract_pptx_chunks,
)
from app.services.qdrant_service import upsert_documents


async def process_document_ingestion(ctx, document_id: int):
    """ARQ background task to extract, chunk, embed, and index uploaded PDF/DOCX/PPTX/TXT files into Qdrant."""
    logger.info("ARQ Ingestion Worker: Starting task for document_id=%d", document_id)
    db = SessionLocal()
    try:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            logger.error("Document id=%d not found in database.", document_id)
            return {"status": "failed", "reason": "Document not found"}

        if not os.path.exists(doc.file_path):
            doc.status = "failed"
            doc.error_message = f"File not found at path: {doc.file_path}"
            db.commit()
            return {"status": "failed", "reason": doc.error_message}

        # 1. Extract text & chunks based on file format
        if doc.file_type == "pdf":
            raw_chunks = extract_pdf_chunks(doc.file_path, doc.filename)
        elif doc.file_type == "docx":
            raw_chunks = extract_docx_chunks(doc.file_path, doc.filename)
        elif doc.file_type == "txt":
            raw_chunks = extract_txt_chunks(doc.file_path, doc.filename)
        elif doc.file_type == "pptx":
            raw_chunks = extract_pptx_chunks(doc.file_path, doc.filename)
        else:
            doc.status = "failed"
            doc.error_message = f"Unsupported file type: {doc.file_type}"
            db.commit()
            return {"status": "failed", "reason": doc.error_message}

        if not raw_chunks:
            doc.status = "failed"
            doc.error_message = "No readable text extracted from document."
            db.commit()
            return {"status": "failed", "reason": doc.error_message}

        # 2. Attach strict metadata payload for session/user isolation
        points_payloads = []
        for chunk in raw_chunks:
            points_payloads.append({
                "text": chunk["content"],
                "content": chunk["content"],
                "document_id": doc.id,
                "user_id": doc.user_id,
                "session_id": doc.session_id,
                "source": doc.filename,
                "page_number": chunk.get("page_number", 1),
                "section": chunk.get("section", "General"),
            })

        # 3. Embed and upsert into Qdrant
        await upsert_documents(points_payloads)

        # 4. Mark document as completed
        doc.status = "completed"
        doc.error_message = None
        db.commit()

        logger.info(
            "ARQ Ingestion Worker: Successfully indexed document_id=%d ('%s') with %d chunks into Qdrant.",
            doc.id, doc.filename, len(points_payloads)
        )
        return {"status": "completed", "document_id": doc.id, "chunks_count": len(points_payloads)}

    except Exception as exc:
        logger.error("ARQ Ingestion Worker failed for document_id=%d: %s", document_id, exc)
        try:
            doc = db.query(Document).filter(Document.id == document_id).first()
            if doc:
                doc.status = "failed"
                doc.error_message = str(exc)
                db.commit()
        except Exception:
            pass
        return {"status": "failed", "error": str(exc)}
    finally:
        db.close()


class WorkerSettings:
    functions = [generate_and_email_report, process_document_ingestion]
    # For testing: run every minute (minute=None or minute=set(range(60)) fires every minute in ARQ cron)
    # Production schedule: cron(generate_and_email_report, hour=7, minute=0)
    cron_jobs = [
        cron(generate_and_email_report,hour=7, minute=0),  # Daily at 7:00 AM UTC)
    ]
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
