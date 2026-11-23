import os
import sys
import shutil

sys.path.insert(0, os.path.abspath("src"))
from pdfcraft_client import PdfCraftClient
import pdfplumber

src_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_FINAL.pdf"
test_pdf = "output/test_aug_ideal_widths.pdf"
shutil.copyfile(src_pdf, test_pdf)

with pdfplumber.open(src_pdf) as pdf:
    char_widths = {}
    for p in pdf.pages:
        for c in p.chars:
            if c.get("size") == 8.0:
                char_widths[c["text"]] = c["width"]
if " " not in char_widths: char_widths[" "] = 2.2

def get_text_width(text):
    return sum(char_widths.get(ch, 4.5) for ch in text)

descs = [
    # Page 1
    "Biaya transaksi bank\nPembayaran Danatopup\n89508089622130569",
    "Pembayaran Danatopup\n89508089622130569",
    "Pembayaran QR\nke SOTO AYAM LAMONGAN CAK JO\n601483798729",
    "Penarikan tunai tanpa kartu\nDi ATM SRG AM PURI ANGREK 0\n089622130569",
    "Biaya transfer BI Fast",
    "Transfer BI Fast\nKe BCA\nBUDI SAPUTRA TANAGUN 1010570065",
    "Transfer ke BANK MANDIRI\nMEI DWI LESTARI 1370011851231",
    "Biaya transaksi bank\nPembayaran Danatopup\n89508087858621135",
    "Pembayaran Danatopup\n89508087858621135",
    "Transfer BI Fast\nDari BANK BNI\nFITRIANA PURWANINGSI 0314467254",
    # Page 2
    "Pembayaran QR\nke MAKO CAKE BAKERY SE 603\n601129029297",
    "Pembayaran QR\nke RESERVE SA SERANG 1 1324\n601120346341",
    "Biaya transaksi bank\nPembayaran Danatopup\n89508089622130569",
    "Pembayaran Danatopup\n89508089622130569",
    "Transfer dari BANK MANDIRI\nNANDA FEBRIANTI 1370013797036",
    "Biaya transaksi bank\nPembayaran Danatopup\n89508089622130569",
    "Pembayaran Danatopup\n89508089622130569",
    "Pembayaran QR\nke PECEL LELE Mas Dikky, pas\n601580938038",
    "Pembayaran QR\nke Syarkawi\n601581102500",
    "Biaya transaksi bank\nPembayaran Danatopup\n89508083175718201",
    "Pembayaran Danatopup\n89508083175718201",
    "Transfer BI Fast\nDari BCA\nPT BENDI NASHA NIAGA INDUSTRI 5411078192\n(CENAIDJA)",
    # Page 3
    "Pembayaran QR\nke TEMAN DENTAL AHMAD YAN 40\n601208674693",
    "Biaya transaksi bank\nPembayaran Danatopup\n89508089622130569",
    "Pembayaran Danatopup\n89508089622130569",
    "Penarikan tunai di ATM BANK\nMANDIRI SRG IM CIRUAS 01",
    "Penarikan tunai tanpa kartu\nDi ATM SRG MD CIRUAS 01\n089622130569",
    "Transfer BI Fast\nDari BANK BNI\nKARINA AMALIA DARMAW 1921323326",
    "Pembayaran QR ke\nwarung madura\n506115913713",
    "Penarikan tunai di ATM BANK\nMANDIRI SRG IM CIRUAS 01",
    "Transfer BI Fast\nDari BCA\nMULYATI 2452705525\n-",
    "Pembayaran QR\nke SPBU 3442109 KM 68 B 36\n601275499757",
    "Biaya transfer BI Fast\n-",
    "Transfer BI Fast\nKe BCA\nLUKMAN 1011284251",
    # Page 4
    "Transfer BI Fast\nDari BCA\nFERNANDUS NAINGGOLAN 8690976766\n-",
    "Penarikan tunai di ATM\nBANK MANDIRI SRG IM PAKUPATAN 01",
    "Biaya administrasi rekening"
]

