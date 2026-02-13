import re

def parse_student_details(text):
    """
    Parses student details (Name, Enrollment, Seat, etc.) from text.
    """
    data = {}
    
    # 1. Name: MR. / MS. <NAME>
    # Try multiple patterns for robustness
    name_match = re.search(r"MR\.\s*/\s*MS\.\s+([A-Z\s]+?)(?=\s+ENROLLMENT|\n)", text)
    if not name_match:
        name_match = re.search(r"(?:MR\.|MS\.)\s+([A-Z\s]+?)(?=\s+Enrollment|\s*$)", text)
    if not name_match:
         name_match = re.search(r"Name\s*:\s*([A-Z\s]+)", text, re.IGNORECASE)

    data['Name'] = name_match.group(1).strip() if name_match else "Unknown"

    # 2. Enrollment No
    enroll_match = re.search(r"ENROLLMENT NO[\.:]\s*(\d+)", text, re.IGNORECASE)
    data['Enrollment No'] = enroll_match.group(1).strip() if enroll_match else "Unknown"

    # 3. Seat No
    seat_match = re.search(r"SEAT NO[\.:]\s*(\d+)", text, re.IGNORECASE)
    data['Seat No'] = seat_match.group(1).strip() if seat_match else "Unknown"
    
    # 4. Course
    course_match = re.search(r"COURSE\s+(.+?)(?=\s+THEORY|\n)", text, re.IGNORECASE)
    if not course_match:
        course_match = re.search(r"Course:\s*([A-Z0-9]+)", text)
    data['Course'] = course_match.group(1).strip() if course_match else "Unknown"

    # 5. Result/Class (Bottom of file often)
    # Look for "A.T.K.T." or "FIRST CLASS" etc.
    result_match = re.search(r"(?:FIRST CLASS|SECOND CLASS|PASS|FAIL|A\.T\.K\.T\.|DISTINCTION)", text)
    data['Class'] = result_match.group(0).strip() if result_match else "Unknown"
    
    # Map Class to specific format if needed, but keeping it as extracted is safer for now.

    # 6. Total Marks & Percentage
    # "SECRETARY 850 526 12" -> Max Obt Credit
    totals_match = re.search(r"SECRETARY\s+(\d+)\s+(\d+)", text)
    if totals_match:
        data['Total Marks'] = totals_match.group(1)
        data['Obtained Marks'] = totals_match.group(2) # Helper field
        try:
            pct = (int(data['Obtained Marks']) / int(data['Total Marks'])) * 100
            data['Percentage'] = f"{pct:.2f}"
        except:
            data['Percentage'] = "0.00"
    else:
        # Fallback to old regex
        total_marks_match = re.search(r"Total Marks:\s*(\d+)", text)
        percentage_match = re.search(r"Percentage:\s*([\d\.]+)", text)
        
        data['Total Marks'] = total_marks_match.group(1).strip() if total_marks_match else "0"
        data['Percentage'] = percentage_match.group(1).strip() if percentage_match else "0.00"

    return data

def parse_subject_marks(text):
    """
    Parses subject-wise marks from text.
    """
    subjects = []
    lines = text.split('\n')
    
    merged_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            i += 1
            continue
            
        # Explicitly skip known headers from being start of merge
        if "TITLE OF SUBJECTS" in line or "MAX OBT" in line or "SECRETARY" in line:
            merged_lines.append(line)
            i += 1
            continue

        # Check if line seems to be just a name (no digits at end)
        # And next line is marks (digits)
        # Regex check: Line consists of Upper Case text/spaces only
        if re.match(r"^[A-Z\s\(\)\+\-]+$", line) and i+1 < len(lines) and re.search(r"\d+\s*$", lines[i+1]):
             merged = line + " " + lines[i+1]
             merged_lines.append(merged)
             i += 2
        else:
             merged_lines.append(line)
             i += 1
             
    for line in merged_lines:
        line = line.strip()
        if not line: continue

        # Ignore lines like header lines
        if "TITLE OF SUBJECTS" in line or "MAX OBT" in line or "SECRETARY" in line:
            continue
            
        # Must end with digit (Credits)
        if not re.search(r"\s\d+$", line):
            continue
            
        # Pattern: sequence of (number|--)[*]?
        match = re.search(r"((?:(?:[\d\-]+)[*#@]?\s+)+)(\d+)$", line)
        if match:
            marks_str = match.group(1)
            credits = match.group(2)
            name = line[:match.start()].strip()
            
            # Parsing Marks
            tokens = marks_str.split()
            cleaned_tokens = [t.strip('*#@') for t in tokens]
            
            subject_total = 0
            subject_max = 0
            
            # Simple heuristic matching the user data:
            # Skip Pair 0 and Pair 1 (FA-TH, SA-TH) if we suspect standard structure
            # But handle "- -" cases.
            
            # Implementation:
            # Iterate pairs.
            # If pair_index == 0 or pair_index == 1: Skip.
            # Else: Add to total.
            
            num_pairs = len(cleaned_tokens) // 2
            
            for p in range(num_pairs):
                # Max value at 2*p, OBT value is at 2*p + 1
                max_val_str = cleaned_tokens[2*p]
                obt_val_str = cleaned_tokens[2*p + 1]
                
                # Skip FA-TH and SA-TH (Indices 0, 1)
                # But only if we have enough pairs to imply specific structure?
                if p < 2:
                    continue
                    
                if obt_val_str == '-' or obt_val_str == '--':
                    continue
                    
                try:
                    subject_total += int(obt_val_str)
                    if max_val_str != '-' and max_val_str != '--':
                        subject_max += int(max_val_str)
                except:
                    pass
            
            # Determine Result
            subject_result = 'P'
            if '*' in marks_str:
                subject_result = 'F'
            
            subjects.append({
                'Subject Name': name,
                'Subject Total': subject_total,
                'Subject Max': subject_max,
                'Credits': int(credits),
                'Subject Result': subject_result
            })
            
    return subjects
