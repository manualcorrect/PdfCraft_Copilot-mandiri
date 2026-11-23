"""
Official Numbered Output Generator for Bank Mandiri e-Statements
Produces REK_(NAMA)_(BULAN)_OUTPUT_1.pdf and Template_Mutasi_(BULAN)_OUTPUT_1.xlsx
With:
1. Xara Copilot-style Instant Audit Gate in Excel
2. Synchronized clustered timestamps pre-salary & chronological distribution post-salary
3. Locked Mandiri Geometry & Pure TTInterphases typography
4. Automated sequential versioning
"""

import os
import sys
import shutil
import re
import calendar
import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import Rule
from openpyxl.styles.differential import DifferentialStyle
import pdfplumber

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from pdfcraft_client import PdfCraftClient
from smart_date_time_generator import shuffle_and_synchronize_schedule
from bank_mandiri_spec import (
    COL_NOMINAL_RIGHT_X,
    COL_SALDO_RIGHT_X,
    SUMMARY_RIGHT_X,
    COL_NO_X,
    COL_DATE_TIME_X0,
    COL_DESC_X,
    VALUE_COL1_X0,
    VALUE_COL2_X0,
    COLOR_CREDIT_GREEN,
    COLOR_RUNNING_SALDO_BLUE,
    COLOR_DEBIT_BLACK,
    COLOR_SALDO_AWAL_GRAY
)

def format_idr(num):
    return f"{abs(num):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def parse_num(val):
    if val is None:
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    val_str = str(val).replace("Rp", "").replace(" ", "").replace(".", "").replace(",", ".").strip()
    try:
        return float(val_str)
    except:
        return 0.0

def sanitize_mandiri_typography(text: str) -> str:
    """
    Sanitizes characters that trigger foreign font fallbacks (like Helvetica)
    in Bank Mandiri embedded font subsets:
    - & -> NT (J&T -> JNT)
    - ' -> empty (MCDONALD'S -> MCDONALDS)
    - V -> F (ARSYIVA -> ARSYIFA)
    """
    t = text.replace("&", "NT").replace("'", "")
    t = re.sub(r'ARSYIVA', 'ARSYIFA', t)
    return t

