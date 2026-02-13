
import re


text = """1/27/25, 3:29 PM about:blank
Maharashtra State Board of Technical Education
STATEMENT OF MARKS
MR. / MS. RAJPUT BHAGYASHRI PRAVIN
ENROLLMENT NO. 23611180254 EXAMINATION 202411 SEAT NO. 408777 THIRD SEMESTER
COURSE Diploma In Computer Engineering
THEORY PRACTICALS
SLA
TITLE OF SUBJECTS FA-TH SA-TH TOTAL FA-PR SA-PR CREDITS
MAX OBT MAX OBT MAX OBT MAX OBT MAX OBT MAX OBT
DATA STRUCTURE USING C 30 020 70 031 100 051 50 041 25 021 - - 4
DATABASE MANAGEMENT SYSTEM 30 018 70 035 100 053 50 041 25 021 25 021 5
DIGITAL TECHNIQUES 30 014 70 013* 100 027* 25 022 25 021 25 021 0
OBJECT ORIENTED PROGRAMMING
30 015 70 016* 100 031* 50 040 25 018 25 017 0
USING C++
COMPUTER GRAPHICS - - - - - - 25 020 - - 25 020 2
ESSENCE OF INDIAN CONSTITUTION - - - - - - - - - - 50 040 1
TOTAL MAX. TOTAL MARKS PERCENTAGE
DATE : This Marksheet is Downloaded from Internet MARKS OBTAINED % TOTAL CREDIT
27/01/2025
SECRETARY 850 526 12
MAHARASHTRA STATE BOARD OF TECHNICAL EDUCATION
4/0369/CO3K A.T.K.T.
INSTRUCTIONS"""

def parse_student_details(text):
    data = {}
    
    # 1. Name: MR. / MS. <NAME>
    name_match = re.search(r"MR\.\s*/\s*MS\.\s+([A-Z\s]+?)(?=\s+ENROLLMENT|\n)", text)
    data['Name'] = name_match.group(1).strip() if name_match else "Unknown"

    # 2. Enrollment No
    enroll_match = re.search(r"ENROLLMENT NO\.\s*(\d+)", text)
    data['Enrollment No'] = enroll_match.group(1).strip() if enroll_match else "Unknown"

    # 3. Seat No
    seat_match = re.search(r"SEAT NO\.\s*(\d+)", text)
    data['Seat No'] = seat_match.group(1).strip() if seat_match else "Unknown"
    
    # 4. Course
    course_match = re.search(r"COURSE\s+(.+?)(?=\s+THEORY|\n)", text)
    data['Course'] = course_match.group(1).strip() if course_match else "Unknown"

    # 5. Result/Class (Bottom of file often)
    # Look for "A.T.K.T." or "FIRST CLASS" etc.
    # In this text: "4/0369/CO3K A.T.K.T."
    result_match = re.search(r"(?:FIRST CLASS|SECOND CLASS|PASS|FAIL|A\.T\.K\.T\.|DISTINCTION)", text)
    data['Result'] = result_match.group(0).strip() if result_match else "Unknown"
    # Map Result to Class if needed, or just use as is.

    # 6. Total Marks & Percentage -> often not explicitly labeled cleanly in this mess
    # "SECRETARY 850 526 12" -> Max Obt Credit
    # We can regex for this pattern near "SECRETARY"
    totals_match = re.search(r"SECRETARY\s+(\d+)\s+(\d+)", text)
    if totals_match:
        data['Total Marks'] = totals_match.group(1)
        data['Obtained Marks'] = totals_match.group(2)
        try:
            pct = (int(data['Obtained Marks']) / int(data['Total Marks'])) * 100
            data['Percentage'] = f"{pct:.2f}"
        except:
            data['Percentage'] = "0.00"
    else:
        data['Total Marks'] = "0"
        data['Percentage'] = "0.00"

    return data

