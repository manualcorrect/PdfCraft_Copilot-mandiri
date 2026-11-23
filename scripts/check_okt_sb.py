import pdfplumber

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\okt\0.pdf"

with pdfplumber.open(pdf_path) as pdf:
    p1 = pdf.pages[0]
    words = p1.extract_words()
    sb_words = [w for w in words if 280 <= w['x0'] <= 580 and 150 <= w['top'] <= 260]
    sb_words.sort(key=lambda w: (round(w['top'], 1), w['x0']))
    current_top = None
    line = []
    for w in sb_words:
        top_round = round(w['top'], 1)
        if current_top is None or abs(top_round - current_top) < 3:
            line.append(w['text'])
            current_top = top_round
        else:
            print(f"Top {current_top:5.1f}: {' '.join(line)}")
            line = [w['text']]
            current_top = top_round
    if line:
        print(f"Top {current_top:5.1f}: {' '.join(line)}")