page_row_counts = [10, 12, 12, 3]
cursor = 0

with PdfCraftClient() as client:
    doc_id = client.doc_open(test_pdf)
    
    for p_num, count in enumerate(page_row_counts, 1):
        base_y = 343.92 if p_num == 1 else 227.92
        
        for r_i in range(count):
            tx_idx = cursor
            cursor += 1
            desc_text = descs[tx_idx]
            lines = desc_text.split("\n")
            num_lines = len(lines)
            
            # calculate ideal width
            line_widths = [get_text_width(l) for l in lines]
            ideal_w = max(line_widths) + 5.0
            
            row_y = base_y + r_i * 46.00
            target_top = row_y - (num_lines - 1) * 5.0
            
            paras = client.get_paragraphs(doc_id, page=p_num)
            p_desc = [p for p in paras if abs(p["rect"][1] - row_y) < 22 and 120 <= p["rect"][0] <= 135]
            if p_desc:
                p_obj = p_desc[0]
                
                # Empty any lingering sub-lines
                extra_min_y = row_y - 20
                extra_max_y = row_y + 25
                extra_paras = [p for p in paras if extra_min_y <= p["rect"][1] <= extra_max_y and 120 <= p["rect"][0] <= 135 and p["paragraph"] != p_obj["paragraph"]]
                for ep in extra_paras:
                    client.edit_text(doc_id, page=p_num, paragraph=ep["paragraph"], text="")

                # Apply text edit WITH IDEAL WIDTH!
                client.call_tool("text_edit", {
                    "doc": doc_id,
                    "page": p_num,
                    "paragraph": p_obj["paragraph"],
                    "text": desc_text,
                    "width": ideal_w,
                    "line_spacing": 1.25
                })
                
                # Check resulting rect and adjust position (dx, dy)
                up_paras = client.get_paragraphs(doc_id, page=p_num)
                up = [p for p in up_paras if p["paragraph"] == p_obj["paragraph"]][0]
                
                dx = 124.00 - up["rect"][0]
                dy = up["rect"][1] - target_top
                
                kwargs_shift = {}
                if abs(dx) > 0.05: kwargs_shift["dx"] = dx
                if abs(dy) > 0.05: kwargs_shift["dy"] = dy
                
                if kwargs_shift:
                    client.edit_text(doc_id, page=p_num, paragraph=p_obj["paragraph"], **kwargs_shift)

    client.doc_save(doc_id, path=test_pdf, full=True)
    client.doc_close(doc_id)

print("\n=== VERIFYING RESULTING KETERANGAN POSITIONS ===")
cursor = 0
all_perfect = True
with pdfplumber.open(test_pdf) as pdf:
    for p_num, count in enumerate(page_row_counts, 1):
        words = pdf.pages[p_num - 1].extract_words()
        base_y = 343.92 if p_num == 1 else 227.92
        print(f"\n--- Page {p_num} ---")
        for r_i in range(count):
            tx_idx = cursor
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
            expected_num_l = len(descs[tx_idx].split("\n"))
            expected_top = row_y - (expected_num_l - 1) * 5.0
            diff = first_top - expected_top
            
            ok = (abs(diff) < 0.2 and num_l == expected_num_l and abs(first_x0 - 124.0) < 0.2)
            if not ok: all_perfect = False
            status = "PERFECT" if ok else "CHECK!"
            print(f"Tx {tx_idx+1:02d} [{status}] | row_y={row_y:.2f} | lines={num_l}/{expected_num_l} | x0={first_x0:.2f} | top={first_top:.2f} (diff: {diff:+.2f})")
            for top in sorted(lines.keys()):
                print(f"     top={top:5.1f}: {' '.join(lines[top])}")

print(f"\nALL PERFECT: {all_perfect}")
