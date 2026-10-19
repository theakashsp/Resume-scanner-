from __future__ import annotations

import io
import pytest
from pypdf import PdfWriter

from pdf_parser import (
    CorruptedPDFError,
    EmptyPDFError,
    EncryptedPDFError,
    ExcessivePageCountError,
    FileSizeLimitExceededError,
    InvalidPDFSignatureError,
    ScannedPDFError,
    extract_pdf_text_from_bytes,
    normalize_extracted_text,
    validate_pdf_bytes,
)


def _make_text_pdf(text: str) -> bytes:
    stream = f"BT\n/F1 12 Tf\n72 712 Td\n({text}) Tj\nET\n"
    stream_bytes = stream.encode("latin1")
    obj1 = b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    obj2 = b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
    obj3 = b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
    obj4 = b"4 0 obj\n<< /Length " + str(len(stream_bytes)).encode("ascii") + b" >>\nstream\n" + stream_bytes + b"endstream\nendobj\n"
    obj5 = b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"

    header = b"%PDF-1.4\n"
    offsets = [0]
    curr = len(header)
    for obj in (obj1, obj2, obj3, obj4, obj5):
        offsets.append(curr)
        curr += len(obj)

    xref = f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode("ascii")
    for off in offsets[1:]:
        xref += f"{off:010d} 00000 n \n".encode("ascii")

    trailer = f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{curr}\n%%EOF\n".encode("ascii")
    return header + obj1 + obj2 + obj3 + obj4 + obj5 + xref + trailer


def test_valid_text_pdf_extraction():
    sample_text = "John Doe - Python Developer with React, Docker, and AWS experience."
    pdf_bytes = _make_text_pdf(sample_text)
    extracted = extract_pdf_text_from_bytes(pdf_bytes)
    assert "John Doe" in extracted
    assert "Python Developer" in extracted
    assert "Docker" in extracted


def test_empty_pdf_rejected():
    with pytest.raises(EmptyPDFError) as exc_info:
        validate_pdf_bytes(b"")
    assert "empty" in str(exc_info.value).lower()


def test_invalid_pdf_signature_rejected():
    with pytest.raises(InvalidPDFSignatureError) as exc_info:
        validate_pdf_bytes(b"Hello world, this is a plain text file pretending to be PDF.")
    assert "signature" in str(exc_info.value).lower()


def test_corrupted_pdf_handling():
    corrupted_data = b"%PDF-1.4\n" + b"random corrupted garbage byte stream \x00\xff" * 50
    with pytest.raises(CorruptedPDFError):
        extract_pdf_text_from_bytes(corrupted_data)


def test_encrypted_pdf_detection():
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    writer.encrypt("secure_password_123")
    buf = io.BytesIO()
    writer.write(buf)
    encrypted_bytes = buf.getvalue()

    with pytest.raises(EncryptedPDFError) as exc_info:
        extract_pdf_text_from_bytes(encrypted_bytes)
    assert "password-protected" in str(exc_info.value).lower()


def test_scanned_image_only_pdf_detection():
    # Blank PDF with pages but no extractable text
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    buf = io.BytesIO()
    writer.write(buf)
    blank_bytes = buf.getvalue()

    with pytest.raises(ScannedPDFError) as exc_info:
        extract_pdf_text_from_bytes(blank_bytes)
    assert "scanned or image-only" in str(exc_info.value).lower()


def test_large_file_size_rejection():
    # Simulate oversized data without allocating 10MB memory
    huge_data = b"%PDF-1.4\n" + b"X" * (11 * 1024 * 1024)
    with pytest.raises(FileSizeLimitExceededError) as exc_info:
        validate_pdf_bytes(huge_data)
    assert "exceeds" in str(exc_info.value).lower()


def test_excessive_page_count_rejection():
    writer = PdfWriter()
    for _ in range(35):
        writer.add_blank_page(width=612, height=792)
    buf = io.BytesIO()
    writer.write(buf)
    data = buf.getvalue()

    with pytest.raises(ExcessivePageCountError) as exc_info:
        validate_pdf_bytes(data)
    assert "maximum limit" in str(exc_info.value).lower()


def test_normalization_preserves_technical_keywords():
    raw_text = "  Experience in C++, C#, .NET, Python, and SQL.\r\n\r\n\r\n\r\n  Led team of 5.  "
    cleaned = normalize_extracted_text(raw_text)
    assert "C++" in cleaned
    assert "C#" in cleaned
    assert ".NET" in cleaned
    assert "\n\n\n\n" not in cleaned


def test_pdf_parser_fallback_on_pdfminer_failure(monkeypatch):
    import pdf_parser

    # Simulate pdfminer failure
    def broken_pdfminer(*args, **kwargs):
        raise RuntimeError("Simulated pdfminer crash")

    monkeypatch.setattr(pdf_parser, "pdfminer_extract_text", broken_pdfminer)

    sample_text = "Jane Doe - Python and AWS Cloud Specialist with Docker experience."
    pdf_bytes = _make_text_pdf(sample_text)
    extracted = pdf_parser.extract_pdf_text_from_bytes(pdf_bytes)
    # Fallback to pypdf should succeed
    assert "Jane Doe" in extracted
    assert "Python" in extracted