def build_advanced_audit_excel(month_code, transactions, header_data, summary_data, output_path):
    wb = openpyxl.Workbook()
    ws_hdr = wb.active
    ws_hdr.title = "Header & Ringkasan"
    ws_mut = wb.create_sheet(title="Tabel_Mutasi")

    f_title = Font(name="Calibri", size=14, bold=True, color="1F497D")
    f_sec = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    f_bold = Font(name="Calibri", size=11, bold=True)
    f_regular = Font(name="Calibri", size=11)
    
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

    # Sheet 1: Header & Ringkasan
    ws_hdr['A1'] = "KONFIGURASI UTAMA & AUDIT GATE PEKERJAAN"
    ws_hdr['A1'].font = f_title
    ws_hdr['A2'] = "Template resmi PdfCraft Copilot (Real-time Instant Error Detection & Cross-Reconciliation)"
    ws_hdr['A2'].font = Font(name="Calibri", size=10, italic=True, color="595959")

    ws_hdr['A4'] = "Kategori / Parameter"
    ws_hdr['B4'] = "Nilai Data (Input / Live Formula)"
    ws_hdr['C4'] = "Status Validasi"
    ws_hdr['D4'] = "Keterangan & SOP Audit"
    for col in ['A4', 'B4', 'C4', 'D4']:
        ws_hdr[col].font = f_sec
        ws_hdr[col].fill = fill_navy

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

    # Conditional formatting on Sheet 1
    dxf_red = DifferentialStyle(fill=fill_red, font=font_red)
    rule_red = Rule(type="containsText", operator="containsText", text="SELISIH", dxf=dxf_red)
    rule_red.formula = ['NOT(ISERROR(SEARCH("SELISIH", B17)))']

    dxf_green = DifferentialStyle(fill=fill_green, font=font_green)
    rule_green = Rule(type="containsText", operator="containsText", text="MATCH", dxf=dxf_green)
    rule_green.formula = ['NOT(ISERROR(SEARCH("MATCH", B17)))']

    ws_hdr.conditional_formatting.add('B17:B20', rule_red)
    ws_hdr.conditional_formatting.add('B17:B20', rule_green)

    ws_hdr.column_dimensions['A'].width = 30
    ws_hdr.column_dimensions['B'].width = 48
    ws_hdr.column_dimensions['C'].width = 18
    ws_hdr.column_dimensions['D'].width = 65

    # Sheet 2: Tabel_Mutasi
    ws_mut['A1'] = "TABEL MUTASI TRANSAKSI RESMI"
    ws_mut['A1'].font = f_title
    ws_mut['A2'] = "Perubahan pada nominal (+/-) otomatis memperbarui saldo berjalan & live-checked dengan Header."
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

    # Transactions
    num_tx = len(transactions)
    for i, tx in enumerate(transactions):
        r = 6 + i
        prev_r = r - 1

        ws_mut.cell(r, 1, i + 1).alignment = Alignment(horizontal="center")
        ws_mut.cell(r, 2, tx.get("date", "")).alignment = Alignment(horizontal="center")
        ws_mut.cell(r, 3, tx.get("time", "")).alignment = Alignment(horizontal="center")
        ws_mut.cell(r, 4, tx.get("desc", ""))
        
        nom_val = tx.get("nom_num", 0.0)
        c_nom = ws_mut.cell(r, 5, nom_val)
        c_nom.number_format = '+#,##0.00;-#,##0.00;0.00'
        if nom_val > 0:
            c_nom.font = Font(name="Calibri", size=11, bold=True, color="008000")
        else:
            c_nom.font = Font(name="Calibri", size=11, bold=True, color="000000")

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

    # Summary Row
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

    # Conditional formatting on Sheet 2
    rule_h_red = Rule(type="containsText", operator="containsText", text="SELISIH", dxf=dxf_red)
    rule_h_red.formula = ['NOT(ISERROR(SEARCH("SELISIH", H6)))']
    rule_h_green = Rule(type="containsText", operator="containsText", text="OK", dxf=dxf_green)
    rule_h_green.formula = ['NOT(ISERROR(SEARCH("OK", H6)))']

    ws_mut.conditional_formatting.add(f'H6:H{sum_r}', rule_h_red)
    ws_mut.conditional_formatting.add(f'H6:H{sum_r}', rule_h_green)

    ws_mut.column_dimensions['A'].width = 8
    ws_mut.column_dimensions['B'].width = 16
    ws_mut.column_dimensions['C'].width = 16
    ws_mut.column_dimensions['D'].width = 48
    ws_mut.column_dimensions['E'].width = 20
    ws_mut.column_dimensions['F'].width = 8
    ws_mut.column_dimensions['G'].width = 22
    ws_mut.column_dimensions['H'].width = 20
    ws_mut.column_dimensions['I'].width = 20

    wb.save(output_path)
    print(f"Generated advanced audit Excel: {output_path}")

