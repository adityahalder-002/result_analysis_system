import pandas as pd

def generate_excel(student_master, subject_data_flattened, student_analysis, subject_analysis_df, output_path):
    """
    Generates the final Excel file with 4 sheets and charts.
    Args:
        student_master: list of dicts
        subject_data_flattened: list of dicts (all subjects for all students)
        student_analysis: dict of metrics
        subject_analysis_df: DataFrame
        output_path: str
    """
    
    # Create DataFrames
    df_student_master = pd.DataFrame(student_master)
    df_subject_marks = pd.DataFrame(subject_data_flattened)
    
    # Rename Columns
    df_student_master.rename(columns={'Total Marks': 'Total Maximum Marks', 'Obtained Marks': 'Total Obtained Marks'}, inplace=True)

    
    # Create Student Analysis DataFrame for sheet
    # We want it as a table: Metric | Value
    df_student_analysis = pd.DataFrame(list(student_analysis.items()), columns=['Metric', 'Value'])
    
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        # Sheet 1: Student_Master
        df_student_master.to_excel(writer, sheet_name='Student_Master', index=False)
        
        # Sheet 2: Subject_Marks
        df_subject_marks.to_excel(writer, sheet_name='Subject_Marks', index=False)
        
        # Sheet 3: Student_Analysis
        df_student_analysis.to_excel(writer, sheet_name='Student_Analysis', index=False)
        
        # Sheet 4: Subject_Wise_Analysis
        subject_analysis_df.to_excel(writer, sheet_name='Subject_Wise_Analysis', index=False)
        
        # Get workbook and worksheets
        workbook = writer.book
        worksheet_analysis = writer.sheets['Student_Analysis']
        worksheet_sub_analysis = writer.sheets['Subject_Wise_Analysis']
        
        # --- Charts ---
        
        # 1. Pie Chart for Overall Result (in Student_Analysis sheet)
        # Data source: Passed Count vs Failed Count
        # Their rows are index 1 and 2 (0-based is title) -> Rows 2 and 3 in Excel (1-based)
        # Passed Count is row 2 (index 1 in DF)
        # Failed Count is row 3 (index 2 in DF)
        
        chart_pie = workbook.add_chart({'type': 'pie'})
        
        # Configure series
        # Categories: 'Passed Count', 'Failed Count' (Column A)
        # Values: Their values (Column B)
        # We need to find row numbers dynamically or assume fixed order from analysis.py
        # analysis.py order: Total, Passed, Failed
        # Row 0: Header
        # Row 1: Total
        # Row 2: Passed
        # Row 3: Failed
        
        chart_pie.add_series({
            'name': 'Overall Result',
            'categories': ['Student_Analysis', 2, 0, 3, 0], # A3:A4
            'values':     ['Student_Analysis', 2, 1, 3, 1], # B3:B4
            'data_labels': {'percentage': True},
        })
        
        chart_pie.set_title({'name': 'Overall Pass/Fail Distribution'})
        chart_pie.set_style(10)
        
        worksheet_analysis.insert_chart('D2', chart_pie)
        
        # 2. Bar Chart for Subject Pass Percentage (in Subject_Wise_Analysis sheet)
        # Columns: Subject Name (A), Pass Percentage (E) - check analysis.py column order
        # analysis.py columns: Subject Name, Students Appeared, Passed, Failed, Pass Percentage, Distinction..., First Class...
        # Index 0: Subject Name (Col A)
        # Index 4: Pass Percentage (Col E)
        
        chart_bar = workbook.add_chart({'type': 'column'})
        
        num_subjects = len(subject_analysis_df)
        
        chart_bar.add_series({
            'name': 'Pass Percentage',
            'categories': ['Subject_Wise_Analysis', 1, 0, num_subjects, 0], # A2:A_End
            'values':     ['Subject_Wise_Analysis', 1, 4, num_subjects, 4], # E2:E_End
            'data_labels': {'value': True},
        })
        
        chart_bar.set_title({'name': 'Subject-wise Pass Percentage'})
        chart_bar.set_y_axis({'name': 'Percentage', 'min': 0, 'max': 100})
        
        worksheet_sub_analysis.insert_chart('H2', chart_bar)
        
    return output_path
