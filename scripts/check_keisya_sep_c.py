import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\REK_KEISYA_SEP_OUTPUT_1.pdf") as pdf:
    p1 = pdf.pages[0]
    words = [w for w in p1.extract_words() if 110 <= w['top'] <= 140 and w['x0'] < 300]
    for w in words:
        print(f"Keisya Sep Branch word: '{w['text']}' top={w['top']} x0={w['x0']} x1={w['x1']}")
    
    chars = [c for c in p1.chars if 110 <= c['top'] <= 140 and c['x0'] < 300]
    for c in chars:
        print(f"Char '{c['text']}' font={c.get('fontname')}")
