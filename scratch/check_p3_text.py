import pdfplumber

pdf_path = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\scratch\test_desc_edit.pdf"
with pdfplumber.open(pdf_path) as pdf:
    p3 = pdf.pages[2]
    print(p3.extract_text())
