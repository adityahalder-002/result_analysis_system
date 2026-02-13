import pandas as pd

def process_results(student_data, subject_data):
    """
    Applies MSBTE rules to calculate result and class.
    Args:
        student_data: dict of student details
        subject_data: list of dicts (subjects)
    Returns:
        student_data: updated student data with 'Result' and 'Percentage' verified
    """
    # 1. Subject Pass Rule: Min 40% in each subject
    # Note: 'Subject Result' from PDF is usually 'P' or 'F'.
    # We can rely on it, but we can also re-calculate for safety.
    # MSBTE rule: Subject Total >= 40 (if total is 100) or 40% of Max Marks.
    # Since we extract "Subject Total" and "Subject Result", let's trust "Subject Result" first if present.
    
    is_fail = False
    for sub in subject_data:
        if sub['Subject Result'] == 'F':
            is_fail = True
            break
        
        # Optional: Double check verification
        # Assuming max marks 100 for standard subjects. A bit risky without knowing max marks.
        # But if Marks < 40 and Marks > 0, likely Fail.
        # if sub['Subject Total'] < 40 and sub['Subject Total'] > 0:
        #    is_fail = True

    # 2. Student Result Rule
    # Use the extracted Class/Result from PDF as primary source if available.
    pdf_class = student_data.get('Class', '').upper()
    
    if "FAIL" in pdf_class:
        final_result = "FAIL"
    elif "A.T.K.T." in pdf_class or "ATKT" in pdf_class:
        final_result = "ATKT"
    else:
        # Check subject failures if PDF result is not explicit Fail/ATKT
        # But usually PDF "Result" (which we stored in 'Class' field in parser) is authoritative.
        if is_fail:
             # If calculated fail but PDF says otherwise? Trust PDF usually, but "is_fail" is based on '*'
             # If '*' exists, it should be Fail or ATKT.
             if final_result != "ATKT": # Only override if not already ATKT
                 final_result = "FAIL"
        else:
             final_result = "PASS"

    student_data['Result'] = final_result

    # 3. Class Assignment Logic
    # If the PDF Class is generic (e.g. just "PASS" or "FAIL"), or "Unknown", we might want to calculating it.
    # But usually PDF has "FIRST CLASS", "DISTINCTION" etc.
    # We should normalize what we extracted.
    
    normalized_class = pdf_class
    
    if "DISTINCTION" in pdf_class:
        normalized_class = "First Class with Distinction"
    elif "FIRST CLASS" in pdf_class:
        normalized_class = "First Class"
    elif "SECOND CLASS" in pdf_class:
        normalized_class = "Second Class"
    elif "PASS" in pdf_class:
         normalized_class = "Pass Class"
    elif "FAIL" in pdf_class:
         normalized_class = "Fail"
    elif "A.T.K.T." in pdf_class or "ATKT" in pdf_class:
         normalized_class = "A.T.K.T."
    
    student_data['Class'] = normalized_class
    
    return student_data
