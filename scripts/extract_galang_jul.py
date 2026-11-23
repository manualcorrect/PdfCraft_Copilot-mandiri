import os
import sys
import openpyxl

header_info = {
    "nama": "GALANG PUTRA KURNIAWAN",
    "periode": "01 Jul 2026 - 31 Jul 2026",
    "dicetak_pada": "19 Oct 2026",
    "nomor_rekening": "1630016287487",
    "cabang": "KCP Serang Ciruas"
}

summary_info = {
    "saldo_awal": 854955.00,
    "dana_masuk": 9111000.00,
    "dana_keluar": 4680607.00,
    "saldo_akhir": 5285348.00
}

# The 22 transactions extracted from REK GALANG JUL 2026.pdf
transactions = [
    # Page 1 (Rows 1..10)
    {"no": 1, "tanggal": "01 Jul 2026", "jam": "19:14:50 WIB", "uraian": "Pembayaran Danatopup\n89508089528734111", "nominal": -500000.00, "tipe": "DB", "saldo": 354955.00},
    {"no": 2, "tanggal": "02 Jul 2026", "jam": "15:52:31 WIB", "uraian": "Pembayaran QR\nke Kantin Ka Rin\n507016923183", "nominal": -4000.00, "tipe": "DB", "saldo": 350955.00},
    {"no": 3, "tanggal": "04 Jul 2026", "jam": "17:26:45 WIB", "uraian": "Transfer dari BANK MANDIRI\nSIGIT BUDHI ARYONO 1550009926679", "nominal": 300000.00, "tipe": "CR", "saldo": 650955.00},
    {"no": 4, "tanggal": "05 Jul 2026", "jam": "09:24:30 WIB", "uraian": "Penarikan tunai di ATM\nBANK MANDIRI SRG IM CIRUAS 01", "nominal": -500000.00, "tipe": "DB", "saldo": 150955.00},
    {"no": 5, "tanggal": "07 Jul 2026", "jam": "19:55:03 WIB", "uraian": "Pembayaran QR\nke kantin wak kaji\n507028275939", "nominal": -30000.00, "tipe": "DB", "saldo": 120955.00},
    {"no": 6, "tanggal": "08 Jul 2026", "jam": "11:36:32 WIB", "uraian": "Pembayaran QR\nke Talon Kelidan\n507024268342", "nominal": -90000.00, "tipe": "DB", "saldo": 30955.00},
    {"no": 7, "tanggal": "09 Jul 2026", "jam": "18:52:08 WIB", "uraian": "Transfer dari BANK MANDIRI\nSIGIT BUDHI ARYONO 1550009926679", "nominal": 642000.00, "tipe": "CR", "saldo": 672955.00},
    {"no": 8, "tanggal": "11 Jul 2026", "jam": "21:08:58 WIB", "uraian": "Pembayaran QR\nke kantin wak kaji\n507029124072", "nominal": -30000.00, "tipe": "DB", "saldo": 642955.00},
    {"no": 9, "tanggal": "12 Jul 2026", "jam": "10:30:38 WIB", "uraian": "Transfer dari BANK MANDIRI\nSIGIT BUDHI ARYONO 1550009926679", "nominal": 500000.00, "tipe": "CR", "saldo": 1142955.00},
    {"no": 10, "tanggal": "14 Jul 2026", "jam": "09:31:37 WIB", "uraian": "Penarikan tunai di ATM\nBANK MANDIRI SRG IM CIRUAS 01", "nominal": -200000.00, "tipe": "DB", "saldo": 942955.00},
    # Page 2 (Rows 11..22)
    {"no": 11, "tanggal": "15 Jul 2026", "jam": "11:12:14 WIB", "uraian": "Pembayaran Danatopup\n89508089528734111", "nominal": -100000.00, "tipe": "DB", "saldo": 842955.00},
    {"no": 12, "tanggal": "17 Jul 2026", "jam": "22:02:40 WIB", "uraian": "Pembayaran Danatopup\n89508089528734111", "nominal": -501500.00, "tipe": "DB", "saldo": 341455.00},
    {"no": 13, "tanggal": "18 Jul 2026", "jam": "21:02:34 WIB", "uraian": "Transfer dari BANK MANDIRI\nNICHO ARYAANSYAH WIJ 1050021206325", "nominal": 519000.00, "tipe": "CR", "saldo": 860455.00},
    {"no": 14, "tanggal": "19 Jul 2026", "jam": "17:03:26 WIB", "uraian": "Pembayaran Danatopup\n89508089528734111", "nominal": -400000.00, "tipe": "DB", "saldo": 460455.00},
    {"no": 15, "tanggal": "21 Jul 2026", "jam": "07:41:08 WIB", "uraian": "Transfer dari BANK MANDIRI\nSIGIT BUDHI ARYONO 1550009926679", "nominal": 500000.00, "tipe": "CR", "saldo": 960455.00},
    {"no": 16, "tanggal": "22 Jul 2026", "jam": "12:13:50 WIB", "uraian": "Pembayaran QR\nke SPBU31.11403 DAAN MOGOT\n507442551414", "nominal": -378107.00, "tipe": "DB", "saldo": 582348.00},
    {"no": 17, "tanggal": "24 Jul 2026", "jam": "12:15:09 WIB", "uraian": "Penarikan tunai di ATM\nBANK MANDIRI SRG IM CIRUAS 01", "nominal": -200000.00, "tipe": "DB", "saldo": 382348.00},
    {"no": 18, "tanggal": "25 Jul 2026", "jam": "08:15:20 WIB", "uraian": "Transfer BI Fast Dari BCA\nPT BENDI NASHA NIAGA INDUSTRI 5411078192\n(CENAIDJA)", "nominal": 6650000.00, "tipe": "CR", "saldo": 7032348.00},
    {"no": 19, "tanggal": "27 Jul 2026", "jam": "08:45:20 WIB", "uraian": "Pembayaran Danatopup\n89508089528734111", "nominal": -92000.00, "tipe": "DB", "saldo": 6940348.00},
    {"no": 20, "tanggal": "28 Jul 2026", "jam": "15:52:03 WIB", "uraian": "Penarikan tunai di ATM\nBANK MANDIRI SRG IM CIRUAS 01", "nominal": -1250000.00, "tipe": "DB", "saldo": 5690348.00},
    {"no": 21, "tanggal": "29 Jul 2026", "jam": "13:46:19 WIB", "uraian": "Pembayaran QR\nke Kantin Ka Rin\n507044523123", "nominal": -400000.00, "tipe": "DB", "saldo": 5290348.00},
    {"no": 22, "tanggal": "31 Jul 2026", "jam": "21:30:00 WIB", "uraian": "Biaya administrasi rekening", "nominal": -5000.00, "tipe": "DB", "saldo": 5285348.00}
]

