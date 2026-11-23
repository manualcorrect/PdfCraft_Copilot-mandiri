import pdfplumber

target = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_REVISED.pdf"

with pdfplumber.open(target) as pdf:
    print(f"Total pages in revised PDF: {len(pdf.pages)}")
    # Page 1 Header
    words = pdf.pages[0].extract_words()
    header_name = [w['text'] for w in words if w['top'] < 130 and 120 <= w['x0'] <= 220]
    print(f"Page 1 Name/Branch: {header_name}")
    
    # Page 1 First 3 rows
    for r in range(1, 4):
        r_w = [w for w in words if 15 <= w['x0'] <= 35 and w['text'] == str(r)][0]
        d_w = [w['text'] for w in words if abs(w['top'] - (r_w['top'] - 4)) < 4 and 45 <= w['x0'] <= 110]
        t_w = [w['text'] for w in words if abs(w['top'] - (r_w['top'] + 5)) < 4 and 45 <= w['x0'] <= 110]
        print(f"  Row {r}: Date={' '.join(d_w)}, Time={' '.join(t_w)}")

    # Page 2 Row 22 (Gaji)
    words2 = pdf.pages[1].extract_words()
    r22_w = [w for w in words2 if 15 <= w['x0'] <= 35 and w['text'] == '22'][0]
    d22_w = [w['text'] for w in words2 if abs(w['top'] - (r22_w['top'] - 4)) < 4 and 45 <= w['x0'] <= 110]
    t22_w = [w['text'] for w in words2 if abs(w['top'] - (r22_w['top'] + 5)) < 4 and 45 <= w['x0'] <= 110]
    print(f"  Row 22 (Gaji): Date={' '.join(d22_w)}, Time={' '.join(t22_w)}")
