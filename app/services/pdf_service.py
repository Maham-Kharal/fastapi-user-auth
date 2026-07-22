import io

try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False
    PdfReader = None


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> list[dict]:
    """
    Parses raw PDF bytes and extracts text page-by-page.
    Returns a list of document dicts: [{"title": ..., "text": ...}]
    """
    if not HAS_PYPDF or PdfReader is None:
        raise RuntimeError("pypdf library is missing. Please run: pip install pypdf")

    reader = PdfReader(io.BytesIO(pdf_bytes))
    documents = []

    for i, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        page_text = page_text.strip()
        if page_text:
            documents.append({
                "title": f"PDF Document — Page {i + 1}",
                "text": page_text
            })

    return documents

