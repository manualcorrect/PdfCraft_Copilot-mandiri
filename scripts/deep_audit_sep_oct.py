import os
import openpyxl
import pdfplumber

def audit_dataset(month_name, folder_path, pdf_name, excel_name):
    print(f"\n{'='*20} AUDITING {month_name} {'='*20}")
    excel_path = os.path.join(folder_path, excel_name)
    pdf_path = os.path.join(folder_path, pdf_name)
    
    # 1. Audit Excel
    if not os.path.exists(excel_path):
        print(f"ERROR: Excel file not found: {excel_path}")
        return
        
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    print("Sheets in Excel:", wb.sheetnames)
    
    ws1 = wb["Header & Ringkasan"]
    ws2 = wb["Tabel_Mutasi"]
    
    print("\n--- Header & Ringkasan ---")
    for r in range(5, 27):
        p_name = ws1.cell(r, 1).value
        p_val = ws1.cell(r, 2).value
        p_stat = ws1.cell(r, 3).value
        if p_name:
            print(f"  {p_name:35}: {repr(p_val)}")
            
    # Summary values in Sheet 1
    sawal = ws1.cell(22, 2).value
    dmasuk = ws1.cell(23, 2).value
    dkeluar = ws1.cell(24, 2).value
    
    # Parse numbers safely
    def to_float(v):
        if v is None: return 0.0
        if isinstance(v, (int, float)): return float(v)
        s = str(v).replace("Rp", "").replace(" ", "").replace(".", "").replace(",", ".").replace("+", "").replace("-", "")
        return float(s)
        
    sawal_f = to_float(sawal)
    dmasuk_f = to_float(dmasuk)
    dkeluar_f = to_float(dkeluar)
    sakhir_calc = sawal_f + dmasuk_f - dkeluar_f
    print(f"\nFinancial Summary Header:")
    print(f"  Saldo Awal   : {sawal_f:,.2f}")
    print(f"  Dana Masuk   : {dmasuk_f:,.2f}")
    print(f"  Dana Keluar  : {dkeluar_f:,.2f}")
    print(f"  Saldo Akhir  : {sakhir_calc:,.2f}")
    
    # 2. Audit Tabel_Mutasi
    print("\n--- Tabel_Mutasi Inspection ---")
    row5 = [ws2.cell(5, c).value for c in range(1, 8)]
    print(f"Row 5 (Awal): {row5}")
    sawal_tabel = to_float(ws2.cell(5, 7).value)
    
    active_txs = []
    total_cr = 0.0
    total_db = 0.0
    chain_errors = []
    prev_saldo = sawal_tabel
    
    for r in range(6, ws2.max_row + 1):
        no_val = ws2.cell(r, 1).value
        tgl_val = ws2.cell(r, 2).value
        jam_val = ws2.cell(r, 3).value
        uraian_val = ws2.cell(r, 4).value
        nom_val = ws2.cell(r, 5).value
        saldo_val = ws2.cell(r, 7).value
        
        if nom_val is not None:
            nom_f = to_float(nom_val)
            # handle negative sign
            is_neg = False
            if isinstance(nom_val, (int, float)) and nom_val < 0:
                is_neg = True
            elif isinstance(nom_val, str) and "-" in nom_val:
                is_neg = True
            
            if is_neg:
                nom_signed = -nom_f
                total_db += nom_f
            else:
                nom_signed = nom_f
                total_cr += nom_f
                
            saldo_f = to_float(saldo_val)
            expected_saldo = round(prev_saldo + nom_signed, 2)
            actual_saldo = round(saldo_f, 2)
            
            if abs(nom_f) > 0.001:
                active_txs.append({
                    "row": r,
                    "tgl": tgl_val,
                    "jam": jam_val,
                    "nom": nom_signed,
                    "saldo": saldo_f
                })
                if abs(expected_saldo - actual_saldo) > 0.01:
                    chain_errors.append(f"Row {r}: prev={prev_saldo:,.2f} + nom={nom_signed:,.2f} = exp {expected_saldo:,.2f} != act {actual_saldo:,.2f}")
            prev_saldo = actual_saldo

    print(f"Total rows in Excel mutasi: {ws2.max_row}")
    print(f"Active transactions (> 0): {len(active_txs)}")
    print(f"Total Kredit (Dana Masuk) dari Mutasi : {total_cr:,.2f} (Header: {dmasuk_f:,.2f}) -> Match: {abs(total_cr - dmasuk_f) < 0.01}")
    print(f"Total Debit (Dana Keluar) dari Mutasi : {total_db:,.2f} (Header: {dkeluar_f:,.2f}) -> Match: {abs(total_db - dkeluar_f) < 0.01}")
    print(f"Saldo Akhir Mutasi                    : {prev_saldo:,.2f} (Header: {sakhir_calc:,.2f}) -> Match: {abs(prev_saldo - sakhir_calc) < 0.01}")
    if chain_errors:
        print(f"WARNING: {len(chain_errors)} Chain Errors found:")
        for err in chain_errors[:5]:
            print("  ", err)
    else:
        print("Chain Saldo Berjalan: 100% KLOP & KONSISTEN!")
        
    # 3. Audit PDF Source
    if not os.path.exists(pdf_path):
        print(f"ERROR: PDF file not found: {pdf_path}")
        return
        
    with pdfplumber.open(pdf_path) as pdf:
        print(f"\n--- PDF Source: {pdf_name} ({len(pdf.pages)} pages) ---")
        pdf_tx_count = 0
        for p_idx, page in enumerate(pdf.pages):
            words = page.extract_words()
            min_top = 320 if p_idx == 0 else 200
            table_words = [w for w in words if min_top <= w['top'] <= 800]
            wib_words = [w for w in table_words if w['text'] == 'WIB']
            print(f"  Page {p_idx+1}: {len(wib_words)} transactions detected via WIB")
            pdf_tx_count += len(wib_words)
        print(f"Total transactions in PDF: {pdf_tx_count} vs Excel active txs: {len(active_txs)}")
        if pdf_tx_count != len(active_txs):
            print(f"MISMATCH WARNING: PDF has {pdf_tx_count} transactions, but Excel has {len(active_txs)} active transactions!")
        else:
            print("Row Count PDF vs Excel: 100% SESUAI!")

sep_dir = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP"
oct_dir = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT"

audit_dataset("SEPTEMBER 2026", sep_dir, "3.pdf", "Template_Mutasi.xlsx")
audit_dataset("OKTOBER 2026", oct_dir, "1.pdf", "Template_Mutasi.xlsx")
