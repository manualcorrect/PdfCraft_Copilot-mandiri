import pdfplumber
import openpyxl

okt_dir = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\okt"
pdf_path = f"{okt_dir}\\0.pdf"
xlsx_path = f"{okt_dir}\\Template_Mutasi_OKT.xlsx"

wb = openpyxl.load_workbook(xlsx_path, data_only=True)
ws_mutasi = wb["Tabel_Mutasi"]

print(f"Tabel_Mutasi max_row={ws_mutasi.max_row}, max_column={ws_mutasi.max_column}")

excel_tx = []
for r in range(6, ws_mutasi.max_row + 1):
    c_no = ws_mutasi.cell(r, 1).value
    c_date = ws_mutasi.cell(r, 2).value
    c_time = ws_mutasi.cell(r, 3).value
    c_desc = ws_mutasi.cell(r, 4).value
    c_nominal = ws_mutasi.cell(r, 5).value
    c_type = ws_mutasi.cell(r, 6).value
    c_saldo = ws_mutasi.cell(r, 7).value
    
    if c_no is None and c_date is None and c_desc is None and c_nominal is None:
        continue
    
    excel_tx.append({
        'excel_row': r,
        'no': c_no,
        'date': str(c_date or '').strip(),
        'time': str(c_time or '').strip(),
        'desc': str(c_desc or '').strip(),
        'nominal': float(c_nominal or 0),
        'type': str(c_type or '').strip(),
        'saldo': float(c_saldo or 0) if c_saldo is not None else None
    })

print(f"\nTotal Active Transactions in Excel Tabel_Mutasi: {len(excel_tx)}")
print("First 3 Transactions:")
for t in excel_tx[:3]:
    print(" ", t)
print("Last 3 Transactions:")
for t in excel_tx[-3:]:
    print(" ", t)

# Calculate totals
kredit_tx = [t['nominal'] for t in excel_tx if t['nominal'] > 0 or t['type'] == 'CR']
debit_tx = [abs(t['nominal']) for t in excel_tx if t['nominal'] < 0 or t['type'] == 'DB']
tot_kredit = sum(kredit_tx)
tot_debit = sum(debit_tx)
print(f"\nExcel Sum Kredit (CR): {tot_kredit:,.2f} ({len(kredit_tx)} tx)")
print(f"Excel Sum Debit (DB):  {tot_debit:,.2f} ({len(debit_tx)} tx)")

# Check Header & Ringkasan
ws_hr = wb["Header & Ringkasan"]
saldo_awal = float(ws_hr['B22'].value)
dana_masuk = float(ws_hr['B23'].value)
dana_keluar = float(ws_hr['B24'].value)
saldo_akhir = float(ws_hr['B25'].value)

print(f"\nHeader & Ringkasan:")
print(f"  Saldo Awal:  {saldo_awal:,.2f}")
print(f"  Dana Masuk:  {dana_masuk:,.2f} (diff with Excel sum: {dana_masuk - tot_kredit})")
print(f"  Dana Keluar: {dana_keluar:,.2f} (diff with Excel sum: {abs(dana_keluar) - tot_debit})")
calc_akhir = saldo_awal + tot_kredit - tot_debit
print(f"  Calculated Saldo Akhir: {calc_akhir:,.2f}")
print(f"  Reported Saldo Akhir:   {saldo_akhir:,.2f}")
print(f"  Diff: {calc_akhir - saldo_akhir}")

# Audit 0.pdf
with pdfplumber.open(pdf_path) as pdf:
    print(f"\n0.pdf has {len(pdf.pages)} pages")
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        col_no = [w for w in words if 15 <= w['x0'] <= 35 and 150 <= w['top'] <= 800 and w['text'].isdigit()]
        col_no.sort(key=lambda w: w['top'])
        print(f"  Page {p_idx+1}: {len(col_no)} tx numbers: {[w['text'] for w in col_no]}")
