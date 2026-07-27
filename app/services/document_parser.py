import os
import io
import zipfile
import logging
from typing import List, Dict, Any
from pypdf import PdfReader
import docx
import filetype

logger = logging.getLogger(__name__)


def sniff_mime_type(content: bytes) -> str:
    """
    Inspect raw binary magic bytes to determine file type.
    Does NOT rely on client-supplied headers or filename extensions.
    Returns 'pdf' or 'docx'. Raises ValueError if invalid.
    """
    if len(content) < 4:
        raise ValueError("File is too small or corrupted.")

    # PDF check: Starts with %PDF- (0x25 0x50 0x44 0x46 0x2D)
    if content.startswith(b"%PDF-"):
        return "pdf"

    # DOCX check: Zip container starting with PK\x03\x04
    if content.startswith(b"PK\x03\x04"):
        try:
            with zipfile.ZipFile(io.BytesIO(content)) as zf:
                namelist = zf.namelist()
                # Check for standard Word processing XML components
                if any("word/document.xml" in name for name in namelist):
                    return "docx"
        except zipfile.BadZipFile:
            pass

    # Fallback to filetype library detection
    kind = filetype.guess(content)
    if kind:
        if kind.extension == "pdf":
            return "pdf"
        elif kind.extension == "docx":
            return "docx"

    raise ValueError("Invalid file format. Only genuine PDF and DOCX documents are supported.")


def _chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """Split text into overlapping character chunks."""
    text = text.strip()
    if not text:
        return []
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += (chunk_size - overlap)
    return chunks


def extract_pdf_chunks(file_path: str, filename: str, chunk_size: int = 500, overlap: int = 100) -> List[Dict[str, Any]]:
    """Extract page-by-page text from PDF file and return chunks with page metadata."""
    reader = PdfReader(file_path)
    chunks = []

    for page_num, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        text_chunks = _chunk_text(page_text, chunk_size, overlap)
        for chunk in text_chunks:
            chunks.append({
                "content": chunk,
                "page_number": page_num,
                "section": f"Page {page_num}",
                "source": filename,
            })

    logger.info("Extracted %d chunks from PDF '%s' across %d pages.", len(chunks), filename, len(reader.pages))
    return chunks


def extract_docx_chunks(file_path: str, filename: str, chunk_size: int = 500, overlap: int = 100) -> List[Dict[str, Any]]:
    """Extract section-by-section text from DOCX file and return chunks with section metadata."""
    doc = docx.Document(file_path)
    chunks = []
    current_section = "General"
    section_text_buffer = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        
        # Check if heading paragraph
        if para.style.name.startswith("Heading"):
            if section_text_buffer:
                full_section_text = "\n".join(section_text_buffer)
                for chunk in _chunk_text(full_section_text, chunk_size, overlap):
                    chunks.append({
                        "content": chunk,
                        "page_number": 1,
                        "section": current_section,
                        "source": filename,
                    })
                section_text_buffer = []
            current_section = text
        else:
            section_text_buffer.append(text)

    if section_text_buffer:
        full_section_text = "\n".join(section_text_buffer)
        for chunk in _chunk_text(full_section_text, chunk_size, overlap):
            chunks.append({
                "content": chunk,
                "page_number": 1,
                "section": current_section,
                "source": filename,
            })

    logger.info("Extracted %d chunks from DOCX '%s'.", len(chunks), filename)
    return chunks
