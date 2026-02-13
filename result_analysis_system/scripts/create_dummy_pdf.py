from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def create_dummy_pdf(filename="sample_marksheet.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 50, "MAHARASHTRA STATE BOARD OF TECHNICAL EDUCATION")
    
    # Student Details
    c.setFont("Helvetica", 12)
    y = height - 100
    c.drawString(50, y, "MR. PATIL ROHIT RAMESH")
    c.drawString(400, y, "Enrollment No: 1900123456")
    y -= 20
    c.drawString(50, y, "Seat No: 223344")
    c.drawString(400, y, "Course: CO6I")
    
    # Headers
    y -= 40
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "SUBJECT NAME")
    c.drawString(250, y, "TH")
    c.drawString(300, y, "PR")
    c.drawString(350, y, "SLA")
    c.drawString(400, y, "TOT")
    c.drawString(450, y, "CR")
    c.drawString(500, y, "RSLT")
    
    # Subject Data
    subjects = [
        ("Management", "70", "00", "20", "90", "3", "P"),
        ("Software Testing", "65", "22", "18", "105", "5", "P"),
        ("Advanced Java", "55", "35", "15", "105", "6", "P"),
        ("Operating System", "45", "40", "15", "100", "5", "P"),
        ("Environmental Studies", "00", "00", "45", "45", "2", "P"), # Only SLA
    ]
    
    y -= 20
    c.setFont("Helvetica", 10)
    for sub in subjects:
        c.drawString(50, y, sub[0])
        c.drawString(250, y, sub[1])
        c.drawString(300, y, sub[2])
        c.drawString(350, y, sub[3])
        c.drawString(400, y, sub[4])
        c.drawString(450, y, sub[5])
        c.drawString(500, y, sub[6])
        y -= 20
        
    # Total & Result
    y -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Total Marks: 550")
    c.drawString(250, y, "Percentage: 76.50%")
    c.drawString(450, y, "Result: FIRST CLASS DIST.") # Keep consistent with regex
    
    c.save()
    print(f"Created {filename}")

if __name__ == "__main__":
    create_dummy_pdf()