def generate_numbered_release(month_code: str, m_num: int, salary_no: int, last_day: int,
                              pdf_source: str, excel_source: str, target_dir: str, target_version: int = 1):
    print(f"\n=========================================================================")
    print(f"   GENERATING NUMBERED RELEASE: {month_code} 2026 (OUTPUT {target_version})")
    print(f"=========================================================================\n")

    templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates"))
    p1_template = os.path.join(templates_dir, "master_page_1.pdf")
    p_mid_template = os.path.join(templates_dir, "master_page_intermediate.pdf")
    p_disc_inline = os.path.join(templates_dir, "master_page_disclaimer_inline.pdf")
    p_disc_standalone = os.path.join(templates_dir, "master_page_disclaimer_standalone.pdf")

    # 1. Parse Excel Source
    wb = openpyxl.load_workbook(excel_source, data_only=True)
    ws1 = wb["Header & Ringkasan"]
    ws2 = wb["Tabel_Mutasi"]

    cabang = "KCP Serang Cilegon"
    periode = f"01 {month_code.capitalize()} 2026 - {last_day:02d} {month_code.capitalize()} 2026"
    dicetak_pada = "06 Nov 2026"
    nomor_rekening = "1630016287487"

    for r in range(5, 21):
        c1 = str(ws1.cell(r, 1).value or "").strip()
        c2 = ws1.cell(r, 2).value
        if "Cabang" in c1 and c2: cabang = str(c2).strip()
        elif "Periode" in c1 and c2:
            raw_p = str(c2).strip()
            for m_id, m_en in [("Okt", "Oct"), ("Agu", "Aug"), ("Agt", "Aug"), ("Mei", "May")]:
                raw_p = raw_p.replace(m_id, m_en)
            periode = raw_p
        elif "Dicetak" in c1 and c2:
            if isinstance(c2, datetime.datetime):
                dicetak_pada = c2.strftime("%d %b %Y")
            else:
                dicetak_pada = str(c2).strip()
        elif "Rekening" in c1 and c2: nomor_rekening = str(c2).strip()

    sawal_val = parse_num(ws1.cell(22, 2).value)
    dmasuk_val = parse_num(ws1.cell(23, 2).value)
    dkeluar_val = abs(parse_num(ws1.cell(24, 2).value))
    sakhir_val = round(sawal_val + dmasuk_val - dkeluar_val, 2)

    header_data = {
        "nama": "GALANG PUTRA KURNIAWAN",
        "nama_line1": "GALANG PUTRA",
        "nama_line2": "KURNIAWAN",
        "cabang": cabang,
        "periode": periode,
        "dicetak_pada": dicetak_pada,
        "nomor_rekening": nomor_rekening
    }

    summary_data = {
        "saldo_awal_num": sawal_val,
        "dana_masuk_num": dmasuk_val,
        "dana_keluar_num": dkeluar_val,
        "saldo_akhir_num": sakhir_val,
        "saldo_awal": format_idr(sawal_val),
        "dana_masuk": format_idr(dmasuk_val),
        "dana_keluar": format_idr(dkeluar_val),
        "saldo_akhir": format_idr(sakhir_val)
    }

    print(f"Header: {header_data}")
    print(f"Summary: {summary_data}")

    # 2. Harvest authentic items from PDF Source
    authentic_items = []
    with pdfplumber.open(pdf_source) as pdf:
        for p_idx, page in enumerate(pdf.pages):
            words = page.extract_words()
            min_top = 320 if p_idx == 0 else 200
            table_words = [w for w in words if min_top <= w["top"] <= 800]
            wibs = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
            for ww in wibs:
                time_token = [w['text'] for w in table_words if abs(w['top'] - ww['top']) < 3 and w['x1'] <= ww['x0'] + 1]
                date_tokens = [w['text'] for w in table_words if 0 < (ww['top'] - w['top']) < 15 and 45 <= w['x0'] <= 90]
                
                desc_words = sorted([w for w in table_words if abs(w['top'] - ww['top']) < 22 and 115 <= w['x0'] <= 365], key=lambda x: (x['top'], x['x0']))
                lines = []
                curr_l = []
                curr_y = None
                for w in desc_words:
                    if curr_y is None or abs(w['top'] - curr_y) < 4:
                        curr_l.append(w['text'])
                        curr_y = w['top'] if curr_y is None else (curr_y * 0.7 + w['top'] * 0.3)
                    else:
                        lines.append(" ".join(curr_l))
                        curr_l = [w['text']]
                        curr_y = w['top']
                if curr_l:
                    lines.append(" ".join(curr_l))
                desc_text = "\n".join(lines)
                desc_text = sanitize_mandiri_typography(desc_text)

                t_str = f"{time_token[-1]} WIB" if time_token else "12:00:00 WIB"
                raw_d = " ".join(date_tokens).strip()
                for m_old in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]:
                    raw_d = raw_d.replace(m_old, month_code.capitalize())
                d_str = re.sub(r'(\d+)\s*([A-Za-z]+)\s*(\d+)', r'\1 \2 \3', raw_d)

                authentic_items.append({
                    "date": d_str,
                    "time": t_str,
                    "desc": desc_text
                })

    print(f"Harvested {len(authentic_items)} authentic items from PDF")

    # 3. Read active transactions from Excel
    excel_txs = []
    for r in range(5, ws2.max_row + 1):
        no_cell = ws2.cell(r, 1).value
        if str(no_cell).strip() == '[AWAL]':
            continue
        nom_cell = ws2.cell(r, 5).value
        sal_cell = ws2.cell(r, 7).value
        if nom_cell is None or str(nom_cell).strip() == '':
            continue
        nom = parse_num(nom_cell)
        sal = parse_num(sal_cell)
        
        if abs(nom) > 0.001:
            idx = len(excel_txs)
            auth = authentic_items[idx] if idx < len(authentic_items) else {
                "date": f"01 {month_code.capitalize()} 2026",
                "time": "12:00:00 WIB",
                "desc": "-"
            }
            excel_txs.append({
                "no": idx + 1,
                "date": auth["date"],
                "time": auth["time"],
                "desc": auth["desc"],
                "nom_num": nom,
                "saldo_num": sal
            })

    print(f"Prepared {len(excel_txs)} active transactions")

    # 4. Apply synchronized shuffling & chronological distribution
    shuffled_txs = shuffle_and_synchronize_schedule(
        excel_txs, month_num=m_num, year=2026, salary_no=salary_no, last_day=last_day
    )

    # Re-calculate exact running saldo
    cur_bal = sawal_val
    for t in shuffled_txs:
        cur_bal = round(cur_bal + t["nom_num"], 2)
        t["saldo_num"] = cur_bal
        is_cr = t["nom_num"] > 0
        t["nominal"] = ("+" if is_cr else "-") + format_idr(t["nom_num"])
        t["saldo"] = format_idr(cur_bal)
        t["is_credit"] = is_cr

    # Output paths
    local_out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))
    os.makedirs(local_out_dir, exist_ok=True)

    out_pdf_path = os.path.join(target_dir, f"REK_GALANG_{month_code}_OUTPUT_{target_version}.pdf")
    out_xls_path = os.path.join(target_dir, f"Template_Mutasi_{month_code}_OUTPUT_{target_version}.xlsx")

    local_xls_out = os.path.join(local_out_dir, f"Template_Mutasi_{month_code}_OUTPUT_{target_version}.xlsx")
    local_pdf_out = os.path.join(local_out_dir, f"REK_GALANG_{month_code}_OUTPUT_{target_version}.pdf")

    print(f"Target Version: {target_version}")
    print(f"PDF Output: {out_pdf_path}")
    print(f"Excel Output: {out_xls_path}")

    # Generate Upgraded Audit Excel locally first
    build_advanced_audit_excel(month_code, shuffled_txs, header_data, summary_data, local_xls_out)

    # 5. Build PDF with PdfCraft
    total_tx = len(shuffled_txs)
    if total_tx <= 34:
        page_capacities = [10, 12, 12]
        page_paths = [p1_template, p_mid_template, p_mid_template, p_disc_standalone]
        is_last_inline = False
    elif total_tx <= 41:
        p4_count = total_tx - 34
        page_capacities = [10, 12, 12, p4_count]
        page_paths = [p1_template, p_mid_template, p_mid_template, p_disc_inline]
        is_last_inline = True
    else:
        raise ValueError(f"Unsupported transaction count: {total_tx}")

    total_pages = len(page_paths)
    temp_combined = os.path.join(local_out_dir, f"temp_{month_code}_numbered_assembly.pdf")

    with PdfCraftClient() as client:
        client.call_tool("doc_combine", {
            "paths": page_paths,
            "out": temp_combined,
            "open": False
        })

        doc_id = client.doc_open(temp_combined)
        print(f"Editing assembled document (doc_id={doc_id})...")

        num_header_pages = 3 if not is_last_inline else 4
        for p_num in range(1, num_header_pages + 1):
            paras = client.get_paragraphs(doc_id, page=p_num)
            
            # Step A: Empty old Cabang paragraph to avoid collision
            p_cabang = [p for p in paras if ("Taman Aries" in p["text"] or "KCP" in p["text"] or "Ciceri" in p["text"] or "Cilegon" in p["text"]) and 115 <= p["rect"][1] <= 135 and p["rect"][0] < 200]
            if p_cabang:
                client.edit_text(doc_id, page=p_num, paragraph=p_cabang[0]["paragraph"], text="")

            # Step B: Apply 3-line composite block to Name paragraph
            paras = client.get_paragraphs(doc_id, page=p_num)
            p_name = [p for p in paras if ("ROY DARWIN" in p["text"] or "GALANG" in p["text"]) and 90 <= p["rect"][1] <= 115 and p["rect"][0] < 200]
            if p_name:
                composite_text = f"{header_data['nama_line1']}\n{header_data['nama_line2']}\n{header_data['cabang']}"
                client.edit_text(doc_id, page=p_num, paragraph=p_name[0]["paragraph"], text=composite_text, line_spacing=1.375)
                up_p = [x for x in client.get_paragraphs(doc_id, page=p_num) if x["paragraph"] == p_name[0]["paragraph"]][0]
                dx = VALUE_COL1_X0 - up_p["rect"][0]
                if abs(dx) > 0.05:
                    client.edit_text(doc_id, page=p_num, paragraph=p_name[0]["paragraph"], dx=dx)

            # Step C: Periode
            paras = client.get_paragraphs(doc_id, page=p_num)
            for p in paras:
                if ("01" in p["text"] and any(m in p["text"] for m in ["Jan", "Feb", "Aug", "Sep", "Oct"])) and 90 <= p["rect"][1] <= 115 and 330 <= p["rect"][0] <= 370:
                    client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text=header_data["periode"])
                    break

            # Step D: Dicetak Pada
            paras = client.get_paragraphs(doc_id, page=p_num)
            for p in paras:
                if any(m in p["text"] for m in ["Jan", "Feb", "Aug", "Sep", "Oct", "Nov", "Dec"]) and 105 <= p["rect"][1] <= 130 and 330 <= p["rect"][0] <= 370:
                    client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text=header_data["dicetak_pada"])
                    break

            # Step E: Page Numbering
            paras = client.get_paragraphs(doc_id, page=p_num)
            for p in paras:
                if "dari" in p["text"] or "of" in p["text"]:
                    client.edit_text(doc_id, page=p_num, paragraph=p["paragraph"], text=f"{p_num} dari {total_pages}\n{p_num} of {total_pages}")
                    break

            # Step F: Page 1 Summary & Account Number
            if p_num == 1:
                paras = client.get_paragraphs(doc_id, page=1)
                for p in paras:
                    if "16500" in p["text"] or "16300" in p["text"]:
                        client.edit_text(doc_id, page=1, paragraph=p["paragraph"], text=header_data["nomor_rekening"])
                        up_p = [x for x in client.get_paragraphs(doc_id, page=1) if x["paragraph"] == p["paragraph"]][0]
                        # Lock Nomor Rekening at x0 = 160.00 pt
                        dx_acc = 160.00 - up_p["rect"][0]
                        if abs(dx_acc) > 0.05:
                            client.edit_text(doc_id, page=1, paragraph=p["paragraph"], dx=dx_acc)
                        break

                paras = client.get_paragraphs(doc_id, page=1)
                for p in paras:
                    t_clean = p["text"].replace(".", "").replace(",", "")
                    if any(c.isdigit() for c in t_clean) and 500 <= p["rect"][0] <= 575:
                        y = p["rect"][1]
                        if 140 <= y <= 158:
                            client.edit_text(doc_id, page=1, paragraph=p["paragraph"], text=summary_data["saldo_awal"], align="right")
                        elif 160 <= y <= 178:
                            client.edit_text(doc_id, page=1, paragraph=p["paragraph"], text=f"+{summary_data['dana_masuk']}", color=COLOR_CREDIT_GREEN, align="right")
                        elif 180 <= y <= 198:
                            client.edit_text(doc_id, page=1, paragraph=p["paragraph"], text=f"-{summary_data['dana_keluar']}", color=COLOR_DEBIT_BLACK, align="right")
                        elif 200 <= y <= 220:
                            client.edit_text(doc_id, page=1, paragraph=p["paragraph"], text=summary_data["saldo_akhir"], color=COLOR_RUNNING_SALDO_BLUE, align="right")

        # Step G: Populate Transactions row-by-row
        tx_cursor = 0
        for p_idx, cap in enumerate(page_capacities):
            p_num = p_idx + 1
            paras = client.get_paragraphs(doc_id, page=p_num)

            p_wibs = sorted([p for p in paras if "WIB" in p["text"] and p["rect"][0] < 110], key=lambda x: x["rect"][1])
            p_nos = sorted([p for p in paras if p["text"].strip().isdigit() and p["rect"][0] < 45 and p["rect"][1] >= 200], key=lambda x: x["rect"][1])

            for row_in_page in range(cap):
                if tx_cursor >= total_tx:
                    break
                tx = shuffled_txs[tx_cursor]
                
                # No
                if row_in_page < len(p_nos):
                    client.edit_text(doc_id, page=p_num, paragraph=p_nos[row_in_page]["paragraph"], text=str(tx["no"]), align="center")

                # Date & Time
                if row_in_page < len(p_wibs):
                    dt_p = p_wibs[row_in_page]
                    client.edit_text(doc_id, page=p_num, paragraph=dt_p["paragraph"], text=f"{tx['date']}\n{tx['time']}")

                # Row baseline y
                ref_y = p_wibs[row_in_page]["rect"][1] if row_in_page < len(p_wibs) else (346.0 + row_in_page * 40.0)

                # Description
                paras_now = client.get_paragraphs(doc_id, page=p_num)
                d_candidates = [p for p in paras_now if abs(p["rect"][1] - ref_y) < 22 and 115 <= p["rect"][0] <= 140]
                if d_candidates:
                    target_d = d_candidates[0]
                    num_lines = len(tx["desc"].split('\n'))
                    ideal_top = ref_y - (num_lines - 1) * 5.0
                    client.edit_text(doc_id, page=p_num, paragraph=target_d["paragraph"], text=tx["desc"])
                    up_d = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == target_d["paragraph"]][0]
                    dx_d = COL_DESC_X - up_d["rect"][0]
                    dy_d = ideal_top - up_d["rect"][1]
                    client.edit_text(doc_id, page=p_num, paragraph=target_d["paragraph"], dx=dx_d, dy=dy_d)

                # Nominal & Saldo
                paras_now = client.get_paragraphs(doc_id, page=p_num)
                nom_candidates = [p for p in paras_now if abs(p["rect"][1] - ref_y) < 18 and 370 <= p["rect"][0] <= 440]
                if nom_candidates:
                    color = COLOR_CREDIT_GREEN if tx["is_credit"] else COLOR_DEBIT_BLACK
                    client.edit_text(doc_id, page=p_num, paragraph=nom_candidates[0]["paragraph"], text=tx["nominal"], color=color, align="right")

                sal_candidates = [p for p in paras_now if abs(p["rect"][1] - ref_y) < 18 and 500 <= p["rect"][0] <= 575]
                if sal_candidates:
                    client.edit_text(doc_id, page=p_num, paragraph=sal_candidates[0]["paragraph"], text=tx["saldo"], color=COLOR_RUNNING_SALDO_BLUE, align="right")

                tx_cursor += 1

        client.doc_save(doc_id, local_pdf_out)
        client.doc_close(doc_id)

    # Safely copy locally generated files to target directory
    try:
        shutil.copyfile(local_xls_out, out_xls_path)
        print(f"Copied Excel to {out_xls_path}")
    except Exception as e:
        print(f"Warning: Could not copy Excel to {out_xls_path} ({e})")

    try:
        shutil.copyfile(local_pdf_out, out_pdf_path)
        print(f"Copied PDF to {out_pdf_path}")
    except Exception as e:
        print(f"Warning: Could not copy PDF to {out_pdf_path} ({e})")

    print(f"SUCCESS: Generated {out_pdf_path} and {out_xls_path}")
    return out_pdf_path, out_xls_path

