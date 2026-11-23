import os
import sys
import shutil
import datetime
import openpyxl
import pdfplumber

sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient
from bank_mandiri_spec import (
    COL_NOMINAL_RIGHT_X,
    COL_SALDO_RIGHT_X,
    SUMMARY_RIGHT_X,
    COL_NO_X,
    COL_DATE_TIME_X0,
    VALUE_COL1_X0,
    COLOR_CREDIT_GREEN,
    COLOR_RUNNING_SALDO_BLUE,
    COLOR_DEBIT_BLACK,
    COLOR_SALDO_AWAL_GRAY
)

def format_idr(num):
    return f"{abs(num):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def parse_num(val):
    if val is None: return 0.0
    if isinstance(val, (int, float)): return float(val)
    s = str(val).replace("Rp", "").replace(" ", "").replace(".", "").replace(",", ".").strip()
    try: return float(s)
    except: return 0.0

# 35 Master Transactions Specification for September 2026
tx_specs = [
    {
        "no": 1, "page": 1, "row_idx": 0,
        "date": "04 Sep 2026", "time": "19:01:17 WIB",
        "desc": "Penarikan tunai di ATM\nBANK MANDIRI SRG IM CIRUAS 01",
        "nom": -1000000.0, "sal": 3527347.81
    },
    {
        "no": 2, "page": 1, "row_idx": 1,
        "date": "04 Sep 2026", "time": "19:18:12 WIB",
        "desc": "Transfer BI Fast\nDari BCA\nINDRA MIDIAN 2452372917\n-",
        "nom": 50000.0, "sal": 3577347.81
    },
    {
        "no": 3, "page": 1, "row_idx": 2,
        "date": "04 Sep 2026", "time": "23:59:59 WIB",
        "desc": "Biaya administrasi kartu debit",
        "nom": -3500.0, "sal": 3573847.81
    },
    {
        "no": 4, "page": 1, "row_idx": 3,
        "date": "05 Sep 2026", "time": "09:42:34 WIB",
        "desc": "Biaya transfer BI Fast",
        "nom": -2500.0, "sal": 3571347.81
    },
    {
        "no": 5, "page": 1, "row_idx": 4,
        "date": "05 Sep 2026", "time": "09:42:34 WIB",
        "desc": "Transfer BI Fast\nKe BCA\nKARINA AMALIA DARMAW 2452998221\n-",
        "nom": -200000.0, "sal": 3371347.81
    },
    {
        "no": 6, "page": 1, "row_idx": 5,
        "date": "05 Sep 2026", "time": "11:16:48 WIB",
        "desc": "Biaya transfer BI Fast",
        "nom": -2500.0, "sal": 3368847.81
    },
    {
        "no": 7, "page": 1, "row_idx": 6,
        "date": "05 Sep 2026", "time": "11:16:48 WIB",
        "desc": "Transfer BI Fast\nKe SEABANK INDONESIA\nMARWA ARSYIVA 901159417428\n-",
        "nom": -110000.0, "sal": 3258847.81
    },
    {
        "no": 8, "page": 1, "row_idx": 7,
        "date": "05 Sep 2026", "time": "11:59:54 WIB",
        "desc": "Pembayaran QR\nke SOTO LAMONGAN CAK JOYO QR\n602456232175",
        "nom": -21000.0, "sal": 3237847.81
    },
    {
        "no": 9, "page": 1, "row_idx": 8,
        "date": "05 Sep 2026", "time": "12:00:48 WIB",
        "desc": "Pembayaran QR\nke MADURA IKA\n602452197164",
        "nom": -36000.0, "sal": 3201847.81
    },
    {
        "no": 10, "page": 1, "row_idx": 9,
        "date": "05 Sep 2026", "time": "15:15:29 WIB",
        "desc": "Biaya transaksi bank\nPembayaran Danatopup\n89508089622130569",
        "nom": -1000.0, "sal": 3200847.81
    },
    # Page 2
    {
        "no": 11, "page": 2, "row_idx": 0,
        "date": "05 Sep 2026", "time": "15:15:29 WIB",
        "desc": "Pembayaran Danatopup\n89508089622130569",
        "nom": -658000.0, "sal": 2542847.81
    },
    {
        "no": 12, "page": 2, "row_idx": 1,
        "date": "06 Sep 2026", "time": "21:03:56 WIB",
        "desc": "Biaya transaksi bank\nPembayaran Danatopup\n89508083175718201",
        "nom": -1000.0, "sal": 2541847.81
    },
    {
        "no": 13, "page": 2, "row_idx": 2,
        "date": "06 Sep 2026", "time": "21:03:56 WIB",
        "desc": "Biaya transfer BI Fast",
        "nom": -2500.0, "sal": 2539347.81
    },
    {
        "no": 14, "page": 2, "row_idx": 3,
        "date": "08 Sep 2026", "time": "09:44:21 WIB",
        "desc": "Transfer BI Fast\nKe BCA\nMULYATI 2452705525\n-",
        "nom": -1500000.0, "sal": 1039347.81
    },
    {
        "no": 15, "page": 2, "row_idx": 4,
        "date": "08 Sep 2026", "time": "20:51:41 WIB",
        "desc": "Pembayaran QR\nke CHANYA DIO PD\n602486735923",
        "nom": -73000.0, "sal": 966347.81
    },
    {
        "no": 16, "page": 2, "row_idx": 5,
        "date": "08 Sep 2026", "time": "22:54:49 WIB",
        "desc": "Penarikan tunai tanpa kartu\nDi ATM SRG MD CIRUAS 01\n089622130569",
        "nom": -500000.0, "sal": 466347.81
    },
    {
        "no": 17, "page": 2, "row_idx": 6,
        "date": "09 Sep 2026", "time": "12:36:44 WIB",
        "desc": "Pembayaran QR\nke QR MTHDS 296 MALL SERANG\n602497965859",
        "nom": -211900.0, "sal": 254447.81
    },
    {
        "no": 18, "page": 2, "row_idx": 7,
        "date": "09 Sep 2026", "time": "12:41:26 WIB",
        "desc": "Biaya transfer BI Fast",
        "nom": -2500.0, "sal": 251947.81
    },
    {
        "no": 19, "page": 2, "row_idx": 8,
        "date": "09 Sep 2026", "time": "16:24:22 WIB",
        "desc": "Transfer BI Fast\nKe BCA\nMULYATI 2452705525\n-",
        "nom": -100000.0, "sal": 151947.81
    },
    {
        "no": 20, "page": 2, "row_idx": 9,
        "date": "10 Sep 2026", "time": "20:29:20 WIB",
        "desc": "Biaya transaksi bank\nPembayaran Danatopup\n89508089622130569",
        "nom": -1000.0, "sal": 150947.81
    },
    {
        "no": 21, "page": 2, "row_idx": 10,
        "date": "10 Sep 2026", "time": "20:29:20 WIB",
        "desc": "Pembayaran Danatopup\n89508089622130569",
        "nom": -50000.0, "sal": 100947.81
    },
    {
        "no": 22, "page": 2, "row_idx": 11,
        "date": "25 Sep 2026", "time": "04:00:00 WIB",
        "desc": "Transfer BI Fast\nDari BCA\nPT BENDI NASHA NIAGA INDUSTRI 5411078192\n(CENAIDJA)",
        "nom": 6778000.0, "sal": 6878947.81
    },
    # Page 3
    {
        "no": 23, "page": 3, "row_idx": 0,
        "date": "25 Sep 2026", "time": "10:49:08 WIB",
        "desc": "Biaya transfer BI Fast",
        "nom": -2500.0, "sal": 6876447.81
    },
    {
        "no": 24, "page": 3, "row_idx": 1,
        "date": "25 Sep 2026", "time": "10:49:08 WIB",
        "desc": "Transfer BI Fast\nKe BCA\nDEBORA DIAN FITRESIA 2453460819",
        "nom": -1300000.0, "sal": 5576447.81
    },
    {
        "no": 25, "page": 3, "row_idx": 2,
        "date": "26 Sep 2026", "time": "10:36:03 WIB",
        "desc": "Biaya transaksi bank\nPembayaran Danatopup\n89508089622130569",
        "nom": -1000.0, "sal": 5575447.81
    },
    {
        "no": 26, "page": 3, "row_idx": 3,
        "date": "26 Sep 2026", "time": "10:36:03 WIB",
        "desc": "Pembayaran Danatopup\n89508089622130569",
        "nom": -49000.0, "sal": 5526447.81
    },
    {
        "no": 27, "page": 3, "row_idx": 4,
        "date": "26 Sep 2026", "time": "14:39:50 WIB",
        "desc": "Pembayaran QR\nke ALGO SIDOARJO - QRIS\n604414054958",
        "nom": -500000.0, "sal": 5026447.81
    },
    {
        "no": 28, "page": 3, "row_idx": 5,
        "date": "27 Sep 2026", "time": "10:46:16 WIB",
        "desc": "Pembayaran QR\nke BPOP Galeri\n602542322638",
        "nom": -500000.0, "sal": 4526447.81
    },
    {
        "no": 29, "page": 3, "row_idx": 6,
        "date": "27 Sep 2026", "time": "16:41:59 WIB",
        "desc": "Top-up e-money\n6032982545716407",
        "nom": -380000.0, "sal": 4146447.81
    },
    {
        "no": 30, "page": 3, "row_idx": 7,
        "date": "28 Sep 2026", "time": "01:46:22 WIB",
        "desc": "Biaya transaksi bank\nPembayaran Danatopup\n89508089622130569",
        "nom": -1000.0, "sal": 4145447.81
    },
    {
        "no": 31, "page": 3, "row_idx": 8,
        "date": "28 Sep 2026", "time": "01:46:22 WIB",
        "desc": "Pembayaran Danatopup\n89508089622130569",
        "nom": -100000.0, "sal": 4045447.81
    },
    {
        "no": 32, "page": 3, "row_idx": 9,
        "date": "28 Sep 2026", "time": "15:12:40 WIB",
        "desc": "Biaya transaksi bank\nPembayaran Doku Merchant\n8902297404788969",
        "nom": -1500.0, "sal": 4043947.81
    },
    {
        "no": 33, "page": 3, "row_idx": 10,
        "date": "28 Sep 2026", "time": "15:12:40 WIB",
        "desc": "Pembayaran Doku Merchant\n8902297404788969",
        "nom": -294591.0, "sal": 3749356.81
    },
    {
        "no": 34, "page": 3, "row_idx": 11,
        "date": "28 Sep 2026", "time": "17:12:24 WIB",
        "desc": "Penarikan tunai di ATM\nBANK MANDIRI SRG IM CIRUAS 01",
        "nom": -1000000.0, "sal": 2749356.81
    },
    # Page 4
    {
        "no": 35, "page": 4, "row_idx": 0,
        "date": "30 Sep 2026", "time": "23:59:00 WIB",
        "desc": "Biaya administrasi rekening",
        "nom": -5000.0, "sal": 2744356.81
    }
]

