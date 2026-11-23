import pdfplumber

pdf_source = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf"
with pdfplumber.open(pdf_source) as pdf:
    for idx, page in enumerate(pdf.pages):
        text = page.extract_text()
        first_few_lines = text.split("\n")[:10]
        print(f"=== 2.pdf Page {idx+1} ===")
        for l in first_few_lines:
            print("  ", l)