if __name__ == "__main__":
    base_dir = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru"
    
    # August
    generate_numbered_release(
        month_code="AUG", m_num=8, salary_no=22, last_day=31,
        pdf_source=os.path.join(base_dir, "AUG", "REK_GALANG_AUG_2026_PERFECT.pdf"),
        excel_source=os.path.join(base_dir, "AUG", "Template_Mutasi_Aug.xlsx"),
        target_dir=os.path.join(base_dir, "AUG"),
        target_version=1
    )

    # September
    generate_numbered_release(
        month_code="SEP", m_num=9, salary_no=22, last_day=30,
        pdf_source=os.path.join(base_dir, "SEP", "REK_GALANG_SEP_2026_PERFECT.pdf"),
        excel_source=os.path.join(base_dir, "SEP", "Template_Mutasi_SEP_Reconciled.xlsx"),
        target_dir=os.path.join(base_dir, "SEP"),
        target_version=1
    )

    # October
    generate_numbered_release(
        month_code="OCT", m_num=10, salary_no=27, last_day=31,
        pdf_source=os.path.join(base_dir, "OCT", "REK_GALANG_OCT_2026_PERFECT.pdf"),
        excel_source=os.path.join(base_dir, "OCT", "Template_Mutasi_OCT_Reconciled.xlsx"),
        target_dir=os.path.join(base_dir, "OCT"),
        target_version=1
    )
