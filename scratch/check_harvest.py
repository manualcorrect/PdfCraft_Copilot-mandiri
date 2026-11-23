import pdfplumber

def check_file(label, path):
    print(f"=== {label}: {path} ===")
    with pdfplumber.open(path) as pdf:
        items = []
        for p_idx, page in enumerate(pdf.pages):
            words = page.extract_words()
            min_top = 320 if p_idx == 0 else 200
            table_words = [w for w in words if min_top <= w['top'] <= 800]
            wibs = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
            for ww in wibs:
                time_w = [w['text'] for w in table_words if abs(w['top'] - ww['top']) < 3 and w['x1'] <= ww['x0'] + 1]
                t_str = f"{time_w[-1]} WIB" if time_w else "12:00:00 WIB"
                desc_words = sorted([w for w in table_words if abs(w['top'] - ww['top']) < 22 and 115 <= w['x0'] <= 365], key=lambda x: (x['top'], x['x0']))
                lines = []
                curr_l = []
                curr_y = None
                for w in desc_words:
                    if curr_y is None or abs(w['top'] - curr_y) < 4:
                        curr_l.append(w['text'])
                        curr_y = w['top'] if curr_y is None else (curr_y * 0.7 + w['top'] * 0.3)
                    else:
                        lines.append(' '.join(curr_l))
                        curr_l = [w['text']]
                        curr_y = w['top']
                if curr_l:
                    lines.append(' '.join(curr_l))
                desc_text = '\n'.join(lines)
                items.append((t_str, desc_text))
        print(f"Found {len(items)} items. Total={len(items)}")
        if items:
            print(f"  Item 1: {items[0]}")
            if len(items) > 21:
                print(f"  Item 22: {items[21]}")
            print(f"  Last Item: {items[-1]}")

check_file('AUG', r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_PERFECT.pdf')
check_file('SEP', r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_SEP_2026_PERFECT.pdf')
check_file('OCT', r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\REK_GALANG_OCT_2026_PERFECT.pdf')
