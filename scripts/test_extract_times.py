import os
import sys
import pdfplumber

pdf_source = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf"
authentic_items = []
with pdfplumber.open(pdf_source) as pdf:
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        min_top = 320 if p_idx == 0 else 200
        table_words = [w for w in words if min_top <= w["top"] <= 800]
        
        wib_words = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        for ww in wib_words:
            time_token = [w['text'] for w in table_words if abs(w['top'] - ww['top']) < 3 and w['x1'] <= ww['x0'] + 1]
            date_tokens = [w['text'] for w in table_words if 0 < (ww['top'] - w['top']) < 15 and 45 <= w['x0'] <= 90]
            desc_w = [w for w in table_words if abs(w['top'] - ww['top']) < 22 and 115 <= w['x0'] <= 360]

            t_str = f"{time_token[-1]} WIB" if time_token else "12:00:00 WIB"
            d_str = " ".join(date_tokens).replace("Jan", "Aug").strip()
            desc_text = " ".join(w["text"] for w in desc_w)

            authentic_items.append({
                "page": p_idx + 1,
                "date": d_str,
                "time": t_str,
                "desc": desc_text[:30]
            })

print(f"Total authentic items: {len(authentic_items)}")
for idx, it in enumerate(authentic_items):
    print(f"[{idx+1:02d}] P{it['page']} Date: {it['date']} | Time: {it['time']} | Desc: {it['desc']}")
