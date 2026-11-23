import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def upgrade_sheet1_audit(src_excel_path, out_excel_path, target_month_str):
    print(f"Loading {src_excel_path} -> Saving to {out_excel_path}...")
    wb = openpyxl.load_workbook(src_excel_path)
    ws = wb['Header & Ringkasan']
    
    # Styles
    font_bold = Font(name="Calibri", size=11, bold=True)
    font_regular = Font(name="Calibri", size=11)
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_summary_title = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    
    fill_navy = PatternFill(start_color="1F61DC", end_color="1F61DC", fill_type="solid")
    fill_row_label = PatternFill(start_color="F7F9FB", end_color="F7F9FB", fill_type="solid")
    fill_calc = PatternFill(start_color="EEF4FF", end_color="EEF4FF", fill_type="solid")
    fill_status = PatternFill(start_color="E8F5E9", end_color="E8F5E9", fill_type="solid")
    fill_banner = PatternFill(start_color="0A3981", end_color="0A3981", fill_type="solid")
    
    thin_border = Border(
        left=Side(style='thin', color='D3D3D3'),
        right=Side(style='thin', color='D3D3D3'),
        top=Side(style='thin', color='D3D3D3'),
        bottom=Side(style='thin', color='D3D3D3')
    )
    
    # Update Target Bulan & Tahun at row 20
    ws.cell(20, 2).value = target_month_str
    
    # Handle section merges to span across A..E
    merge_rows = [1, 2, 5, 9, 16, 19, 21]
    for mr in merge_rows:
        # Check if already merged as A..D
        for rng in list(ws.merged_cells.ranges):
            if rng.min_row == mr and rng.max_row == mr and rng.min_col == 1:
                ws.unmerge_cells(str(rng))
        # Re-merge as A..E
        ws.merge_cells(start_row=mr, start_column=1, end_row=mr, end_column=5)
        # Apply style to the merged row
        for c in range(1, 6):
            cell = ws.cell(mr, c)
            if mr in [5, 9, 16, 19, 21]:
                cell.fill = fill_navy
                cell.font = font_summary_title
            cell.border = thin_border
    
    # Header row 4
    headers = [
        (1, "Kategori / Parameter"),
        (2, "Nilai Data (Input Header)"),
        (3, "Hasil Hitung Mutasi (Auto)"),
        (4, "Status Rekonsiliasi (Audit)"),
        (5, "Panduan Pengisian")
    ]
    for col_idx, text in headers:
        cell = ws.cell(4, col_idx)
        cell.value = text
        cell.font = font_header
        cell.fill = fill_navy
        cell.alignment = Alignment(horizontal="center" if col_idx in [2, 3, 4] else "left", vertical="center")
        cell.border = thin_border
        
    # Section 5 Title at row 21
    ws.cell(21, 1).value = "5. RINGKASAN KEUANGAN & AUDIT REKONSILIASI (FINANCIAL SUMMARY)"
    ws.cell(21, 1).font = font_summary_title
    ws.cell(21, 1).fill = fill_navy
    ws.cell(21, 1).alignment = Alignment(horizontal="left", vertical="center")
        
    # Row 22: Saldo Awal
    ws.cell(22, 1).value = "Saldo Awal"
    ws.cell(22, 1).fill = fill_row_label
    ws.cell(22, 1).font = font_bold
    ws.cell(22, 1).border = thin_border
    
    c_b22 = ws.cell(22, 2)
    c_b22.number_format = '#,##0.00'
    c_b22.border = thin_border
    c_b22.alignment = Alignment(horizontal="right", vertical="center")
    
    c_c22 = ws.cell(22, 3)
    c_c22.value = "=Tabel_Mutasi!G5"
    c_c22.number_format = '#,##0.00'
    c_c22.font = font_bold
    c_c22.fill = fill_calc
    c_c22.border = thin_border
    c_c22.alignment = Alignment(horizontal="right", vertical="center")
    
    c_d22 = ws.cell(22, 4)
    c_d22.value = '=IF(ISBLANK(B22), "KOSONG", IF(ABS(B22-C22)<0.01, "SESUAI", "SELISIH: " & TEXT(B22-C22, "#,##0.00")))'
    c_d22.font = font_bold
    c_d22.fill = fill_status
    c_d22.border = thin_border
    c_d22.alignment = Alignment(horizontal="center", vertical="center")
    
    ws.cell(22, 5).value = "Saldo pembuka rekening awal periode (Tabel_Mutasi G5)"
    ws.cell(22, 5).font = font_regular
    ws.cell(22, 5).border = thin_border
    
    # Row 23: Dana Masuk (Kredit)
    ws.cell(23, 1).value = "Dana Masuk (Kredit)"
    ws.cell(23, 1).fill = fill_row_label
    ws.cell(23, 1).font = font_bold
    ws.cell(23, 1).border = thin_border
    
    c_b23 = ws.cell(23, 2)
    c_b23.number_format = '#,##0.00'
    c_b23.border = thin_border
    c_b23.alignment = Alignment(horizontal="right", vertical="center")
    
    c_c23 = ws.cell(23, 3)
    c_c23.value = '=SUMIF(Tabel_Mutasi!E6:E200, ">0")'
    c_c23.number_format = '#,##0.00'
    c_c23.font = font_bold
    c_c23.fill = fill_calc
    c_c23.border = thin_border
    c_c23.alignment = Alignment(horizontal="right", vertical="center")
    
    c_d23 = ws.cell(23, 4)
    c_d23.value = '=IF(ISBLANK(B23), "KOSONG", IF(ABS(B23-C23)<0.01, "SESUAI", "SELISIH: " & TEXT(B23-C23, "#,##0.00")))'
    c_d23.font = font_bold
    c_d23.fill = fill_status
    c_d23.border = thin_border
    c_d23.alignment = Alignment(horizontal="center", vertical="center")
    
    ws.cell(23, 5).value = "Total mutasi kredit (Warna Hijau #06AA6F)"
    ws.cell(23, 5).font = font_regular
    ws.cell(23, 5).border = thin_border
    
    # Row 24: Dana Keluar (Debit)
    ws.cell(24, 1).value = "Dana Keluar (Debit)"
    ws.cell(24, 1).fill = fill_row_label
    ws.cell(24, 1).font = font_bold
    ws.cell(24, 1).border = thin_border
    
    c_b24 = ws.cell(24, 2)
    c_b24.number_format = '#,##0.00'
    c_b24.border = thin_border
    c_b24.alignment = Alignment(horizontal="right", vertical="center")
    
    c_c24 = ws.cell(24, 3)
    c_c24.value = '=-ABS(SUMIF(Tabel_Mutasi!E6:E200, "<0"))'
    c_c24.number_format = '#,##0.00'
    c_c24.font = font_bold
    c_c24.fill = fill_calc
    c_c24.border = thin_border
    c_c24.alignment = Alignment(horizontal="right", vertical="center")
    
    c_d24 = ws.cell(24, 4)
    c_d24.value = '=IF(ISBLANK(B24), "KOSONG", IF(ABS(ABS(B24)-ABS(C24))<0.01, "SESUAI", "SELISIH: " & TEXT(ABS(B24)-ABS(C24), "#,##0.00")))'
    c_d24.font = font_bold
    c_d24.fill = fill_status
    c_d24.border = thin_border
    c_d24.alignment = Alignment(horizontal="center", vertical="center")
    
    ws.cell(24, 5).value = "Total mutasi debit (Format: -Rp xxx.xxx,xx)"
    ws.cell(24, 5).font = font_regular
    ws.cell(24, 5).border = thin_border
    
    # Row 25: Saldo Akhir
    ws.cell(25, 1).value = "Saldo Akhir"
    ws.cell(25, 1).fill = fill_row_label
    ws.cell(25, 1).font = font_bold
    ws.cell(25, 1).border = thin_border
    
    c_b25 = ws.cell(25, 2)
    c_b25.number_format = '#,##0.00'
    c_b25.border = thin_border
    c_b25.alignment = Alignment(horizontal="right", vertical="center")
    
    c_c25 = ws.cell(25, 3)
    c_c25.value = '=C22+C23+C24'
    c_c25.number_format = '#,##0.00'
    c_c25.font = font_bold
    c_c25.fill = fill_calc
    c_c25.border = thin_border
    c_c25.alignment = Alignment(horizontal="right", vertical="center")
    
    c_d25 = ws.cell(25, 4)
    c_d25.value = '=IF(ISBLANK(B25), "KOSONG", IF(ABS(B25-C25)<0.01, "SESUAI", "SELISIH: " & TEXT(B25-C25, "#,##0.00")))'
    c_d25.font = font_bold
    c_d25.fill = fill_status
    c_d25.border = thin_border
    c_d25.alignment = Alignment(horizontal="center", vertical="center")
    
    ws.cell(25, 5).value = "Saldo penutupan akhir: Saldo Awal + Masuk - Keluar"
    ws.cell(25, 5).font = font_regular
    ws.cell(25, 5).border = thin_border
    
    # Row 26: STATUS KELAYAKAN DOKUMEN (BANNER)
    ws.cell(26, 1).value = "STATUS KELAYAKAN DOKUMEN"
    ws.cell(26, 1).font = font_header
    ws.cell(26, 1).fill = fill_banner
    ws.cell(26, 1).border = thin_border
    
    c_b26 = ws.cell(26, 2)
    c_b26.value = '=IF(AND(D22="SESUAI", D23="SESUAI", D24="SESUAI", D25="SESUAI"), "LULUS AUDIT (KLOP 100%)", "BELUM KLOP (PERIKSA SELISIH)")'
    c_b26.font = font_header
    c_b26.fill = fill_banner
    c_b26.alignment = Alignment(horizontal="center", vertical="center")
    c_b26.border = thin_border
    
    c_c26 = ws.cell(26, 3)
    c_c26.value = '=IF(B26="LULUS AUDIT (KLOP 100%)", "100% MATCH", "ADA SELISIH")'
    c_c26.font = font_header
    c_c26.fill = fill_banner
    c_c26.alignment = Alignment(horizontal="center", vertical="center")
    c_c26.border = thin_border
    
    c_d26 = ws.cell(26, 4)
    c_d26.value = '=IF(B26="LULUS AUDIT (KLOP 100%)", "SIAP PROSES PDF", "PERIKSA MUTASI")'
    c_d26.font = font_header
    c_d26.fill = fill_banner
    c_d26.alignment = Alignment(horizontal="center", vertical="center")
    c_d26.border = thin_border
    
    c_e26 = ws.cell(26, 5)
    c_e26.value = "Verifikasi otomatis: Nilai Header wajib 100% klop dengan Tabel_Mutasi"
    c_e26.font = font_regular
    c_e26.border = thin_border
    
    # Clear any merged cells below row 26
    for rng in list(ws.merged_cells.ranges):
        if rng.min_row >= 27:
            ws.unmerge_cells(str(rng))
            
    # Clear old rows 27 to 35
    for r in range(27, 36):
        for c in range(1, 7):
            cell = ws.cell(r, c)
            cell.value = None
            cell.fill = PatternFill(fill_type=None)
            cell.border = Border()
            
    # Adjust column dimensions
    ws.column_dimensions['A'].width = 32.0
    ws.column_dimensions['B'].width = 28.0
    ws.column_dimensions['C'].width = 26.0
    ws.column_dimensions['D'].width = 24.0
    ws.column_dimensions['E'].width = 48.0
    
    os.makedirs(os.path.dirname(out_excel_path), exist_ok=True)
    wb.save(out_excel_path)
    print(f"Successfully saved upgraded template to {out_excel_path}!")

if __name__ == "__main__":
    sep_src = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\Template_Mutasi.xlsx"
    oct_src = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\Template_Mutasi.xlsx"
    
    sep_out = r"output\Template_Mutasi_SEP_Reconciled.xlsx"
    oct_out = r"output\Template_Mutasi_OCT_Reconciled.xlsx"
    
    upgrade_sheet1_audit(sep_src, sep_out, "Sep 2026")
    upgrade_sheet1_audit(oct_src, oct_out, "Oct 2026")
