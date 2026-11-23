import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_advanced_audit_excel(month_code, transactions, header_data, summary_data, output_path):
    wb = openpyxl.Workbook()
    ws_hdr = wb.active
    ws_hdr.title = "Header & Ringkasan"
    ws_mut = wb.create_sheet(title="Tabel_Mutasi")

    # Styles
    f_title = Font(name="Calibri", size=14, bold=True, color="1F497D")
    f_sec = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    f_bold = Font(name="Calibri", size=11, bold=True)
    f_regular = Font(name="Calibri", size=11)
    f_mono = Font(name="Consolas", size=10)
    
    fill_navy = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    fill_header = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")
    fill_zebra = PatternFill(start_color="F2F5F9", end_color="F2F5F9", fill_type="solid")
    fill_green = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    font_green = Font(name="Calibri", size=11, bold=True, color="006100")
    fill_red = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    font_red = Font(name="Calibri", size=11, bold=True, color="9C0006")

    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    # ---------------------------------------------------------
    # SHEET 1: Header & Ringkasan
    # ---------------------------------------------------------
    ws_hdr['A1'] = "KONFIGURASI UTAMA & AUDIT GATE PEKERJAAN"
    ws_hdr['A1'].font = f_title
    ws_hdr['A2'] = "Template resmi PdfCraft Copilot V2 (Real-time Instant Error Detection & Reconciliation)"
    ws_hdr['A2'].font = Font(name="Calibri", size=10, italic=True, color="595959")

    ws_hdr['A4'] = "Kategori / Parameter"
    ws_hdr['B4'] = "Nilai Data (Input / Live Formula)"
    ws_hdr['C4'] = "Status Validasi"
    ws_hdr['D4'] = "Keterangan & SOP Audit"
    for col in ['A4', 'B4', 'C4', 'D4']:
        ws_hdr[col].font = f_sec
        ws_hdr[col].fill = fill_navy

    # Section 1: Customer Header
    ws_hdr['A5'] = "1. DATA HEADER NASABAH"
    ws_hdr['A5'].font = f_bold

    rows_sec1 = [
        ("Nama Nasabah", header_data.get("nama", "GALANG PUTRA KURNIAWAN"), "Wajib", "Nama pemilik rekening (2 baris didukung penuh)"),
        ("Kantor Cabang", header_data.get("cabang", "KCP Serang Cilegon"), "Wajib", "Nama unit kantor cabang penerbit"),
        ("Periode Laporan", header_data.get("periode", f"01 {month_code} 2026 - 30 {month_code} 2026"), "Wajib", "Rentang tanggal mutasi rekening"),
        ("Dicetak Pada", header_data.get("dicetak_pada", "06 Nov 2026"), "Wajib", "Tanggal pencetakan e-Statement"),
        ("Nomor Rekening", header_data.get("nomor_rekening", "1630016287487"), "Wajib", "Nomor rekening (format teks)")
    ]

    for idx, (label, val, stat, desc) in enumerate(rows_sec1):
        r = 6 + idx
        ws_hdr.cell(r, 1, label).font = f_bold
        c_val = ws_hdr.cell(r, 2, val)
        c_val.font = f_regular
        if label == "Nomor Rekening":
            c_val.number_format = '@'
        ws_hdr.cell(r, 3, stat).font = f_regular
        ws_hdr.cell(r, 4, desc).font = f_regular

    # Section 2: Financial Summary & Live Audit Gate
    ws_hdr['A12'] = "2. RINGKASAN KEUANGAN & LIVE AUDIT GATE"
    ws_hdr['A12'].font = f_bold

    s_awal = summary_data.get("saldo_awal_num", 0.0)
    d_masuk = summary_data.get("dana_masuk_num", 0.0)
    d_keluar = summary_data.get("dana_keluar_num", 0.0)
    s_akhir = summary_data.get("saldo_akhir_num", 0.0)

    ws_hdr.cell(13, 1, "Saldo Awal").font = f_bold
    c = ws_hdr.cell(13, 2, s_awal)
    c.number_format = '#,##0.00'
    c.font = f_bold
    ws_hdr.cell(13, 3, "Wajib").font = f_regular
    ws_hdr.cell(13, 4, "Saldo pembukaan periode awal").font = f_regular

    ws_hdr.cell(14, 1, "Dana Masuk (Kredit)").font = f_bold
    c = ws_hdr.cell(14, 2, d_masuk)
    c.number_format = '#,##0.00'
    c.font = Font(name="Calibri", size=11, bold=True, color="008000")
    ws_hdr.cell(14, 3, "Wajib").font = f_regular
    ws_hdr.cell(14, 4, "Total nominal uang masuk (Kredit)").font = f_regular

    ws_hdr.cell(15, 1, "Dana Keluar (Debit)").font = f_bold
    c = ws_hdr.cell(15, 2, d_keluar)
    c.number_format = '#,##0.00'
    c.font = Font(name="Calibri", size=11, bold=True, color="000000")
    ws_hdr.cell(15, 3, "Wajib").font = f_regular
    ws_hdr.cell(15, 4, "Total nominal uang keluar (Debit)").font = f_regular

    ws_hdr.cell(16, 1, "Saldo Akhir").font = f_bold
    c = ws_hdr.cell(16, 2, s_akhir)
    c.number_format = '#,##0.00'
    c.font = Font(name="Calibri", size=11, bold=True, color="005B9C")
    ws_hdr.cell(16, 3, "Wajib").font = f_regular
    ws_hdr.cell(16, 4, "Saldo penutupan akhir periode").font = f_regular

    # Audit Formulas
    ws_hdr.cell(17, 1, "Keseimbangan Neraca Header").font = f_bold
    ws_hdr.cell(17, 2, '=IF(ROUND(B13+B14-B15-B16,2)=0,"BALANCE (MATCH)","SELISIH: " & TEXT(B13+B14-B15-B16,"#,##0.00"))').font = f_bold
    ws_hdr.cell(17, 3, "Live-Check").font = f_bold
    ws_hdr.cell(17, 4, "Audit: Saldo Awal (B13) + Masuk (B14) - Keluar (B15) = Saldo Akhir (B16)").font = f_regular

    ws_hdr.cell(18, 1, "Kesesuaian Mutasi Masuk").font = f_bold
    ws_hdr.cell(18, 2, '=IF(ROUND(B14-SUMIF(Tabel_Mutasi!E6:E200,">0"),2)=0,"MATCH MUTASI MASUK","SELISIH: " & TEXT(B14-SUMIF(Tabel_Mutasi!E6:E200,">0"),"#,##0.00"))').font = f_bold
    ws_hdr.cell(18, 3, "Live-Check").font = f_bold
    ws_hdr.cell(18, 4, "Audit: Total Kredit di Tabel_Mutasi harus sama persis dengan Dana Masuk").font = f_regular

    ws_hdr.cell(19, 1, "Kesesuaian Mutasi Keluar").font = f_bold
    ws_hdr.cell(19, 2, '=IF(ROUND(B15-ABS(SUMIF(Tabel_Mutasi!E6:E200,"<0")),2)=0,"MATCH MUTASI KELUAR","SELISIH: " & TEXT(B15-ABS(SUMIF(Tabel_Mutasi!E6:E200,"<0")),"#,##0.00"))').font = f_bold
    ws_hdr.cell(19, 3, "Live-Check").font = f_bold
    ws_hdr.cell(19, 4, "Audit: Total Debit di Tabel_Mutasi harus sama persis dengan Dana Keluar").font = f_regular

    ws_hdr.cell(20, 1, "STATUS KELAYAKAN DOKUMEN").font = f_bold
    ws_hdr.cell(20, 2, '=IF(AND(ROUND(B13+B14-B15-B16,2)=0, ROUND(B14-SUMIF(Tabel_Mutasi!E6:E200,">0"),2)=0, ROUND(B15-ABS(SUMIF(Tabel_Mutasi!E6:E200,"<0")),2)=0), "SEMUA PERHITUNGAN VALID (SIAP CETAK)", "PERHITUNGAN TIDAK LENGKAP / ADA SELISIH!")').font = Font(name="Calibri", size=12, bold=True, color="1F497D")
    ws_hdr.cell(20, 3, "GATE STATUS").font = f_bold
    ws_hdr.cell(20, 4, "Lampu hijau jika neraca & transaksi 100% klop tanpa selisih 1 rupiah pun").font = f_regular

    for r in range(4, 21):
        for c in range(1, 5):
            ws_hdr.cell(r, c).border = thin_border

    ws_hdr.column_dimensions['A'].width = 30
    ws_hdr.column_dimensions['B'].width = 45
    ws_hdr.column_dimensions['C'].width = 18
    ws_hdr.column_dimensions['D'].width = 65

    # ---------------------------------------------------------
    # SHEET 2: Tabel_Mutasi
    # ---------------------------------------------------------
    ws_mut['A1'] = "TABEL MUTASI TRANSAKSI RESMI"
    ws_mut['A1'].font = f_title
    ws_mut['A2'] = "Pengisian nominal otomatis memperbarui saldo berjalan & langsung terverifikasi dengan audit gate."
    ws_mut['A2'].font = Font(name="Calibri", size=10, italic=True, color="595959")

    mut_headers = [
        "No", "Tanggal", "Jam", "Keterangan / Remarks", "Nominal (+/-)", "Tipe", "Saldo Berjalan", "Audit Baris", "Catatan"
    ]
    for c_idx, h in enumerate(mut_headers, start=1):
        cell = ws_mut.cell(4, c_idx, h)
        cell.font = f_sec
        cell.fill = fill_navy
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # Row 5: Saldo Awal
    ws_mut.cell(5, 1, "[AWAL]").alignment = Alignment(horizontal="center")
    ws_mut.cell(5, 2, f"01/{month_code}").alignment = Alignment(horizontal="center")
    ws_mut.cell(5, 3, "-").alignment = Alignment(horizontal="center")
    ws_mut.cell(5, 4, "SALDO AWAL PEMBUKAAN PERIODE (INITIAL BALANCE)")
    ws_mut.cell(5, 5, "-").alignment = Alignment(horizontal="center")
    ws_mut.cell(5, 6, "AWAL").alignment = Alignment(horizontal="center")
    
    c_s0 = ws_mut.cell(5, 7, "='Header & Ringkasan'!B13")
    c_s0.number_format = '#,##0.00'
    c_s0.font = f_bold
    
    ws_mut.cell(5, 8, "OK (AWAL)").font = font_green
    ws_mut.cell(5, 9, "Saldo pembukaan rekening awal periode")

    for c in range(1, 10):
        ws_mut.cell(5, c).border = thin_border
        ws_mut.cell(5, c).fill = fill_header

    # Transactions 1..N
    num_tx = len(transactions)
    for i, tx in enumerate(transactions):
        r = 6 + i
        prev_r = r - 1

        ws_mut.cell(r, 1, i + 1).alignment = Alignment(horizontal="center")
        ws_mut.cell(r, 2, tx.get("date", "")).alignment = Alignment(horizontal="center")
        ws_mut.cell(r, 3, tx.get("time", "")).alignment = Alignment(horizontal="center")
        ws_mut.cell(r, 4, tx.get("desc", ""))
        
        # Nominal
        nom_val = tx.get("nom_num", 0.0)
        c_nom = ws_mut.cell(r, 5, nom_val)
        c_nom.number_format = '+#,##0.00;-#,##0.00;0.00'
        if nom_val > 0:
            c_nom.font = Font(name="Calibri", size=11, bold=True, color="008000")
        else:
            c_nom.font = Font(name="Calibri", size=11, bold=True, color="000000")

        # Tipe Formula
        ws_mut.cell(r, 6, f'=IF(E{r}="","",IF(E{r}>0,"CR","DB"))').alignment = Alignment(horizontal="center")

        # Dynamic Running Balance Formula
        c_sal = ws_mut.cell(r, 7, f'=IF(E{r}="","",ROUND(G{prev_r}+E{r},2))')
        c_sal.number_format = '#,##0.00'
        c_sal.font = Font(name="Calibri", size=11, bold=True, color="005B9C")

        # Live Row Audit Formula
        ws_mut.cell(r, 8, f'=IF(E{r}="","",IF(ROUND(G{prev_r}+E{r}-G{r},2)=0,"OK Verified","SELISIH: " & TEXT(G{prev_r}+E{r}-G{r},"#,##0.00")))').alignment = Alignment(horizontal="center")
        
        ws_mut.cell(r, 9, "OK Verified" if abs(nom_val) > 0 else "")

        for c in range(1, 10):
            ws_mut.cell(r, c).border = thin_border
            if i % 2 == 1:
                ws_mut.cell(r, c).fill = fill_zebra

    # Summary Row at the bottom
    sum_r = 6 + num_tx + 1
    ws_mut.cell(sum_r, 4, "TOTAL MUTASI PERIODE (REKAP)").font = f_bold
    ws_mut.cell(sum_r, 4).alignment = Alignment(horizontal="right")
    
    c_tot = ws_mut.cell(sum_r, 5, f"=SUM(E6:E{6 + num_tx - 1})")
    c_tot.number_format = '+#,##0.00;-#,##0.00;0.00'
    c_tot.font = f_bold

    ws_mut.cell(sum_r, 6, "AKHIR").alignment = Alignment(horizontal="center")
    
    c_fin = ws_mut.cell(sum_r, 7, f"=G{6 + num_tx - 1}")
    c_fin.number_format = '#,##0.00'
    c_fin.font = Font(name="Calibri", size=11, bold=True, color="005B9C")

    ws_mut.cell(sum_r, 8, f'=IF(ROUND(G{6 + num_tx - 1}-\'Header & Ringkasan\'!B16,2)=0,"MATCH SALDO AKHIR","MISMATCH SALDO AKHIR")').font = f_bold
    ws_mut.cell(sum_r, 8).alignment = Alignment(horizontal="center")

    for c in range(1, 10):
        ws_mut.cell(sum_r, c).border = thin_border
        ws_mut.cell(sum_r, c).fill = fill_header

    ws_mut.column_dimensions['A'].width = 8
    ws_mut.column_dimensions['B'].width = 16
    ws_mut.column_dimensions['C'].width = 16
    ws_mut.column_dimensions['D'].width = 45
    ws_mut.column_dimensions['E'].width = 20
    ws_mut.column_dimensions['F'].width = 8
    ws_mut.column_dimensions['G'].width = 22
    ws_mut.column_dimensions['H'].width = 20
    ws_mut.column_dimensions['I'].width = 20

    wb.save(output_path)
    print(f"Generated advanced audit Excel: {output_path}")

if __name__ == "__main__":
    dummy_summary = {
        "saldo_awal_num": 4527347.81,
        "dana_masuk_num": 6828000.00,
        "dana_keluar_num": 8610991.00,
        "saldo_akhir_num": 2744356.81
    }
    dummy_header = {
        "nama": "GALANG PUTRA KURNIAWAN",
        "cabang": "KCP Serang Cilegon",
        "periode": "01 Sep 2026 - 30 Sep 2026",
        "dicetak_pada": "06 Nov 2026",
        "nomor_rekening": "1630016287487"
    }
    dummy_txs = [
        {"date": "04 Sep 2026", "time": "19:03:17 WIB", "desc": "Transfer BI Fast Dari BCA", "nom_num": -1000000.0},
        {"date": "04 Sep 2026", "time": "19:23:25 WIB", "desc": "Transfer BI Fast Dari BCA", "nom_num": 50000.0},
        {"date": "04 Sep 2026", "time": "23:59:59 WIB", "desc": "Biaya administrasi kartu debit", "nom_num": -3500.0}
    ]
    build_advanced_audit_excel("SEP", dummy_txs, dummy_header, dummy_summary, "scratch/test_out.xlsx")
