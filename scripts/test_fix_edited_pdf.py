import os
import sys
import shutil

sys.path.insert(0, os.path.abspath("src"))
from pdfcraft_client import PdfCraftClient
import pdfplumber

src_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_edited ketengangan.pdf"
test_pdf = "output/test_fix_edited_pdf.pdf"
shutil.copyfile(src_pdf, test_pdf)

# Chronological dates for rows 23-27
# Row 23: 25 Aug 2026 (was 20 Aug)
# Row 24: 25 Aug 2026 (was 20 Aug)
# Row 25: 25 Aug 2026 (was 20 Aug)
# Row 26: 26 Aug 2026 (was 21 Aug)
# Row 27: 26 Aug 2026 (was 21 Aug)
date_updates = {
    # (page, row_in_page_1based): new_date
    (3, 1): "25 Aug 2026",
    (3, 2): "25 Aug 2026",
    (3, 3): "25 Aug 2026",
    (3, 4): "26 Aug 2026",
    (3, 5): "26 Aug 2026",
}

with PdfCraftClient() as client:
    doc_id = client.doc_open(test_pdf)
    
    # 1. Update Dates on Page 3
    for (p_num, r_idx), new_d in date_updates.items():
        row_y = 227.92 + (r_idx - 1) * 46.00
        paras = client.get_paragraphs(doc_id, page=p_num)
        p_dates = [p for p in paras if 45 <= p["rect"][0] <= 85 and abs(p["rect"][1] - (row_y - 4.0)) < 10.0 and "WIB" not in p["text"]]
        if p_dates:
            print(f"Updating Date P{p_num} Row {r_idx}: '{p_dates[0]['text']}' -> '{new_d}'")
            client.edit_text(doc_id, page=p_num, paragraph=p_dates[0]["paragraph"], text=new_d)
            # ensure x0 = 52.00
            up = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_dates[0]["paragraph"]][0]
            dx = 52.00 - up["rect"][0]
            if abs(dx) > 0.05:
                client.edit_text(doc_id, page=p_num, paragraph=p_dates[0]["paragraph"], dx=dx)

    # 2. Fix Keterangan position and alignment across all pages
    page_row_counts = [10, 12, 12, 3]
    for p_num, count in enumerate(page_row_counts, 1):
        base_y = 343.92 if p_num == 1 else 227.92
        for r_i in range(count):
            row_y = base_y + r_i * 46.00
            paras = client.get_paragraphs(doc_id, page=p_num)
            
            # Find main description paragraph in this row
            p_desc = [p for p in paras if abs(p["rect"][1] - row_y) < 22 and 120 <= p["rect"][0] <= 135 and p["text"].strip() != "-"]
            if p_desc:
                p_obj = p_desc[0]
                lines = [l for l in p_obj.get("editor_text", p_obj["text"]).split("\n") if l.strip()]
                num_lines = len(lines)
                
                # Check if there is an extra trailing '-' paragraph (like in Row 31, 33 on page 3, or Row 35 on page 4)
                extra_dash = [p for p in paras if abs(p["rect"][1] - row_y) < 25 and 120 <= p["rect"][0] <= 135 and p["text"].strip() == "-"]
                if extra_dash:
                    num_lines += 1 # includes the dash
                    
                target_top = row_y - (num_lines - 1) * 5.0
                
                # Calculate dy and dx
                # Note: up["rect"][1] is top coordinate
                # dy > 0 moves up (decreases top), dy < 0 moves down (increases top)
                dx = 124.00 - p_obj["rect"][0]
                dy = p_obj["rect"][1] - target_top
                
                kwargs = {}
                if abs(dx) > 0.05: kwargs["dx"] = dx
                if abs(dy) > 0.05: kwargs["dy"] = dy
                
                if kwargs:
                    print(f"P{p_num} R{r_i+1}: adjusting main desc by dx={kwargs.get('dx', 0):.2f}, dy={kwargs.get('dy', 0):.2f}")
                    client.edit_text(doc_id, page=p_num, paragraph=p_obj["paragraph"], **kwargs)
                    
                if extra_dash:
                    dash_obj = extra_dash[0]
                    # Target top for dash is target_top + (num_lines - 1) * 10.0
                    target_dash_top = target_top + (num_lines - 1) * 10.0
                    dx_dash = 124.00 - dash_obj["rect"][0]
                    dy_dash = dash_obj["rect"][1] - target_dash_top
                    kwargs_dash = {}
                    if abs(dx_dash) > 0.05: kwargs_dash["dx"] = dx_dash
                    if abs(dy_dash) > 0.05: kwargs_dash["dy"] = dy_dash
                    if kwargs_dash:
                        print(f"P{p_num} R{r_i+1}: adjusting dash by dx={kwargs_dash.get('dx', 0):.2f}, dy={kwargs_dash.get('dy', 0):.2f}")
                        client.edit_text(doc_id, page=p_num, paragraph=dash_obj["paragraph"], **kwargs_dash)

    # 3. Ensure Account Number on Page 1 is x0=160.00
    paras = client.get_paragraphs(doc_id, page=1)
    p_acc = [p for p in paras if "1630016287487" in p["text"] and 180 <= p["rect"][1] <= 200]
    if p_acc:
        dx = 160.00 - p_acc[0]["rect"][0]
        if abs(dx) > 0.05:
            print(f"Adjusting account number by dx={dx:.2f}")
            client.edit_text(doc_id, page=1, paragraph=p_acc[0]["paragraph"], dx=dx)

    client.doc_save(doc_id, path=test_pdf, full=True)
    client.doc_close(doc_id)

print("\n=== VERIFYING RESULTING POSITIONS AND DATES ===")
with pdfplumber.open(test_pdf) as pdf:
    cursor = 0
    for p_num, count in enumerate(page_row_counts, 1):
        words = pdf.pages[p_num - 1].extract_words()
        base_y = 343.92 if p_num == 1 else 227.92
        print(f"\n================ PAGE {p_num} ================")
        wibs = sorted([w for w in words if w['text'] == 'WIB' and w['top'] > 200], key=lambda x: x['top'])
        for r_i, w in enumerate(wibs):
            cursor += 1
            row_y = base_y + r_i * 46.00
            
            # date
            date_words = [d['text'] for d in words if 0 < (w['top'] - d['top']) < 15 and 45 <= d['x0'] <= 95]
            time_words = [t['text'] for t in words if abs(t['top'] - w['top']) < 3 and t['x1'] <= w['x0'] + 1]
            date_str = " ".join(date_words)
            time_str = " ".join(time_words) + " WIB"
            
            row_words = [cw for cw in words if 115 <= cw['x0'] <= 365 and abs(cw['top'] - row_y) < 22]
            lines = {}
            for cw in sorted(row_words, key=lambda x: (x['top'], x['x0'])):
                lines.setdefault(round(cw['top'], 1), []).append(cw['text'])
            first_top = min(lines.keys()) if lines else 0
            first_x0 = min([cw['x0'] for cw in row_words]) if row_words else 0
            diff = first_top - row_y
            
            print(f"Tx {cursor:02d} | {date_str} {time_str} | x0={first_x0:.2f} | top={first_top:.2f} (diff={diff:+.2f}) | {len(lines)} lines")
            for top, ws in sorted(lines.items()):
                print(f"     top={top:5.1f}: {' '.join(ws)}")