print(f"Loaded {len(tx_specs)} transactions.")
assert len(tx_specs) == 35, "Expected 35 transactions!"

# Source base PDF: REK_GALANG_SEP_2026.pdf (clean authentic font base)
src_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_SEP_2026.pdf"
out_pdf = r"output\REK_GALANG_SEP_2026_PERFECT.pdf"

# Calculate character widths from src_pdf
char_widths = {}
with pdfplumber.open(src_pdf) as pdf:
    for p in pdf.pages:
        for c in p.chars:
            if c.get("size") == 8.0:
                char_widths[c["text"]] = c["width"]
if " " not in char_widths: char_widths[" "] = 2.2

def get_text_width(text):
    return sum(char_widths.get(ch, 4.5) for ch in text)

# Copy base to output
shutil.copyfile(src_pdf, out_pdf)

with PdfCraftClient() as client:
    doc_id = client.doc_open(out_pdf)
    print(f"Opened doc_id={doc_id} for perfection editing...")
    
    # 1. Update Header on all 4 pages if needed
    for p_num in range(1, 5):
        paras = client.get_paragraphs(doc_id, page=p_num)
        # Ensure Page number says X dari 4 / X of 4
        # In REK_GALANG_SEP_2026.pdf, page numbers are already 1 dari 4, etc.
        # Check Cabang & Name
        p_name = [p for p in paras if "GALANG" in p["text"] and p["rect"][1] < 140]
        if p_name:
            client.edit_text(doc_id, page=p_num, paragraph=p_name[0]["paragraph"], text="GALANG PUTRA\nKURNIAWAN\nKCP Serang Ciceri", line_spacing=1.375)
            up = [x for x in client.get_paragraphs(doc_id, page=p_num) if x["paragraph"] == p_name[0]["paragraph"]][0]
            dx = VALUE_COL1_X0 - up["rect"][0]
            if abs(dx) > 0.05:
                client.edit_text(doc_id, page=p_num, paragraph=up["paragraph"], dx=dx)

    # 2. Page 1 Account Number & Summary
    paras = client.get_paragraphs(doc_id, page=1)
    p_acc = [p for p in paras if "1630016287487" in p["text"]]
    if p_acc:
        # Align exactly at x0 = 160.00
        up = p_acc[0]
        dx = 160.00 - up["rect"][0]
        if abs(dx) > 0.05:
            client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)
            
    # Check Summary
    p_sawal = [p for p in paras if 160 <= p["rect"][1] <= 180 and p["rect"][0] > 480][0]
    client.edit_text(doc_id, page=1, paragraph=p_sawal["paragraph"], text="4.527.347,81", color=COLOR_SALDO_AWAL_GRAY)
    up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_sawal["paragraph"]][0]
    dx = SUMMARY_RIGHT_X - up["rect"][2]
    if abs(dx) > 0.01: client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

    p_dmasuk = [p for p in paras if 185 <= p["rect"][1] <= 205 and p["rect"][0] > 480][0]
    client.edit_text(doc_id, page=1, paragraph=p_dmasuk["paragraph"], text="+ 6.828.000,00", color=COLOR_CREDIT_GREEN)
    up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_dmasuk["paragraph"]][0]
    dx = SUMMARY_RIGHT_X - up["rect"][2]
    if abs(dx) > 0.01: client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

    p_dkeluar = [p for p in paras if 208 <= p["rect"][1] <= 228 and p["rect"][0] > 480][0]
    client.edit_text(doc_id, page=1, paragraph=p_dkeluar["paragraph"], text="- 8.610.991,00", color=COLOR_DEBIT_BLACK)
    up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_dkeluar["paragraph"]][0]
    dx = SUMMARY_RIGHT_X - up["rect"][2]
    if abs(dx) > 0.01: client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

    p_sakhir = [p for p in paras if 230 <= p["rect"][1] <= 255 and p["rect"][0] > 480][0]
    client.edit_text(doc_id, page=1, paragraph=p_sakhir["paragraph"], text="2.744.356,81", color=COLOR_RUNNING_SALDO_BLUE)
    up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_sakhir["paragraph"]][0]
    dx = SUMMARY_RIGHT_X - up["rect"][2]
    if abs(dx) > 0.01: client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

    # 3. Process all 35 transactions
    for tx in tx_specs:
        p_num = tx["page"]
        base_y = 343.92 if p_num == 1 else 227.92
        row_y = base_y + tx["row_idx"] * 46.00
        lines = tx["desc"].split("\n")
        num_lines = len(lines)
        
        # Calculate ideal width
        line_widths = [get_text_width(l) for l in lines]
        ideal_w = max(line_widths) + 5.0
        target_top = row_y - (num_lines - 1) * 5.0
        
        # A. Update No
        paras = client.get_paragraphs(doc_id, page=p_num)
        p_no = [p for p in paras if abs(p["rect"][1] - row_y) < 15 and 15 <= p["rect"][0] <= 35 and p["text"].strip().isdigit()]
        if p_no:
            client.edit_text(doc_id, page=p_num, paragraph=p_no[0]["paragraph"], text=str(tx["no"]))
            up_no = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_no[0]["paragraph"]][0]
            dx_no = COL_NO_X - up_no["rect"][0]
            if abs(dx_no) > 0.05:
                client.edit_text(doc_id, page=p_num, paragraph=up_no["paragraph"], dx=dx_no)
                
        # B. Update Date
        paras = client.get_paragraphs(doc_id, page=p_num)
        p_date = [p for p in paras if abs(p["rect"][1] - (row_y - 4.0)) < 10 and 45 <= p["rect"][0] <= 85 and "WIB" not in p["text"]]
        if p_date:
            client.edit_text(doc_id, page=p_num, paragraph=p_date[0]["paragraph"], text=tx["date"])
            up_d = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_date[0]["paragraph"]][0]
            dx_d = COL_DATE_TIME_X0 - up_d["rect"][0]
            if abs(dx_d) > 0.05:
                client.edit_text(doc_id, page=p_num, paragraph=up_d["paragraph"], dx=dx_d)
                
        # C. Update Time
        paras = client.get_paragraphs(doc_id, page=p_num)
        p_time = [p for p in paras if abs(p["rect"][1] - (row_y + 5.0)) < 10 and 45 <= p["rect"][0] <= 85 and "WIB" in p["text"]]
        if p_time:
            client.edit_text(doc_id, page=p_num, paragraph=p_time[0]["paragraph"], text=tx["time"])
            up_t = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_time[0]["paragraph"]][0]
            dx_t = COL_DATE_TIME_X0 - up_t["rect"][0]
            if abs(dx_t) > 0.05:
                client.edit_text(doc_id, page=p_num, paragraph=up_t["paragraph"], dx=dx_t)
                
        # D. Update Keterangan
        paras = client.get_paragraphs(doc_id, page=p_num)
        p_desc = [p for p in paras if abs(p["rect"][1] - row_y) < 22 and 120 <= p["rect"][0] <= 135]
        if p_desc:
            p_obj = p_desc[0]
            # Empty any lingering extra paragraphs in this row's description slot
            extra_paras = [p for p in paras if abs(p["rect"][1] - row_y) < 22 and 120 <= p["rect"][0] <= 135 and p["paragraph"] != p_obj["paragraph"]]
            for ep in extra_paras:
                client.edit_text(doc_id, page=p_num, paragraph=ep["paragraph"], text="")
                
            client.edit_text(doc_id, page=p_num, paragraph=p_obj["paragraph"], text=tx["desc"], width=ideal_w, line_spacing=1.25)
            up_k = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_obj["paragraph"]][0]
            dx_k = 124.00 - up_k["rect"][0]
            dy_k = target_top - up_k["rect"][1]
            if abs(dx_k) > 0.02 or abs(dy_k) > 0.02:
                client.edit_text(doc_id, page=p_num, paragraph=up_k["paragraph"], dx=dx_k, dy=dy_k)

        # E. Update Nominal
        paras = client.get_paragraphs(doc_id, page=p_num)
        p_nom = [p for p in paras if abs(p["rect"][1] - row_y) < 15 and 370 <= p["rect"][0] <= 450]
        if p_nom:
            is_credit = tx["nom"] > 0
            nom_str = ("+" if is_credit else "-") + format_idr(tx["nom"])
            col = COLOR_CREDIT_GREEN if is_credit else COLOR_DEBIT_BLACK
            client.edit_text(doc_id, page=p_num, paragraph=p_nom[0]["paragraph"], text=nom_str, color=col)
            up_n = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_nom[0]["paragraph"]][0]
            dx_n = COL_NOMINAL_RIGHT_X - up_n["rect"][2]
            if abs(dx_n) > 0.01:
                client.edit_text(doc_id, page=p_num, paragraph=up_n["paragraph"], dx=dx_n)
                
        # F. Update Saldo
        paras = client.get_paragraphs(doc_id, page=p_num)
        p_sal = [p for p in paras if abs(p["rect"][1] - row_y) < 15 and 490 <= p["rect"][0] <= 585]
        if p_sal:
            sal_str = format_idr(tx["sal"])
            client.edit_text(doc_id, page=p_num, paragraph=p_sal[0]["paragraph"], text=sal_str, color=COLOR_RUNNING_SALDO_BLUE)
            up_s = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_sal[0]["paragraph"]][0]
            dx_s = COL_SALDO_RIGHT_X - up_s["rect"][2]
            if abs(dx_s) > 0.01:
                client.edit_text(doc_id, page=p_num, paragraph=up_s["paragraph"], dx=dx_s)

    # Save output
    client.doc_save(doc_id, path=out_pdf, full=True)
    client.doc_close(doc_id)
    print(f"\n[SUCCESS] Generated perfected PDF: {out_pdf}")

# Audit the generated output
print("\n--- RUNNING AUDIT ON OUTPUT ---")
with pdfplumber.open(out_pdf) as pdf:
    for page_idx, page in enumerate(pdf.pages, 1):
        fonts = set(c.get('fontname') for c in page.chars)
        foreign = [c for c in page.chars if 'TTInterphases' not in c.get('fontname', '')]
        print(f"Page {page_idx}: fonts={fonts}, foreign_chars_count={len(foreign)}")
        
        # Check Account number on Page 1
        if page_idx == 1:
            for w in page.extract_words():
                if "163001" in w['text']:
                    print(f"  Account number: '{w['text']}' at x0={w['x0']:.2f}, top={w['top']:.2f}")
