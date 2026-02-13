import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import processor
import analysis
import pandas as pd

def test_logic():
    # Mock Data
    student_data = [
        {'Name': 'Student A', 'Enrollment No': '101', 'Class': 'Unknown', 'Percentage': '78.50'},
        {'Name': 'Student B', 'Enrollment No': '102', 'Class': 'Unknown', 'Percentage': '45.00'},
        {'Name': 'Student C', 'Enrollment No': '103', 'Class': 'Unknown', 'Percentage': '35.00'}
    ]
    
    subject_data_A = [
        {'Subject Name': 'Math', 'Subject Result': 'P', 'Subject Total': 80},
        {'Subject Name': 'Science', 'Subject Result': 'P', 'Subject Total': 75}
    ]
    
    subject_data_B = [
        {'Subject Name': 'Math', 'Subject Result': 'P', 'Subject Total': 45},
        {'Subject Name': 'Science', 'Subject Result': 'P', 'Subject Total': 40}
    ]
    
    subject_data_C = [
        {'Subject Name': 'Math', 'Subject Result': 'F', 'Subject Total': 30},
        {'Subject Name': 'Science', 'Subject Result': 'P', 'Subject Total': 50}
    ]
    
    # Process Results
    print("Processing Student A...")
    processed_A = processor.process_results(student_data[0], subject_data_A)
    print(processed_A)
    
    print("Processing Student B...")
    processed_B = processor.process_results(student_data[1], subject_data_B)
    print(processed_B)
    
    print("Processing Student C...")
    processed_C = processor.process_results(student_data[2], subject_data_C)
    print(processed_C)
    
    # Analysis
    all_students = [processed_A, processed_B, processed_C]
    all_subjects = []
    
    for s in subject_data_A: all_subjects.append(s)
    for s in subject_data_B: all_subjects.append(s)
    for s in subject_data_C: all_subjects.append(s)
    
    print("\nCalculating Analysis...")
    metrics, sub_df = analysis.calculate_analysis(all_students, all_subjects)
    
    print("\nStudent Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v}")
        
    print("\nSubject Metrics:")
    print(sub_df)

if __name__ == "__main__":
    test_logic()