def parse_subject_marks(text):
    subjects = []
    lines = text.split('\n')
    
    # Logic: Look for lines ending in a single digit (Credit).
    # And having multiple numbers in between.
    
    # Regex for a subject line:
    # Starts with Name (A-Z chars)
    # Has sequence of numbers/dashes/stars
    # Ends with single digit
    
    # We need to handle split lines. "OBJECT ORIENTED PROGRAMMING" \n "30..."
    # Iterate and merge lines if next line looks like marks but curr line is just text?
    
    merged_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines
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
        if re.match(r"^[A-Z\s]+$", line) and i+1 < len(lines) and re.search(r"\d+\s*$", lines[i+1]):

             merged = line + " " + lines[i+1]
             merged_lines.append(merged)
             i += 2
        else:
             merged_lines.append(line)
             i += 1
             
    for line in merged_lines:
        line = line.strip()
        if not line: continue
        
        # Regex: Name ... nums ... credit
        # Ignore lines like header lines
        if "TITLE OF SUBJECTS" in line or "MAX OBT" in line or "SECRETARY" in line:
            continue
            
        # Match ends with digit
        if not re.search(r"\s\d+$", line):
            print(f"Skipping line (no ending digit): {line}")
            continue
            
        # Parse logic
        # Split by spaces?
        # Name can have spaces. Marks have spaces.
        # Strategy: matching marks sequence at end, rest is name.
        
        # Pattern: sequence of (number|--)[*]?
        # (?:(?:[\d\-]+)[*#@]?\s+)+(\d+)$
        
        match = re.search(r"((?:(?:[\d\-]+)[*#@]?\s+)+)(\d+)$", line)
        if match:
            marks_str = match.group(1)
            credits = match.group(2)
            name = line[:match.start()].strip()
            
            # Check for failure symbol *
            subject_result = 'P'
            if '*' in marks_str:
                subject_result = 'F'
                
            print(f"Matched: {name} -> Marks: {marks_str} Credits: {credits} Result: {subject_result}")
            
            # Now parse marks_str
            # "30 020 70 031 100 051 50 041 25 021 - - "
            tokens = marks_str.split()
            
            # Clean tokens (remove *)
            cleaned_tokens = [t.strip('*#@') for t in tokens]
            
            # Map columns? 
            # We want Subject Total.
            # If 3rd pair exists (Total TH), index 5 (0-based) -> token[5]
            # But "Graphics" has - - ...
            
            # Heuristic: Sum of obtained marks (even indices: 1, 3, 5...)??
            # NO. Header: MAX OBT.
            # So OBT is at indices 1, 3, 5...
            
            # Indexes:
            # 0: FA-TH Max, 1: FA-TH Obt
            # 2: SA-TH Max, 3: SA-TH Obt
            # 4: TOT-TH Max, 5: TOT-TH Obt
            
            # If we sum 1 and 3, we get 5. So don't sum 1,3,5. Just take 5.
            # BUT for practicals?
            # 6: FA-PR Max, 7: FA-PR Obt
            # 8: SA-PR Max, 9: SA-PR Obt
            
            # Logic:
            # If token[4] is '100' or similar (Total Column?), take token[5].
            # Then add token[7], token[9]...
            
            # Simple approach: 
            # Identify "Total" columns vs "Component" columns.
            # In this sheet, TH Total is explicit. PR Totals are components.
            # List of Obt indices to sum:
            # If TH exists: Index 5 (Total TH) + Index 7 (FA-PR) + Index 9 (SA-PR) + ...
            # If TH is "--": Index 5 is "--".
            # Check for "-":
            
            # Let's count pairs.
            # Data Struct: 12 tokens. (6 pairs).
            # 51 is at index 5. 
            # 41 at 7. 21 at 9. 
            # Total = 51 + 41 + 21 = 113.
            
            # Graphics: "- - - - - - 25 020 - - 25 020"
            # Tokens: -, -, -, -, -, -, 25, 020, -, -, 25, 020.
            # Index 5 is "-".
            # So we sum components?
            # Index 1 (-), 3 (-), 5 (-).
            # Index 7 (020). Index 9 (-). Index 11 (020).
            # Total = 20 + 20 = 40.
            
            # Algorithm:
            # Iterate pairs (Max, Obt).
            # If Pair 3 (Total TH) is valid number: Use it. Skip Pair 1 & 2.
            # Else: Use Pair 1 & 2 (if valid).
            # Add all other Pairs (Pair 4 onwards).
            
            # Wait, Pair 3 is SUM of 1 & 2.
            # So generally: Just take Pair 3 + Pair 4 + Pair 5...
            # If Pair 3 is '-', take Pair 1 + Pair 2 + Pair 4 + ...
            # Actually, if Pair 3 is '-', then Pair 1 & 2 are likely '-' too (verified in Graphics).
            # So simply: Sum all OBT tokens, EXCEPT Pair 1 & Pair 2.
            # Parsing Marks
            tokens = marks_str.split()
            cleaned_tokens = [t.strip('*#@') for t in tokens]
            
            subject_total = 0
            subject_max = 0
            
            # Implementation:
            # Iterate pairs of (Max, Obt).
            # Max value is at 2*p
            # OBT value is at 2*p + 1
            
            num_pairs = len(cleaned_tokens) // 2
            
            for p in range(num_pairs):
                # Max value at 2*p, Obt value at 2*p + 1
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
                    # Helper: if Max is also a number, add it.
                    # Max might be '-' if Obt is valid? Unlikely.
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


print("--- parsed data ---")
print(parse_student_details(text))
print("--- parsed subjects ---")
print(parse_subject_marks(text))
