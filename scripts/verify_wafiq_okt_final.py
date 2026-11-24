"""
Verification & Audit Suite for Bank Mandiri e-Statement:
Client: WAFIQ DWI ANANDA
Period: October 2026 (01 Oct 2026 - 31 Oct 2026)
"""

import os
import sys
import re
import pdfplumber
import openpyxl

PDF_TARGET = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\okt\REK_WAFIQ_OKT_OUTPUT_PERFECT.pdf"
EXCEL_TARGET = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\okt\Template_Mutasi_OKT.xlsx"

def run_audit():
    print("=================================================================")
    print("AUDITING WAFIQ DWI ANANDA - OCTOBER 2026 STATEMENT & EXCEL")
    print("=================================================================")

    passes = []
    failures = []

    def check(name, condition, details=""):
        if condition:
            passes.append(f"[PASS] {name} {details}")
            print(f"  [PASS] {name} {details}")
        else:
            failures.append(f"[FAIL] {name} {details}")
            print(f"  [FAIL] {name} {details}")

    # 1. FILE EXISTENCE
    print("\n--- 1. FILE EXISTENCE ---")
    check("PDF Target exists", os.path.exists(PDF_TARGET), PDF_TARGET)
    check("Excel Target exists", os.path.exists(EXCEL_TARGET), EXCEL_TARGET)

    # 2. PDF METADATA & HEADER AUDIT
    print("\n--- 2. PDF HEADER & METADATA AUDIT ---")
    with pdfplumber.open(PDF_TARGET) as pdf:
        check("Total pages is 5", len(pdf.pages) == 5, f"Found {len(pdf.pages)}")

        for p_idx in range(4):
            page = pdf.pages[p_idx]
            text = page.extract_text()
            p_num = p_idx + 1

            check(f"Page {p_num} Name is WAFIQ DWI ANANDA", "WAFIQ DWI ANANDA" in text)
            check(f"Page {p_num} Branch is KCP Serang Ciceri", "KCP Serang Ciceri" in text)
            check(f"Page {p_num} Period is 01 Oct 2026 - 31 Oct 2026", "01 Oct 2026 - 31 Oct 2026" in text)
            check(f"Page {p_num} Issued on 12 Nov 2026", "12 Nov 2026" in text)
            check(f"Page {p_num} Page number '{p_num} dari 5'", f"{p_num} dari 5" in text)
            check(f"Page {p_num} Page number '{p_num} of 5'", f"{p_num} of 5" in text)

            if p_num == 1:
                check("Page 1 Account is 1630016689138", "1630016689138" in text)

        # Page 5 Disclaimer
        p5_text = pdf.pages[4].extract_text()
        check("Page 5 contains Disclaimer", "Disclaimer" in p5_text and "batas akhir transaksi anda" in p5_text)

    # 3. SUMMARY BOX ON PAGE 1
    print("\n--- 3. FINANCIAL SUMMARY BOX AUDIT (PAGE 1) ---")
    with pdfplumber.open(PDF_TARGET) as pdf:
        p1 = pdf.pages[0]
        words = p1.extract_words()
        sb_words = [w for w in words if 290 <= w['x0'] <= 580 and 150 <= w['top'] <= 260]
        sb_text = " ".join([w['text'] for w in sorted(sb_words, key=lambda x: (x['top'], x['x0']))])

        check("Summary Saldo Awal is 5.730.669,81", "5.730.669,81" in sb_text)
        check("Summary Dana Masuk is + 11.408.000,00", "+ 11.408.000,00" in sb_text)
        check("Summary Dana Keluar is - 5.669.669,00", "- 5.669.669,00" in sb_text)
        check("Summary Saldo Akhir is 11.469.000,81", "11.469.000,81" in sb_text)

        # Check alignment right edge
        v_awal = [w for w in sb_words if w['text'] == '5.730.669,81']
        v_masuk = [w for w in sb_words if '11.408.000,00' in w['text']]
        v_keluar = [w for w in sb_words if '5.669.669,00' in w['text']]
        v_akhir = [w for w in sb_words if w['text'] == '11.469.000,81']

        if v_awal: check("Saldo Awal right edge at 567.00 pt", abs(v_awal[0]['x1'] - 567.00) < 0.5, f"x1={v_awal[0]['x1']:.2f}")
        if v_masuk: check("Dana Masuk right edge at 567.00 pt", abs(v_masuk[0]['x1'] - 567.00) < 0.5, f"x1={v_masuk[0]['x1']:.2f}")
        if v_keluar: check("Dana Keluar right edge at 567.00 pt", abs(v_keluar[0]['x1'] - 567.00) < 0.5, f"x1={v_keluar[0]['x1']:.2f}")
        if v_akhir: check("Saldo Akhir right edge at 567.00 pt", abs(v_akhir[0]['x1'] - 567.00) < 0.5, f"x1={v_akhir[0]['x1']:.2f}")

    # 4. TABLE ROWS AUDIT
    print("\n--- 4. TABLE ROWS & TRANSACTION AUDIT ---")
    with pdfplumber.open(PDF_TARGET) as pdf:
        all_tx = []
        for p_idx in range(4):
            page = pdf.pages[p_idx]
            words = page.extract_words()
            min_top = 310 if p_idx == 0 else 180
            t_words = [w for w in words if min_top <= w['top'] <= 780]
            wibs = sorted([w for w in t_words if w['text'] == 'WIB'], key=lambda x: x['top'])
            for w in wibs:
                noms = [x for x in t_words if abs(x['top'] - w['top']) < 15 and 360 <= x['x0'] <= 440]
                saldos = [x for x in t_words if abs(x['top'] - w['top']) < 15 and 490 <= x['x0'] <= 580]
                nos = [x for x in t_words if abs(x['top'] - w['top']) < 15 and 15 <= x['x0'] <= 40]
                descs = [x for x in t_words if abs(x['top'] - w['top']) < 22 and 115 <= x['x0'] <= 365]

                nom_str = " ".join([x['text'] for x in sorted(noms, key=lambda x: x['x0'])])
                sal_str = " ".join([x['text'] for x in sorted(saldos, key=lambda x: x['x0'])])
                no_str = " ".join([x['text'] for x in sorted(nos, key=lambda x: x['x0'])])

                lines = {}
                for cw in sorted(descs, key=lambda x: (x['top'], x['x0'])):
                    lines.setdefault(round(cw['top'], 1), []).append(cw['text'])
                desc_str = "\n".join([" ".join(lines[top]) for top in sorted(lines.keys())])

                all_tx.append({
                    'page': p_idx + 1,
                    'top': w['top'],
                    'no': no_str,
                    'nom': nom_str,
                    'saldo': sal_str,
                    'desc': desc_str,
                    'saldo_x1': saldos[-1]['x1'] if saldos else 0,
                    'nom_x1': noms[-1]['x1'] if noms else 0
                })

        check("Total extracted table rows is 46", len(all_tx) == 46, f"Found {len(all_tx)}")

        # Audit Tx 34 (Salary)
        tx34 = all_tx[33]
        check("Tx 34 is on Page 3", tx34['page'] == 3)
        check("Tx 34 No is 34", tx34['no'] == '34', f"no={tx34['no']}")
        check("Tx 34 Nominal is +5.200.000,00", "+5.200.000,00" in tx34['nom'] or "+ 5.200.000,00" in tx34['nom'], f"nom={tx34['nom']}")
        check("Tx 34 Saldo is 11.937.000,81", "11.937.000,81" in tx34['saldo'], f"saldo={tx34['saldo']}")
        check("Tx 34 Desc has BENDI NASHA NIAGA INDUSTRI 5411078192", "PT BENDI NASHA NIAGA INDUSTRI 5411078192" in tx34['desc'])
        check("Tx 34 Desc has (CENAIDJA)", "(CENAIDJA)" in tx34['desc'])

        # Audit Tx 46 (Closing Fee)
        tx46 = all_tx[45]
        check("Tx 46 is on Page 4", tx46['page'] == 4)
        check("Tx 46 No is 46", tx46['no'] == '46', f"no={tx46['no']}")
        check("Tx 46 Nominal is -5.000,00", "-5.000,00" in tx46['nom'] or "- 5.000,00" in tx46['nom'], f"nom={tx46['nom']}")
        check("Tx 46 Saldo is 11.469.000,81", "11.469.000,81" in tx46['saldo'], f"saldo={tx46['saldo']}")
        check("Tx 46 Desc is Biaya administrasi rekening", "Biaya administrasi rekening" in tx46['desc'])

        # Check right-edge alignment across all rows
        saldo_edges = [tx['saldo_x1'] for tx in all_tx if tx['saldo_x1'] > 0]
        max_sal_err = max(abs(x - 571.00) for x in saldo_edges) if saldo_edges else 99
        check("All running saldos right-aligned at 571.00 pt (+-0.5 pt)", max_sal_err < 0.5, f"max error={max_sal_err:.2f} pt")

    # 5. EXCEL SYNCHRONIZATION AUDIT
    print("\n--- 5. EXCEL TEMPLATE SYNCHRONIZATION AUDIT ---")
    wb = openpyxl.load_workbook(EXCEL_TARGET, data_only=True)
    ws_hr = wb['Header & Ringkasan']
    check("Excel HR Nama is WAFIQ DWI ANANDA", ws_hr['B10'].value == "WAFIQ DWI ANANDA")
    check("Excel HR Cabang is KCP Serang Ciceri", ws_hr['B11'].value == "KCP Serang Ciceri")
    check("Excel HR Periode is 01 Oct 2026 - 31 Oct 2026", ws_hr['B12'].value == "01 Oct 2026 - 31 Oct 2026")
    check("Excel HR Rekening is 1630016689138", str(ws_hr['B14'].value) == "1630016689138")
    check("Excel HR Saldo Awal is 5730669", ws_hr['B22'].value == 5730669)
    check("Excel HR Dana Masuk is 11408000", ws_hr['B23'].value == 11408000)
    check("Excel HR Dana Keluar is -5669669", ws_hr['B24'].value == -5669669)
    check("Excel HR Saldo Akhir is 11469000", ws_hr['B25'].value == 11469000)
    check("Excel HR Status is LULUS AUDIT (KLOP 100%)", ws_hr['B26'].value == "LULUS AUDIT (KLOP 100%)")

    ws = wb['Tabel_Mutasi']
    active_rows = [r for r in range(6, ws.max_row + 1) if ws.cell(r, 5).value is not None and abs(float(ws.cell(r, 5).value)) > 0]
    check("Excel active rows count is 46", len(active_rows) == 46, f"Found {len(active_rows)}")

    # Check Excel Tx 34 & 46
    r34 = active_rows[33]
    check("Excel Tx 34 Nominal is 5200000", ws.cell(r34, 5).value == 5200000)
    check("Excel Tx 34 Saldo is 11937000", ws.cell(r34, 7).value == 11937000)
    check("Excel Tx 34 Type is CR", ws.cell(r34, 6).value == "CR")
    check("Excel Tx 34 Desc is BENDI Salary", "BENDI" in str(ws.cell(r34, 4).value))

    r46 = active_rows[45]
    check("Excel Tx 46 Nominal is -5000", ws.cell(r46, 5).value == -5000)
    check("Excel Tx 46 Saldo is 11469000", ws.cell(r46, 7).value == 11469000)
    check("Excel Tx 46 Type is DB", ws.cell(r46, 6).value == "DB")
    check("Excel Tx 46 Desc is Biaya administrasi rekening", ws.cell(r46, 4).value == "Biaya administrasi rekening")

    # 6. FONT PURITY AUDIT
    print("\n--- 6. FONT PURITY AUDIT ---")
    with open(PDF_TARGET, 'rb') as f:
        pdf_raw = f.read()
    foreign_fonts = [b'Helvetica', b'Arial', b'Times', b'Courier', b'Calibri']
    found_foreign = [f.decode() for f in foreign_fonts if f in pdf_raw]
    check("No foreign fallback fonts in PDF", len(found_foreign) == 0, f"Found: {found_foreign}")

    print("\n=================================================================")
    print(f"AUDIT SUMMARY: {len(passes)} PASSED, {len(failures)} FAILED")
    print("=================================================================")

    if failures:
        print("\nFAILURES TO INVESTIGATE:")
        for fail in failures:
            print(f"  {fail}")
        return False
    else:
        print("\nALL AUDIT CHECKS PASSED WITH 100% PERFECTION!")
        return True

if __name__ == "__main__":
    success = run_audit()
    sys.exit(0 if success else 1)
