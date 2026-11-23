import pdfplumber

target = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_FINAL.pdf"

with pdfplumber.open(target) as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    # check Page 1 Header
    words = pdf.pages[0].extract_words()
    name_words = [w['text'] for w in words if w['top'] < 130 and 120 <= w['x0'] <= 220]
    print(f"Header: {name_words}")
    
    # check Row 10 description
    table_words = [w for w in words if 320 <= w['top'] <= 800]
    r10_w = [w for w in table_words if 15 <= w['x0'] <= 35 and w['text'] == '10'][0]
    desc10 = [w['text'] for w in table_words if abs(w['top'] - r10_w['top']) < 22 and 120 <= w['x0'] <= 365]
    print(f"Row 10 desc: {' '.join(desc10)}")
    
    # check Page 2 Row 22 description
    words2 = pdf.pages[1].extract_words()
    table_words2 = [w for w in words2 if 200 <= w['top'] <= 800]
    r22_w = [w for w in table_words2 if 15 <= w['x0'] <= 35 and w['text'] == '22'][0]
    desc22 = [w['text'] for w in table_words2 if abs(w['top'] - r22_w['top']) < 22 and 120 <= w['x0'] <= 365]
    print(f"Row 22 desc: {' '.join(desc22)}")
