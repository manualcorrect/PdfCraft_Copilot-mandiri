import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Reference Anchors:
# Rata Kiri (x0):
#   16.00: e-Statement, Nama/Name, Cabang/Branch, Tabungan NOW IDR, Nomor Rekening/Account Number, Mata Uang/Currency
#   20.00: No
#   52.00: Tanggal, Date, DD Mon YYYY, Jam WIB
#   111.00: colons for Nama, Cabang
#   123.00: Customer Name, Branch values
#   124.00: Keterangan, Remarks, Description text
#   148.00: colons for Nomor Rekening, Mata Uang
#   160.00: Account Number value, Currency (IDR)
#   233.00: Periode/Period, Dicetak pada/Issued on
#   298.00: Saldo Awal, Dana Masuk, Dana Keluar, Saldo Akhir labels
#   326.00: colons for Periode, Dicetak pada
#   340.00: Periode value, Dicetak pada value
#   446.12: colons for Summary Box
#
# Rata Kanan (x1):
#   432.00: Nominal (IDR), Amount (IDR), ALL transaction nominals
#   567.00: ALL 4 summary values (Saldo Awal, Dana Masuk, Dana Keluar, Saldo Akhir)
#   571.00: Saldo (IDR), Balance (IDR), ALL running saldos
#   579.00: Bank address line, Mandiri Call 14000
#   563.96: Page numbers (Indonesian & English)

pdf_path = "output/REK_GALANG_JUL_2026_STANDARDIZED.pdf"

with pdfplumber.open(pdf_path) as pdf:
    for page_idx, page in enumerate(pdf.pages):
        p_num = page_idx + 1
        print(f"\n==================== PAGE {p_num} AUDIT ====================")
        words = page.extract_words()
        
        # Check Left Alignments on Page 1
        if p_num == 1:
            print("--- Left-aligned elements (x0 check) ---")
            checks_x0 = [
                ("Nama/Name", 16.00),
                ("Cabang/Branch", 16.00),
                ("GALANG", 123.00),
                ("KCP", 123.00),
                ("Nomor", 16.00),
                ("16300", 160.00),
                ("Periode/Period", 233.00),
                ("01 Jul", 340.00),
                ("Dicetak", 233.00),
                ("09 Aug", 340.00),
                ("Saldo Awal", 298.00),
                ("Dana Masuk", 298.00),
                ("Dana Keluar", 298.00),
                ("Saldo Akhir", 298.00),
            ]
            for target_text, target_x in checks_x0:
                matches = [w for w in words if target_text in w['text'] or w['text'] in target_text]
                if matches:
                    m = matches[0]
                    diff = m['x0'] - target_x
                    status = "OK" if abs(diff) < 0.5 else f"DIFF ({diff:+.2f} pt)"
                    print(f"  {target_text:15s} | actual x0={m['x0']:6.2f} | target={target_x:6.2f} | status={status}")
                else:
                    print(f"  {target_text:15s} | NOT FOUND")

        # Check Right Alignments on Summary Box (Page 1)
        if p_num == 1:
            print("\n--- Summary Box Right Alignments (x1 = 567.00 check) ---")
            summary_words = [w for w in words if 160 <= w['top'] <= 255 and w['x0'] > 480 and (',' in w['text'] or '.' in w['text'])]
            for w in summary_words:
                diff = w['x1'] - 567.00
                status = "OK" if abs(diff) < 0.5 else f"DIFF ({diff:+.2f} pt)"
                print(f"  Summary Val: {w['text']:18s} | actual x1={w['x1']:6.2f} | target=567.00 | status={status}")

        # Check Table Elements
        print(f"\n--- Table Transactions Check (Page {p_num}) ---")
        min_y = 320 if p_num == 1 else 200
        table_words = [w for w in words if min_y <= w['top'] <= 800]
        
        # Check Nominals (target x1 = 432.00)
        nominals = [w for w in table_words if (w['text'].startswith('+') or w['text'].startswith('-') or w['text'] == '300.000,00') and 350 <= w['x0'] <= 450]
        print(f"Total Nominals found: {len(nominals)}")
        for w in nominals:
            diff = w['x1'] - 432.00
            has_sign = w['text'].startswith('+') or w['text'].startswith('-')
            status = "OK" if abs(diff) < 0.5 and has_sign else f"FAILED (x1 diff={diff:+.2f}, sign={has_sign})"
            print(f"  Nominal: {w['text']:16s} | x1={w['x1']:6.2f} | target=432.00 | status={status}")

        # Check Saldos (target x1 = 571.00)
        saldos = [w for w in table_words if 500 <= w['x0'] <= 585 and ',' in w['text'] and not w['text'].startswith('+') and not w['text'].startswith('-')]
        print(f"Total Saldos found: {len(saldos)}")
        for w in saldos:
            diff = w['x1'] - 571.00
            status = "OK" if abs(diff) < 0.5 else f"DIFF ({diff:+.2f} pt)"
            print(f"  Saldo:   {w['text']:16s} | x1={w['x1']:6.2f} | target=571.00 | status={status}")
