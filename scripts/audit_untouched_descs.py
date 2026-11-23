import pdfplumber

pdf_path = r"output\REK_GALANG_AUG_2026_STANDARDIZED.pdf"

print("==================================================")
print("     AUDIT OF UNTOUCHED AUTHENTIC DESCRIPTIONS    ")
print("==================================================")

with pdfplumber.open(pdf_path) as pdf:
    tx_cursor = 0
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        min_top = 320 if p_idx == 0 else 200
        table_words = [w for w in words if min_top <= w['top'] <= 800]
        row_nos = sorted([w for w in table_words if 15 <= w['x0'] <= 35 and w['text'].isdigit()], key=lambda x: x['top'])
        
        for r_w in row_nos:
            r_top = r_w['top']
            r_no = int(r_w['text'])
            tx_cursor += 1
            
            # Extract desc words
            desc_words = sorted([w for w in table_words if abs(w['top'] - r_top) < 22 and 120 <= w['x0'] <= 365], key=lambda x: (x['top'], x['x0']))
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
            
            first_line = lines[0] if lines else "EMPTY"
            print(f"Row {r_no:02d} | Lines: {len(lines)} | First line: {first_line:35} | Total words: {len(desc_words)}")
            if r_no in [10, 22]:
                print(f"   >>> Full text of Row {r_no:02d}: {repr(lines)}")

print(f"\nTotal audited: {tx_cursor}")
