
import pdfplumber

def dump_pdf_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            print(f"--- Page {page.page_number} ---")
            print(text)
            print("----------------")

if __name__ == "__main__":
    dump_pdf_text("sample_marksheet.pdf")
