import os, openpyxl, pdfplumber

base_dir = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru"

months = ["AUG", "SEP", "OCT"]

print("=========================================================================")
print("   COMPREHENSIVE AUDIT REPORT: OFFICIAL NUMBERED OUTPUT 1")
print("=========================================================================\n")

for m in months:
    pdf_path = os.path.join(base_dir, m, f"REK_GALANG_{m}_OUTPUT_1.pdf")
    xls_path = os.path.join(base_dir, m, f"Template_Mutasi_{m}_OUTPUT_1.xlsx")
    
    print(f"\n>>> AUDITING MONTH: {m} <<<")
    print(f"PDF: {pdf_path} (Exists: {os.path.exists(pdf_path)}, Size: {os.path.getsize(pdf_path):,} bytes)")
    print(f"Excel: {xls_path} (Exists: {os.path.exists(xls_path)}, Size: {os.path.getsize(xls_path):,} bytes)")

    # 1. Audit Excel
    wb = openpyxl.load_workbook(xls_path, data_only=True)
    ws1 = wb["Header & Ringkasan"]
    ws2 = wb["Tabel_Mutasi"]

    sawal = ws1.cell(13, 2).value
    dmasuk = ws1.cell(14, 2).value
    dkeluar = ws1.cell(15, 2).value
    sakhir = ws1.cell(16, 2).value
    stat_neraca = ws1.cell(17, 2).value
    stat_masuk = ws1.cell(18, 2).value
    stat_keluar = ws1.cell(19, 2).value
    stat_gate = ws1.cell(20, 2).value

    print(f"  [Excel Header & Ringkasan]")
    print(f"    Saldo Awal  : {sawal:,.2f}")
    print(f"    Dana Masuk  : {dmasuk:,.2f}")
    print(f"    Dana Keluar : {dkeluar:,.2f}")
    print(f"    Saldo Akhir : {sakhir:,.2f}")
    print(f"    Neraca      : {stat_neraca}")
    print(f"    Audit Masuk : {stat_masuk}")
    print(f"    Audit Keluar: {stat_keluar}")
    print(f"    Gate Status : {stat_gate}")

    # 2. Audit PDF
    with pdfplumber.open(pdf_path) as pdf:
        print(f"  [PDF Inspection]")
        print(f"    Total Pages: {len(pdf.pages)}")
        all_fonts = set()
        for p_idx, page in enumerate(pdf.pages):
            for c in page.chars:
                all_fonts.add(c.get('fontname', 'unknown'))
        print(f"    Fonts present: {sorted(list(all_fonts))}")
        
        # Check foreign fonts
        foreign = [f for f in all_fonts if "TTInterphases" not in f and "TT_Interphases" not in f]
        print(f"    Foreign fonts: {foreign} (PASSED: {len(foreign) == 0})")

        # Check Page 1 Header coordinates
        p1 = pdf.pages[0]
        words = p1.extract_words()
        acc_words = [w for w in words if "1630016287487" in w['text']]
        if acc_words:
            print(f"    Nomor Rekening x0: {acc_words[0]['x0']:.2f} pt (Target: 160.00 pt, diff: {abs(acc_words[0]['x0'] - 160.0):.2f} pt)")
        
        name_words = [w for w in words if "GALANG" in w['text']]
        if name_words:
            print(f"    Nama x0: {name_words[0]['x0']:.2f} pt")

print("\nAudit completed!")
