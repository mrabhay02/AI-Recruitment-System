from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file):
    """Extract text from a PDF resume."""
    reader = PdfReader(uploaded_file)

    text = []

    for page in reader.pages:
        text.append(page.extract_text() or "")

    return "\n".join(text).strip()