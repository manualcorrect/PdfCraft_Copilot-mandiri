import pdfplumber

pdf_source = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf"

with pdfplumber.open(pdf_source) as pdf:
    tx_idx = 0
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        min_top = 320 if p_idx == 0 else 200
        table_words = [w for w in words if min_top <= w['top'] <= 800]
        
        wib_words = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        for ww in wib_words:
            tx_idx += 1
            desc_words = sorted([w for w in table_words if abs(w['top'] - ww['top']) < 22 and 115 <= w['x0'] <= 365], key=lambda x: (x['top'], x['x0']))
            
            lines = []
            curr_l = []
            curr_y = None
            for w in desc_words:
                if curr_y is None or abs(w['top'] - curr_y) < 4:
                    curr_l.append(w['text'])
                    curr_y = w['top'] if curr_y is None else (curr_y * 0.7 + w['top'] * 0.3)
                else:
                    lines.append(" ".join(curr_l))
                    curr_l = [w['text']]
                    curr_y = w['top']
            if curr_l:
                lines.append(" ".join(curr_l))
                
            raw_desc = "\n".join(lines)
            print(f"--- TX {tx_idx:02d} ---")
            print(raw_desc)
