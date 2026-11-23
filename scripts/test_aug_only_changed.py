import os
import sys
import shutil

sys.path.insert(0, os.path.abspath("src"))
from pdfcraft_client import PdfCraftClient
import pdfplumber

src_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_FINAL.pdf"
test_pdf = "output/test_aug_only_changed.pdf"
shutil.copyfile(src_pdf, test_pdf)

# Only the changed rows:
# Mapping: (page, row_in_page, global_row_1based): (text, ideal_width)
changed_rows = {
    # Page 1
    (1, 4, 5): ("Biaya transfer BI Fast", 80.0),
    (1, 5, 6): ("Transfer BI Fast\nKe BCA\nBUDI SAPUTRA TANAGUN 1010570065", 150.0),
    (1, 6, 7): ("Transfer ke BANK MANDIRI\nMEI DWI LESTARI 1370011851231", 130.0),
    (1, 9, 10): ("Transfer BI Fast\nDari BANK BNI\nFITRIANA PURWANINGSI 0314467254", 145.0),
    # Page 2
    (2, 4, 15): ("Transfer dari BANK MANDIRI\nNANDA FEBRIANTI 1370013797036", 135.0),
    (2, 11, 22): ("Transfer BI Fast\nDari BCA\nPT BENDI NASHA NIAGA INDUSTRI 5411078192\n(CENAIDJA)", 175.0),
    # Page 3
    (3, 3, 26): ("Penarikan tunai di ATM BANK\nMANDIRI SRG IM CIRUAS 01", 120.0),
    (3, 6, 29): ("Pembayaran QR ke\nwarung madura\n506115913713", 80.0),
    (3, 7, 30): ("Penarikan tunai di ATM BANK\nMANDIRI SRG IM CIRUAS 01", 120.0),
    (3, 10, 33): ("Biaya transfer BI Fast\n-", 80.0),
    (3, 11, 34): ("Transfer BI Fast\nKe BCA\nLUKMAN 1011284251", 85.0),
}

with PdfCraftClient() as client:
    doc_id = client.doc_open(test_pdf)
    
    for (p_num, r_i, g_row), (text, width) in changed_rows.items():
        base_y = 343.92 if p_num == 1 else 227.92
        row_y = base_y + r_i * 46.00
        lines = text.split("\n")
        num_lines = len(lines)
        target_top = row_y - (num_lines - 1) * 5.0
        
        paras = client.get_paragraphs(doc_id, page=p_num)
        p_desc = [p for p in paras if abs(p["rect"][1] - row_y) < 22 and 120 <= p["rect"][0] <= 135]
        assert p_desc, f"Paragraph not found for row {g_row} (P{p_num}:{r_i+1})"
        p_obj = p_desc[0]
        
        # Empty any lingering sub-lines in this row
        extra_min_y = row_y - 20
        extra_max_y = row_y + 25
        extra_paras = [p for p in paras if extra_min_y <= p["rect"][1] <= extra_max_y and 120 <= p["rect"][0] <= 135 and p["paragraph"] != p_obj["paragraph"]]
        for ep in extra_paras:
            client.edit_text(doc_id, page=p_num, paragraph=ep["paragraph"], text="")

        # Edit text
        client.call_tool("text_edit", {
            "doc": doc_id,
            "page": p_num,
            "paragraph": p_obj["paragraph"],
            "text": text,
            "width": width,
            "line_spacing": 1.25
        })
        
        # Adjust position
        up = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_obj["paragraph"]][0]
        dx = 124.00 - up["rect"][0]
        dy = up["rect"][1] - target_top
        
        kwargs_shift = {}
        if abs(dx) > 0.05: kwargs_shift["dx"] = dx
        if abs(dy) > 0.05: kwargs_shift["dy"] = dy
        if kwargs_shift:
            client.edit_text(doc_id, page=p_num, paragraph=p_obj["paragraph"], **kwargs_shift)

    client.doc_save(doc_id, path=test_pdf, full=True)
    client.doc_close(doc_id)

print("\n=== VERIFYING ALL 37 ROWS IN test_aug_only_changed.pdf ===")
page_row_counts = [10, 12, 12, 3]
cursor = 0
all_perfect = True
with pdfplumber.open(test_pdf) as pdf:
    for p_num, count in enumerate(page_row_counts, 1):
        words = pdf.pages[p_num - 1].extract_words()
        base_y = 343.92 if p_num == 1 else 227.92
        print(f"\n--- Page {p_num} ---")
        for r_i in range(count):
            cursor += 1
            row_y = base_y + r_i * 46.00
            
            row_words = [w for w in words if 115 <= w["x0"] <= 365 and abs(w["top"] - row_y) < 22]
            lines = {}
            for w in row_words:
                lk = round(w["top"], 1)
                lines.setdefault(lk, []).append(w["text"])
                
            first_top = min(lines.keys()) if lines else 0
            first_x0 = min([w["x0"] for w in row_words]) if row_words else 0
            num_l = len(lines)
            
            print(f"Tx {cursor:02d} | lines={num_l} | x0={first_x0:.2f} | top={first_top:.2f}")
            for top in sorted(lines.keys()):
                print(f"     top={top:5.1f}: {' '.join(lines[top])}")