template_src = r"C:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\templates\Template_Mutasi_Bank.xlsx"
out_excel = r"C:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\templates\Galang_Jul_2026.xlsx"

wb = openpyxl.load_workbook(template_src)

# Sheet 1: Header & Ringkasan
ws_header = wb["Header & Ringkasan"]
ws_header["B10"] = header_info["nama"]
ws_header["B11"] = header_info["periode"]
ws_header["B12"] = header_info["dicetak_pada"]
ws_header["B13"] = header_info["nomor_rekening"]
ws_header["B18"] = "Jul 2026"

ws_header["B21"] = summary_info["saldo_awal"]
ws_header["B22"] = summary_info["dana_masuk"]
ws_header["B23"] = summary_info["dana_keluar"]
ws_header["B24"] = summary_info["saldo_akhir"]

# Sheet 2: Tabel_Mutasi
ws_mutasi = wb["Tabel_Mutasi"]
for r in range(6, ws_mutasi.max_row + 1):
    for c in range(1, 15):
        ws_mutasi.cell(row=r, column=c).value = None

for i, tx in enumerate(transactions):
    row = 6 + i
    ws_mutasi.cell(row=row, column=1, value=tx["no"])
    ws_mutasi.cell(row=row, column=2, value=tx["tanggal"])
    ws_mutasi.cell(row=row, column=3, value=tx["jam"])
    ws_mutasi.cell(row=row, column=4, value=tx["uraian"])
    ws_mutasi.cell(row=row, column=5, value=tx["nominal"])
    ws_mutasi.cell(row=row, column=6, value=tx["tipe"])
    ws_mutasi.cell(row=row, column=7, value=tx["saldo"])

wb.save(out_excel)
print("Created Galang_Jul_2026.xlsx successfully.")
