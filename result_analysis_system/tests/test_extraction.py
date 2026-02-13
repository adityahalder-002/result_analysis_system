import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import extractor
import pdf_parser as parser

def test_extraction():
    pdf_path = os.path.join(os.path.dirname(__file__), "..", "sample_marksheet.pdf")
    if not os.path.exists(pdf_path):
        print("Error: sample_marksheet.pdf not found.")
        return

    print(f"Extracting text from {pdf_path}...")
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
        text = extractor.extract_text_from_pdf_bytes(pdf_bytes)
    
    print("\n--- Extracted Text ---")
    print(text)
    print("----------------------\n")

    print("\n--- Parsed Student Details ---")
    student_data = parser.parse_student_details(text)
    for k, v in student_data.items():
        print(f"{k}: {v}")

    print("\n--- Parsed Subject Marks ---")
    subjects = parser.parse_subject_marks(text)
    for sub in subjects:
        print(sub)

if __name__ == "__main__":
    test_extraction()
