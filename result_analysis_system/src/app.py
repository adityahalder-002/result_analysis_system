import streamlit as st
import os
import tempfile
import pandas as pd
import extractor
import extractor
import pdf_parser as parser
import processor
import analysis
import excel_generator

def main():
    st.set_page_config(page_title="MSBTE Result Analysis", layout="wide")
    st.title("📊 MSBTE Result Analysis System")
    st.markdown("""
    Upload a **ZIP file** containing MSBTE marksheet PDFs. 
    The system will extract data, calculate results, and generate a detailed Excel report with analytics.
    """)

    uploaded_file = st.file_uploader("Choose a ZIP file", type="zip")

    if uploaded_file is not None:
        if st.button("Process Marksheets", type="primary"):
            with st.spinner("Processing files... This may take a moment."):
                try:
                    # 1. Extraction
                    # Create a temporary file for the uploaded zip because zipfile needs a path or file-like
                    # st.file_uploader returns BytesIO, which zipfile accepts.
                    
                    pdf_texts = extractor.extract_data_from_zip(uploaded_file)
                    st.success(f"Extracted {len(pdf_texts)} PDFs.")
                    
                    if not pdf_texts:
                        st.error("No PDFs found in the ZIP file.")
                        return

                    # 2. Parsing & Processing
                    all_student_data = []
                    all_subject_data = [] # Flattened for Excel
                    
                    progress_bar = st.progress(0)
                    total_files = len(pdf_texts)
                    
                    for i, (filename, text) in enumerate(pdf_texts.items()):
                        # Parse
                        student = parser.parse_student_details(text)
                        subjects = parser.parse_subject_marks(text)
                        
                        # Process (Calculate Result & Class)
                        student = processor.process_results(student, subjects)
                        
                        # Add tracking info
                        student['Filename'] = filename
                        all_student_data.append(student)
                        
                        for sub in subjects:
                            sub['Enrollment No'] = student['Enrollment No']
                            sub['Student Name'] = student['Name']
                            all_subject_data.append(sub)
                        
                        progress_bar.progress((i + 1) / total_files)
                    
                    # 3. Analysis
                    student_metrics, subject_metrics_df = analysis.calculate_analysis(all_student_data, all_subject_data)
                    
                    # 4. Excel Generation
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                        output_path = tmp.name
                        
                    excel_generator.generate_excel(
                        all_student_data, 
                        all_subject_data, 
                        student_metrics, 
                        subject_metrics_df, 
                        output_path
                    )
                    
                    # 5. Display & Download
                    st.success("Analysis Complete!")
                    
                    # Show quick stats
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Total Students", student_metrics['Total Students Appeared'])
                    c2.metric("Passed", student_metrics['Passed Count'])
                    c3.metric("Pass %", f"{student_metrics['Overall Pass Percentage']}%")
                    
                    with open(output_path, "rb") as f:
                        st.download_button(
                            label="📥 Download Detailed Excel Report",
                            data=f,
                            file_name="MSBTE_Result_Analysis.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                        
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    # print traceback for debugging in console
                    import traceback
                    traceback.print_exc()

if __name__ == "__main__":
    main()
