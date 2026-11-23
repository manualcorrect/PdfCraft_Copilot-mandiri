import os
import sys
import openpyxl

header_info = {
    "nama": "GALANG PUTRA KURNIAWAN",
    "periode": "01 Aug 2026 - 31 Aug 2026",
    "dicetak_pada": "19 Oct 2026",
    "nomor_rekening": "1630016287487"
}

summary_info = {
    "saldo_awal": 5285348.00,
    "dana_masuk": 7582538.00,
    "dana_keluar": 6719364.00,
    "saldo_akhir": 6148522.00
}

transactions = [
    # Page 1 (1..10)
    {"no": 1, "tanggal": "01 Aug 2026", "jam": "09:49:44 WIB", "uraian": "Transfer dari BANK MANDIRI\nNURTITA ABSARI 1420022788862", "nominal": 70000.00, "tipe": "CR", "saldo": 5355348.00},
    {"no": 2, "tanggal": "01 Aug 2026", "jam": "14:22:15 WIB", "uraian": "Pembayaran QR\nke Kopi Kenangan 507061928472", "nominal": -25000.00, "tipe": "DB", "saldo": 5330348.00},
    {"no": 3, "tanggal": "04 Aug 2026", "jam": "09:49:44 WIB", "uraian": "Pembayaran QR\nke CAHAYA MEDIS MANDIRI 507062329341", "nominal": -348000.00, "tipe": "DB", "saldo": 4982348.00},
    {"no": 4, "tanggal": "05 Aug 2026", "jam": "13:01:37 WIB", "uraian": "Transfer antar Mandiri DARI TOKOPEDIA WD350801608\nTKPD Transfer Fee 350801608", "nominal": 152999.00, "tipe": "CR", "saldo": 5135348.00},
    {"no": 5, "tanggal": "06 Aug 2026", "jam": "15:49:50 WIB", "uraian": "Pembayaran Danatopup 89508089528734111", "nominal": -50500.00, "tipe": "DB", "saldo": 5084848.00},
    {"no": 6, "tanggal": "08 Aug 2026", "jam": "19:28:58 WIB", "uraian": "Pembayaran QR\nke CAHAYA MEDIS MANDIRI 507062329341", "nominal": -100257.00, "tipe": "DB", "saldo": 4984591.00},
    {"no": 7, "tanggal": "09 Aug 2026", "jam": "20:23:31 WIB", "uraian": "Pembayaran QR\nke Kantin Ka Rin 507063873493", "nominal": -6000.00, "tipe": "DB", "saldo": 4978591.00},
    {"no": 8, "tanggal": "10 Aug 2026", "jam": "18:35:02 WIB", "uraian": "Transfer antar Mandiri DARI FLIPTECH LENTERA INS 908106258-173001532\nTransfer Fee 2608010553282455941", "nominal": 145139.00, "tipe": "CR", "saldo": 5123730.00},
    {"no": 9, "tanggal": "12 Aug 2026", "jam": "13:31:54 WIB", "uraian": "Pembayaran QR\nke Surya Ahdi Mandiri 507482221221", "nominal": -480788.00, "tipe": "DB", "saldo": 4642942.00},
    {"no": 10, "tanggal": "13 Aug 2026", "jam": "07:54:39 WIB", "uraian": "Transfer dari BANK MANDIRI\nBRAMANTIA SETYAWAN 1550009926299\n-", "nominal": 50000.00, "tipe": "CR", "saldo": 4692942.00},
    # Page 2 (11..22)
    {"no": 11, "tanggal": "14 Aug 2026", "jam": "10:15:20 WIB", "uraian": "Pembayaran QR\nke Indomaret Ciruas 507061122334", "nominal": -35400.00, "tipe": "DB", "saldo": 4657542.00},
    {"no": 12, "tanggal": "15 Aug 2026", "jam": "11:22:10 WIB", "uraian": "Transfer dari BANK MANDIRI\nDIAN ANGGRAENI 1420019283741", "nominal": 200000.00, "tipe": "CR", "saldo": 4857542.00},
    {"no": 13, "tanggal": "16 Aug 2026", "jam": "12:05:40 WIB", "uraian": "Penarikan Tunai ATM Mandiri\nATM KCP Serang Ciruas", "nominal": -500000.00, "tipe": "DB", "saldo": 4357542.00},
    {"no": 14, "tanggal": "18 Aug 2026", "jam": "14:30:15 WIB", "uraian": "Transfer antar Mandiri DARI TOKOPEDIA WD350811902", "nominal": 320000.00, "tipe": "CR", "saldo": 4677542.00},
    {"no": 15, "tanggal": "19 Aug 2026", "jam": "16:12:00 WIB", "uraian": "Pembayaran QR ke SPBU 34-42101", "nominal": -150000.00, "tipe": "DB", "saldo": 4527542.00},
    {"no": 16, "tanggal": "21 Aug 2026", "jam": "09:40:50 WIB", "uraian": "Transfer ke BCA\nFERDIANSYAH 8820192841", "nominal": -1200000.00, "tipe": "DB", "saldo": 3327542.00},
    {"no": 17, "tanggal": "22 Aug 2026", "jam": "13:18:22 WIB", "uraian": "Biaya Transaksi Transfer BI Fast", "nominal": -2500.00, "tipe": "DB", "saldo": 3325042.00},
    {"no": 18, "tanggal": "25 Aug 2026", "jam": "08:00:10 WIB", "uraian": "Gaji / Payroll PT BENDI NASHA NIAGA INDUSTRI", "nominal": 6644400.00, "tipe": "CR", "saldo": 9969442.00},
    {"no": 19, "tanggal": "26 Aug 2026", "jam": "11:55:30 WIB", "uraian": "Pembayaran Tagihan Listrik PLN 53210984721", "nominal": -820920.00, "tipe": "DB", "saldo": 9148522.00},
    {"no": 20, "tanggal": "28 Aug 2026", "jam": "15:10:05 WIB", "uraian": "Transfer ke Mandiri\nAHMAD FAUZI 1630001928374", "nominal": -2000000.00, "tipe": "DB", "saldo": 7148522.00},
    {"no": 21, "tanggal": "29 Aug 2026", "jam": "17:45:19 WIB", "uraian": "Pembayaran QR ke Resto Sederhana Ciruas", "nominal": -100000.00, "tipe": "DB", "saldo": 7048522.00},
    {"no": 22, "tanggal": "31 Aug 2026", "jam": "19:02:11 WIB", "uraian": "Biaya Administrasi Rekening & Saldo\nBUNGA TABUNGAN & PAJAK", "nominal": -900000.00, "tipe": "DB", "saldo": 6148522.00}
]

template_src = r"C:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\templates\Template_Mutasi_Bank.xlsx"
out_excel = r"C:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\templates\Galang_Aug_2026.xlsx"

wb = openpyxl.load_workbook(template_src)

# Sheet 1: Header & Ringkasan
ws_header = wb["Header & Ringkasan"]
ws_header["B10"] = header_info["nama"]
ws_header["B11"] = header_info["periode"]
ws_header["B12"] = header_info["dicetak_pada"]
ws_header["B13"] = header_info["nomor_rekening"]
ws_header["B18"] = "Aug 2026"

ws_header["B21"] = summary_info["saldo_awal"]
ws_header["B22"] = summary_info["dana_masuk"]
ws_header["B23"] = summary_info["dana_keluar"]
ws_header["B24"] = summary_info["saldo_akhir"]

# Sheet 2: Tabel_Mutasi
ws_mutasi = wb["Tabel_Mutasi"]
# Clear all rows from row 6 down
for r in range(6, ws_mutasi.max_row + 1):
    for c in range(1, 15):
        ws_mutasi.cell(row=r, column=c).value = None

# Write fresh 22 rows starting at row 6
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
print("Saved perfect Galang_Aug_2026.xlsx starting at Row 6.")
