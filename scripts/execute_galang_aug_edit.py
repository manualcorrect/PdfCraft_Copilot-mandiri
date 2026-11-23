"""
Execute Galang Aug 2026 In-Place e-Statement Editing
Performs authentic SOP 7-Tahap in-place editing on 2.pdf to generate standardized Galang Putra Kurniawan statement.
"""

import os
import sys
import shutil
import re
from typing import Dict, Any, List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from pdfcraft_client import PdfCraftClient
from bank_mandiri_spec import (
    COL_NOMINAL_RIGHT_X,
    COL_SALDO_RIGHT_X,
    SUMMARY_RIGHT_X,
    COL_NO_X,
    COL_DATE_TIME_X0,
    VALUE_COL1_X0,
    VALUE_COL2_X0,
    COLOR_CREDIT_GREEN,
    COLOR_RUNNING_SALDO_BLUE,
    COLOR_DEBIT_BLACK,
    COLOR_SALDO_AWAL_GRAY
)
from parse_excel_template import parse_xara_excel_template
import pdfplumber

def execute_edit(src_pdf: str, excel_path: str, out_pdf: str):
    print("==================================================")
    print("  EXECUTING GALANG AUG 2026 IN-PLACE PDF EDITING  ")
    print(f"  Source PDF : {src_pdf}")
    print(f"  Excel Spec : {excel_path}")
    print(f"  Output PDF : {out_pdf}")
    print("==================================================")

    # 1. Parse Excel data
    data = parse_xara_excel_template(excel_path)
    header = data.get("header", {})
    summary = data.get("summary", {})
    all_txs = data.get("transactions", [])

    # Filter out empty or zero nominals
    active_txs = []
    for tx in all_txs:
        nom_raw = str(tx.get("nominal", "")).replace(".", "").replace(",", ".").replace("+", "").strip()
        try:
            val = float(nom_raw)
            if abs(val) > 0.001:
                active_txs.append(tx)
        except:
            if tx.get("nominal"):
                active_txs.append(tx)

    print(f"[1] Total active transactions to map: {len(active_txs)} (Expected: 37)")
    assert len(active_txs) == 37, f"Expected 37 transactions, got {len(active_txs)}"

    # Copy src_pdf to out_pdf first
    os.makedirs(os.path.dirname(out_pdf), exist_ok=True)
    shutil.copyfile(src_pdf, out_pdf)

    with PdfCraftClient() as client:
        doc_id = client.doc_open(out_pdf)
        print(f"[2] Opened document with doc_id={doc_id}")

        customer_name = header.get("nama", "GALANG PUTRA KURNIAWAN").upper()
        cabang = header.get("cabang", "KCP Serang Ciceri")
        periode = header.get("periode", "01 Aug 2026 - 31 Aug 2026")
        dicetak_pada = header.get("dicetak_pada", "09 Sep 2026")
        no_rek = header.get("nomor_rekening", "1630016287487")

        total_pages = 4

        # ----------------------------------------------------------------------
        # TAHAP 1-5: HEADER ACROSS ALL 4 PAGES
        # ----------------------------------------------------------------------
        for p_num in range(1, total_pages + 1):
            paras = client.get_paragraphs(doc_id, page=p_num)
            
            # Customer Name
            for p in paras:
                if "ROY DARWIN REZERIUS" in p["text"] and p["rect"][1] < 150:
                    client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text=customer_name)
                    # align left to 123.00
                    up_p = [x for x in client.get_paragraphs(doc_id, page=p_num) if x["paragraph"] == p["paragraph"]][0]
                    dx = VALUE_COL1_X0 - up_p["rect"][0]
                    if abs(dx) > 0.05:
                        client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], dx=dx)
                    break

            # Cabang
            paras = client.get_paragraphs(doc_id, page=p_num)
            for p in paras:
                if ("Taman Aries" in p["text"] or "KCP" in p["text"]) and 115 <= p["rect"][1] <= 135 and p["rect"][0] < 200:
                    client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text=cabang)
                    up_p = [x for x in client.get_paragraphs(doc_id, page=p_num) if x["paragraph"] == p["paragraph"]][0]
                    dx = VALUE_COL1_X0 - up_p["rect"][0]
                    if abs(dx) > 0.05:
                        client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], dx=dx)
                    break

            # Periode
            paras = client.get_paragraphs(doc_id, page=p_num)
            for p in paras:
                if ("01Jan" in p["text"] or "01 Jan" in p["text"]) and 90 <= p["rect"][1] <= 115 and 330 <= p["rect"][0] <= 370:
                    client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text=periode)
                    up_p = [x for x in client.get_paragraphs(doc_id, page=p_num) if x["paragraph"] == p["paragraph"]][0]
                    dx = VALUE_COL2_X0 - up_p["rect"][0]
                    if abs(dx) > 0.05:
                        client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], dx=dx)
                    break

            # Dicetak Pada
            paras = client.get_paragraphs(doc_id, page=p_num)
            for p in paras:
                if ("09Sep" in p["text"] or "09 Sep" in p["text"]) and 115 <= p["rect"][1] <= 135 and 330 <= p["rect"][0] <= 370:
                    client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text=dicetak_pada)
                    up_p = [x for x in client.get_paragraphs(doc_id, page=p_num) if x["paragraph"] == p["paragraph"]][0]
                    dx = VALUE_COL2_X0 - up_p["rect"][0]
                    if abs(dx) > 0.05:
                        client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], dx=dx)
                    break

            # Page Numbers (1 dari 4, 1 of 4, etc.)
            paras = client.get_paragraphs(doc_id, page=p_num)
            # 1. Clear orphaned digit
            for p in paras:
                if p["text"].strip().isdigit() and 545 <= p["rect"][0] <= 575 and 90 <= p["rect"][1] <= 110:
                    client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text="")

            paras = client.get_paragraphs(doc_id, page=p_num)
            for p in paras:
                if "dari" in p["text"] and 520 <= p["rect"][0] <= 570 and 90 <= p["rect"][1] <= 115:
                    client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text=f"{p_num} dari 4", width=50.0)
                elif "of" in p["text"] and 530 <= p["rect"][0] <= 570 and 105 <= p["rect"][1] <= 125:
                    client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text=f"{p_num} of 4", width=50.0)

            print(f"  [Tahap 1-5] Page {p_num} headers updated to Galang Putra Kurniawan & '{p_num} dari 4'")

        # ----------------------------------------------------------------------
        # PAGE 1 SPECIFIC: ACCOUNT NUMBER & FINANCIAL SUMMARY
        # ----------------------------------------------------------------------
        paras = client.get_paragraphs(doc_id, page=1)
        for p in paras:
            if "1650003584860" in p["text"]:
                client.edit_text(doc_id, page=1, paragraph=p["paragraph"], text=f"{no_rek} ")
                break

        # Financial Summary values
        paras = client.get_paragraphs(doc_id, page=1)
        # Saldo Awal (approx Y=168)
        p_sawal = [p for p in paras if 160 <= p["rect"][1] <= 180 and p["rect"][0] > 480]
        if p_sawal:
            val = summary.get("saldo_awal", "4.530.335,81")
            client.edit_text(doc_id, page=1, paragraph=p_sawal[0]["paragraph"], text=val, color=COLOR_SALDO_AWAL_GRAY)
            up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_sawal[0]["paragraph"]][0]
            dx = SUMMARY_RIGHT_X - up["rect"][2]
            if abs(dx) > 0.01:
                client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

        paras = client.get_paragraphs(doc_id, page=1)
        # Dana Masuk (approx Y=191)
        p_dmasuk = [p for p in paras if 185 <= p["rect"][1] <= 205 and p["rect"][0] > 480]
        if p_dmasuk:
            val = f"+ {summary.get('dana_masuk', '7.649.000,00')}"
            client.edit_text(doc_id, page=1, paragraph=p_dmasuk[0]["paragraph"], text=val, color=COLOR_CREDIT_GREEN)
            up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_dmasuk[0]["paragraph"]][0]
            dx = SUMMARY_RIGHT_X - up["rect"][2]
            if abs(dx) > 0.01:
                client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

        paras = client.get_paragraphs(doc_id, page=1)
        # Dana Keluar (approx Y=214)
        p_dkeluar = [p for p in paras if 208 <= p["rect"][1] <= 228 and p["rect"][0] > 480]
        if p_dkeluar:
            val = f"- {summary.get('dana_keluar', '7.651.988,00')}"
            client.edit_text(doc_id, page=1, paragraph=p_dkeluar[0]["paragraph"], text=val, color=COLOR_DEBIT_BLACK)
            up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_dkeluar[0]["paragraph"]][0]
            dx = SUMMARY_RIGHT_X - up["rect"][2]
            if abs(dx) > 0.01:
                client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

        paras = client.get_paragraphs(doc_id, page=1)
        # Saldo Akhir (approx Y=238)
        p_sakhir = [p for p in paras if 230 <= p["rect"][1] <= 255 and p["rect"][0] > 480]
        if p_sakhir:
            val = summary.get("saldo_akhir", "4.527.347,81")
            client.edit_text(doc_id, page=1, paragraph=p_sakhir[0]["paragraph"], text=val, color=COLOR_RUNNING_SALDO_BLUE)
            up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_sakhir[0]["paragraph"]][0]
            dx = SUMMARY_RIGHT_X - up["rect"][2]
            if abs(dx) > 0.01:
                client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

        print("  [Tahap 7] Page 1 Financial Summary updated & right-aligned to 567.00 pt")

        # ----------------------------------------------------------------------
        # TAHAP 6 & 7: TRANSACTIONS ROW BY ROW (1 s.d. 37)
        # ----------------------------------------------------------------------
        tx_cursor = 0
        page_capacities = [10, 12, 12, 3]

        for p_idx, num_rows in enumerate(page_capacities):
            p_num = p_idx + 1
            min_top = 320 if p_num == 1 else 200
            print(f"[3] Processing Page {p_num} ({num_rows} transactions)...")

            for r_idx in range(num_rows):
                tx_no = tx_cursor + 1
                tx_data = active_txs[tx_cursor]
                tx_cursor += 1

                paras = client.get_paragraphs(doc_id, page=p_num)
                # Find row index paragraphs on this page
                table_paras = [p for p in paras if min_top <= p["rect"][1] <= 800]
                no_paras = sorted([p for p in table_paras if 15 <= p["rect"][0] <= 35 and p["text"].strip().isdigit()], key=lambda x: x["rect"][1])
                
                assert len(no_paras) >= num_rows, f"Page {p_num} expected {num_rows} no_paras, got {len(no_paras)}"
                target_no_p = no_paras[r_idx]
                row_y = target_no_p["rect"][1]

                # 1. Update No to sequential (1..37)
                client.edit_text(doc_id, page=p_num, paragraph=target_no_p["paragraph"], text=str(tx_no))
                up_no = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == target_no_p["paragraph"]][0]
                dx_no = COL_NO_X - up_no["rect"][0]
                if abs(dx_no) > 0.05:
                    client.edit_text(doc_id, page=p_num, paragraph=up_no["paragraph"], dx=dx_no)

                # 2. Update Date Month Jan -> Aug
                paras = client.get_paragraphs(doc_id, page=p_num)
                date_paras = [p for p in paras if abs(p["rect"][1] - row_y) < 15 and 45 <= p["rect"][0] <= 80]
                if date_paras:
                    dp = date_paras[0]
                    # If special override on Row 22 (orig 25 Aug 2026)
                    if tx_no == 22:
                        new_date = "25 Aug 2026"
                    else:
                        new_date = dp["text"].replace("Jan", "Aug").strip()
                    client.edit_text(doc_id, page=p_num, paragraph=dp["paragraph"], text=new_date)
                    up_d = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == dp["paragraph"]][0]
                    dx_d = COL_DATE_TIME_X0 - up_d["rect"][0]
                    if abs(dx_d) > 0.05:
                        client.edit_text(doc_id, page=p_num, paragraph=up_d["paragraph"], dx=dx_d)

                # 3. Update Time if Row 22
                if tx_no == 22:
                    paras = client.get_paragraphs(doc_id, page=p_num)
                    time_paras = [p for p in paras if abs(p["rect"][1] - (row_y + 11)) < 8 and 45 <= p["rect"][0] <= 80]
                    if time_paras:
                        tp = time_paras[0]
                        client.edit_text(doc_id, page=p_num, paragraph=tp["paragraph"], text="04:00:00 WIB")
                        up_t = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == tp["paragraph"]][0]
                        dx_t = COL_DATE_TIME_X0 - up_t["rect"][0]
                        if abs(dx_t) > 0.05:
                            client.edit_text(doc_id, page=p_num, paragraph=up_t["paragraph"], dx=dx_t)

                # 4. Update Nominal
                paras = client.get_paragraphs(doc_id, page=p_num)
                nom_paras = [p for p in paras if abs(p["rect"][1] - row_y) < 15 and 370 <= p["rect"][0] <= 450]
                if nom_paras:
                    np = nom_paras[0]
                    nom_val = str(tx_data["nominal"]).strip()
                    is_credit = tx_data.get("tipe") == "CR" or nom_val.startswith("+")
                    if is_credit and not nom_val.startswith("+"):
                        nom_val = f"+{nom_val}"
                    elif not is_credit and not nom_val.startswith("-"):
                        nom_val = f"-{nom_val}"
                    color = COLOR_CREDIT_GREEN if is_credit else COLOR_DEBIT_BLACK

                    client.edit_text(doc_id, page=p_num, paragraph=np["paragraph"], text=nom_val, color=color)
                    up_n = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == np["paragraph"]][0]
                    dx_n = COL_NOMINAL_RIGHT_X - up_n["rect"][2]
                    if abs(dx_n) > 0.01:
                        client.edit_text(doc_id, page=p_num, paragraph=up_n["paragraph"], dx=dx_n)

                # 5. Update Saldo
                paras = client.get_paragraphs(doc_id, page=p_num)
                sal_paras = [p for p in paras if abs(p["rect"][1] - row_y) < 15 and 490 <= p["rect"][0] <= 585]
                if sal_paras:
                    sp = sal_paras[0]
                    sal_val = str(tx_data["saldo"]).strip()
                    client.edit_text(doc_id, page=p_num, paragraph=sp["paragraph"], text=sal_val, color=COLOR_RUNNING_SALDO_BLUE)
                    up_s = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == sp["paragraph"]][0]
                    dx_s = COL_SALDO_RIGHT_X - up_s["rect"][2]
                    if abs(dx_s) > 0.01:
                        client.edit_text(doc_id, page=p_num, paragraph=up_s["paragraph"], dx=dx_s)

        # Save finalized PDF
        client.doc_save(doc_id, path=out_pdf, full=True)
        client.doc_close(doc_id)

    print(f"\n[SUCCESS] PDF e-Statement standardized and saved to: {out_pdf}")

    # Run quick telemetry audit
    print("\n--- RUNNING TELEMETRY VERIFICATION AUDIT ---")
    with pdfplumber.open(out_pdf) as pdf:
        for p_idx, page in enumerate(pdf.pages):
            p_n = p_idx + 1
            words = page.extract_words()
            p_header = [w['text'] for w in words if w['top'] < 130 and any(k in w['text'] for k in ['GALANG', 'Ciceri', 'Aug', 'dari', 'of'])]
            print(f"Page {p_n} Header tokens: {p_header[:10]}")
            
            # Check row count
            min_top = 320 if p_n == 1 else 200
            r_nos = [w['text'] for w in words if min_top <= w['top'] <= 800 and 15 <= w['x0'] <= 35 and w['text'].isdigit()]
            print(f"Page {p_n} Transactions ({len(r_nos)} rows): {r_nos}")

if __name__ == "__main__":
    src_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf"
    excel_path = r"templates\Template_Mutasi_Aug_Reconciled.xlsx"
    out_pdf = r"output\REK_GALANG_AUG_2026_STANDARDIZED.pdf"

    execute_edit(src_pdf, excel_path, out_pdf)
