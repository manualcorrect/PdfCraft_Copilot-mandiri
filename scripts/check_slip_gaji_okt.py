import pdfplumber

slip_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\SLIP GAJI 1026 KEISYA AULIA.pdf"
with pdfplumber.open(slip_path) as pdf:
    for i, p in enumerate(pdf.pages):
        print(f"--- Page {i+1} ---")
        print(p.extract_text())
