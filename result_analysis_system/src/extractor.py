import pdfplumber
import zipfile
import io
import os

def extract_text_from_pdf_bytes(pdf_bytes):
    """
    Extracts text from a single PDF file (bytes).
    """
    text = ""
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text

def extract_data_from_zip(zip_file):
    """
    Extracts text from all PDFs in a ZIP file.
    Args:
        zip_file: A file-like object (uploaded file) or path to a zip file.
    Returns:
        dict: filename -> text content
    """
    pdf_texts = {}
    with zipfile.ZipFile(zip_file, 'r') as z:
        for filename in z.namelist():
            if filename.lower().endswith('.pdf'):
                with z.open(filename) as f:
                    pdf_bytes = f.read()
                    try:
                        text = extract_text_from_pdf_bytes(pdf_bytes)
                        pdf_texts[filename] = text
                    except Exception as e:
                        print(f"Error reading {filename}: {e}")
    return pdf_texts

if __name__ == "__main__":
    print("Testing extractor.py...")
    try:
        import pdfplumber
        print(f"pdfplumber imported: {pdfplumber.__version__}")
    except ImportError as e:
        print(f"Import failed: {e}")
