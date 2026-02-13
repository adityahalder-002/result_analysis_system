import pandas as pd

def calculate_analysis(all_student_data, all_subject_data):
    """
    Calculates statistical metrics for the analysis sheets.
    Args:
        all_student_data: list of student dicts
        all_subject_data: list of all subject dicts (flattened)
    Returns:
        student_metrics: dict
        subject_metrics_df: DataFrame
    """
    df_students = pd.DataFrame(all_student_data)
    df_subjects = pd.DataFrame(all_subject_data)

    # Student Analysis
    total_students = len(df_students)
    passed_count = len(df_students[df_students['Result'] == 'PASS'])
    failed_count = total_students - passed_count
    
    # Class counts
    # Normalized classes: "First Class with Distinction", "First Class", "Second Class", "Pass Class", "Fail", "A.T.K.T."
    
    distinction_count = len(df_students[df_students['Class'] == 'First Class with Distinction'])
    first_class_count = len(df_students[df_students['Class'] == 'First Class'])
    second_class_count = len(df_students[df_students['Class'] == 'Second Class'])
    pass_class_count = len(df_students[df_students['Class'] == 'Pass Class'])
    atkt_count = len(df_students[df_students['Result'] == 'ATKT'])
    
    pass_percentage = (passed_count / total_students * 100) if total_students > 0 else 0

    student_metrics = {
        'Total Students Appeared': total_students,
        'Passed Count': passed_count,
        'Failed Count': failed_count,
        'ATKT Count': atkt_count,
        'Distinction Count': distinction_count,
        'First Class Count': first_class_count,
        'Second Class Count': second_class_count,
        'Pass Class Count': pass_class_count,
        'Overall Pass Percentage': round(pass_percentage, 2)
    }

    # Subject Wise Analysis
    # Group by Subject Name
    subject_metrics = []
    
    if not df_subjects.empty:
        grouped = df_subjects.groupby('Subject Name')
        
        for name, group in grouped:
            appeared = len(group)
            passed = len(group[group['Subject Result'] == 'P'])
            failed = appeared - passed
            pass_pct = (passed / appeared * 100) if appeared > 0 else 0
            
            # Distinction: >= 75% of Subject Max
            # First Class: >= 60% and < 75% of Subject Max
            
            def check_grade(row, lower, upper=None):
                total = row.get('Subject Total', 0)
                max_m = row.get('Subject Max', 0)
                if max_m == 0: return False # avoid div by zero
                pct = (total / max_m) * 100
                if upper:
                    return pct >= lower and pct < upper
                return pct >= lower

            distinctions = len(group[group.apply(lambda x: check_grade(x, 75), axis=1)])
            first_classes = len(group[group.apply(lambda x: check_grade(x, 60, 75), axis=1)])
            
            subject_metrics.append({
                'Subject Name': name,
                'Students Appeared': appeared,
                'Passed': passed,
                'Failed': failed,
                'Pass Percentage': round(pass_pct, 2),
                'Distinction Count': distinctions,
                'First Class Count': first_classes
            })
            
    subject_metrics_df = pd.DataFrame(subject_metrics)
    
    return student_metrics, subject_metrics_df
