# MSBTE Result Analysis System

A system to process bulk MSBTE marksheet PDFs and generate a consolidated Excel report.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   streamlit run app.py
   ```

## Structure

- `app.py`: Main Streamlit application.
- `extractor.py`: Handles ZIP and PDF extraction.
- `parser.py`: Regex logic for parsing text.
- `processor.py`: Applies pass/fail and grading rules.
- `analysis.py`: Generates statistical analysis.
- `excel_generator.py`: Creates the final Excel report with charts.
