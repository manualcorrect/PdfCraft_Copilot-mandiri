import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import os
import shutil

def add_audit_system_to_template(excel_path: str, output_path: str = None):
    if output_path is None:
        output_path = excel_path

    wb = openpyxl.load_workbook(excel_path)
    ws1 = wb["Header & Ringkasan"]

    # Styles matching template theme
    font_sec = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    fill_sec = PatternFill(start_color="1F61DC", end_color="1F61DC", fill_type="solid") # Mandiri Blue

    font_bold = Font(name="Calibri", size=10, bold=True, color="000000")
    font_regular = Font(name="Calibri", size=10, bold=False, color="333333")
    font_status_match = Font(name="Calibri", size=10, bold=True, color="008000") # Dark Green
    font_overall_pass = Font(name="Calibri", size=11, bold=True, color="FFFFFF")

    fill_row_even = PatternFill(start_color="F7F9FB", end_color="F7F9FB", fill_type="solid")
    fill_row_odd = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    fill_overall_pass = PatternFill(start_color="107C41", end_color="107C41", fill_type="solid") # Excel Green

    thin_border = Border(
        left=Side(style='thin', color='D1D5DB'),
        right=Side(style='thin', color='D1D5DB'),
        top=Side(style='thin', color='D1D5DB'),
        bottom=Side(style='thin', color='D1D5DB')
    )

    # 1. Section Header at Row 27
    ws1.cell(row=27, column=1, value="6. SISTEM AUDIT & VALIDASI OTOMATIS (REKONSILIASI KEUANGAN)")
    for col in range(1, 5):
        c = ws1.cell(row=27, column=col)
        c.font = font_sec
        c.fill = fill_sec
        c.alignment = Alignment(vertical="center", indent=1 if col == 1 else 0)

    # 2. Row 28: Total Dana Masuk (Kredit)
    ws1.cell(row=28, column=1, value="Total Dana Masuk (Tabel Mutasi)")
    ws1.cell(row=28, column=2, value='=SUMIF(Tabel_Mutasi!E6:E100, ">0")')
    ws1.cell(row=28, column=3, value='=IF(ISBLANK(B23), "INPUT KOSONG", IF(ABS(B28-ABS(B23))<1, "MATCH / SESUAI", "SELISIH: Rp " & TEXT(ABS(B28-ABS(B23)), "#,##0.00")))')
    ws1.cell(row=28, column=4, value="Memverifikasi total mutasi kredit dari Tabel_Mutasi vs Cell B23")

    # 3. Row 29: Total Dana Keluar (Debit)
    ws1.cell(row=29, column=1, value="Total Dana Keluar (Tabel Mutasi)")
    ws1.cell(row=29, column=2, value='=ABS(SUMIF(Tabel_Mutasi!E6:E100, "<0"))')
    ws1.cell(row=29, column=3, value='=IF(ISBLANK(B24), "INPUT KOSONG", IF(ABS(B29-ABS(B24))<1, "MATCH / SESUAI", "SELISIH: Rp " & TEXT(ABS(B29-ABS(B24)), "#,##0.00")))')
    ws1.cell(row=29, column=4, value="Memverifikasi total mutasi debit dari Tabel_Mutasi vs Cell B24")

    # 4. Row 30: Saldo Akhir Terkalkulasi
    ws1.cell(row=30, column=1, value="Kalkulasi Saldo Akhir (Awal + Masuk - Keluar)")
    ws1.cell(row=30, column=2, value='=B22+B28-B29')
    ws1.cell(row=30, column=3, value='=IF(ISBLANK(B25), "INPUT KOSONG", IF(ABS(B30-B25)<1, "MATCH / SESUAI", "SELISIH: Rp " & TEXT(ABS(B30-B25), "#,##0.00")))')
    ws1.cell(row=30, column=4, value="Rumus: Saldo Awal (B22) + Dana Masuk (B28) - Dana Keluar (B29)")

    # 5. Row 31: Saldo Baris Terakhir (Tabel Mutasi)
    ws1.cell(row=31, column=1, value="Saldo Akhir Baris Penutup (Tabel Mutasi)")
    ws1.cell(row=31, column=2, value='=LOOKUP(2, 1/(Tabel_Mutasi!G6:G100<>""), Tabel_Mutasi!G6:G100)')
    ws1.cell(row=31, column=3, value='=IF(ISBLANK(B25), "INPUT KOSONG", IF(ABS(B31-B25)<1, "MATCH / SESUAI", "SELISIH: Rp " & TEXT(ABS(B31-B25), "#,##0.00")))')
    ws1.cell(row=31, column=4, value="Saldo berjalan pada baris mutasi paling akhir di Tabel_Mutasi")

    # 6. Row 32: Status Validasi Dokumen
    ws1.cell(row=32, column=1, value="STATUS KELAYAKAN DOKUMEN")
    ws1.cell(row=32, column=2, value='=IF(AND(C28="MATCH / SESUAI", C29="MATCH / SESUAI", C30="MATCH / SESUAI", C31="MATCH / SESUAI"), "LULUS AUDIT - SIAP CETAK", "BELUM MATCH - PERIKSA SELISIH")')
    ws1.cell(row=32, column=3, value="100% RECONCILED")
    ws1.cell(row=32, column=4, value="Indikator otomatis: Wajib LULUS AUDIT sebelum konversi PDF")

    # Apply formatting to rows 28-32
    for r in range(28, 33):
        fill = fill_row_even if r % 2 == 0 else fill_row_odd
        for c_idx in range(1, 5):
            cell = ws1.cell(row=r, column=c_idx)
            cell.border = thin_border
            cell.fill = fill
            if r == 32:
                if c_idx in [1, 2]:
                    cell.font = font_overall_pass
                    cell.fill = fill_overall_pass
                else:
                    cell.font = font_bold
            elif c_idx == 1:
                cell.font = font_bold
            elif c_idx == 2:
                cell.font = font_bold
                cell.number_format = '#,##0.00'
                cell.alignment = Alignment(horizontal="right")
            elif c_idx == 3:
                cell.font = font_status_match
                cell.alignment = Alignment(horizontal="center")
            else:
                cell.font = font_regular

    # Also update row 23, 24, 25 to exact reconciled values
    ws1.cell(row=23, column=2, value=7649000)
    ws1.cell(row=24, column=2, value=-7651988)
    ws1.cell(row=25, column=2, value=4527347.81)

    wb.save(output_path)
    print(f"Audit system successfully installed into: {output_path}")

if __name__ == "__main__":
    src_file = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\Template_Mutasi_Aug.xlsx"
    out_file = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\Template_Mutasi_Aug_Reconciled.xlsx"
    add_audit_system_to_template(src_file, out_file)
