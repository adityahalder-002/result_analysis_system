import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pandas as pd
import excel_generator

def test_excel_gen():
    print("Testing Excel Generation...")
    
    # Mock Data (same as test_processing but structured for excel_generator)
    student_data = [
        {'Name': 'Student A', 'Enrollment No': '101', 'Class': 'First Class with Distinction', 'Percentage': 78.50, 'Result': 'PASS'},
        {'Name': 'Student B', 'Enrollment No': '102', 'Class': 'Pass Class', 'Percentage': 45.00, 'Result': 'PASS'},
        {'Name': 'Student C', 'Enrollment No': '103', 'Class': 'Fail', 'Percentage': 35.00, 'Result': 'FAIL'}
    ]
    
    subject_data_flattened = [
        {'Enrollment No': '101', 'Student Name': 'Student A', 'Subject Name': 'Math', 'Subject Result': 'P', 'Subject Total': 80},
        {'Enrollment No': '101', 'Student Name': 'Student A', 'Subject Name': 'Science', 'Subject Result': 'P', 'Subject Total': 75},
        {'Enrollment No': '102', 'Student Name': 'Student B', 'Subject Name': 'Math', 'Subject Result': 'P', 'Subject Total': 45},
        {'Enrollment No': '102', 'Student Name': 'Student B', 'Subject Name': 'Science', 'Subject Result': 'P', 'Subject Total': 40},
        {'Enrollment No': '103', 'Student Name': 'Student C', 'Subject Name': 'Math', 'Subject Result': 'F', 'Subject Total': 30},
        {'Enrollment No': '103', 'Student Name': 'Student C', 'Subject Name': 'Science', 'Subject Result': 'P', 'Subject Total': 50}
    ]
    
    student_metrics = {
        'Total Students Appeared': 3,
        'Passed Count': 2,
        'Failed Count': 1,
        'Distinction Count': 1,
        'First Class Count': 0,
        'Second Class Count': 0,
        'Overall Pass Percentage': 66.67
    }
    
    subject_metrics_df = pd.DataFrame([
        {'Subject Name': 'Math', 'Students Appeared': 3, 'Passed': 2, 'Failed': 1, 'Pass Percentage': 66.67, 'Distinction Count': 1, 'First Class Count': 0},
        {'Subject Name': 'Science', 'Students Appeared': 3, 'Passed': 3, 'Failed': 0, 'Pass Percentage': 100.0, 'Distinction Count': 1, 'First Class Count': 0}
    ])
    
    output_path = "test_output.xlsx"
    
    try:
        excel_generator.generate_excel(
            student_data, 
            subject_data_flattened, 
            student_metrics, 
            subject_metrics_df, 
            output_path
        )
        print(f"Successfully created {output_path}")
    except Exception as e:
        print(f"Failed to create Excel: {e}")
        raise e

if __name__ == "__main__":
    test_excel_gen()
