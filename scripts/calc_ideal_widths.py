import sys
import os
import pdfplumber

# Let's inspect the exact line widths from 2.pdf chars or measure using a test script
test_pdf = "output/test_no_width.pdf"

with pdfplumber.open(test_pdf) as pdf:
    # Build a char width map from TTInterphases
    char_widths = {}
    for p in pdf.pages:
        for c in p.chars:
            if c.get("size") == 8.0:
                char_widths[c["text"]] = c["width"]

print(f"Mapped {len(char_widths)} character widths for size=8.0")
# Add fallback space if needed
if " " not in char_widths: char_widths[" "] = 2.2

def get_text_width(text):
    return sum(char_widths.get(ch, 4.5) for ch in text)

descs = [
    # Page 1
    "Biaya transaksi bank\nPembayaran Danatopup\n89508089622130569",
    "Pembayaran Danatopup\n89508089622130569",
    "Pembayaran QR\nke SOTO AYAM LAMONGAN CAK JO\n601483798729",
    "Penarikan tunai tanpa kartu\nDi ATM SRG AM PURI ANGREK 0\n089622130569",
    "Biaya transfer BI Fast",
    "Transfer BI Fast\nKe BCA\nBUDI SAPUTRA TANAGUN 1010570065",
    "Transfer ke BANK MANDIRI\nMEI DWI LESTARI 1370011851231",
    "Biaya transaksi bank\nPembayaran Danatopup\n89508087858621135",
    "Pembayaran Danatopup\n89508087858621135",
    "Transfer BI Fast\nDari BANK BNI\nFITRIANA PURWANINGSI 0314467254",
    # Page 2
    "Pembayaran QR\nke MAKO CAKE BAKERY SE 603\n601129029297",
    "Pembayaran QR\nke RESERVE SA SERANG 1 1324\n601120346341",
    "Biaya transaksi bank\nPembayaran Danatopup\n89508089622130569",
    "Pembayaran Danatopup\n89508089622130569",
    "Transfer dari BANK MANDIRI\nNANDA FEBRIANTI 1370013797036",
    "Biaya transaksi bank\nPembayaran Danatopup\n89508089622130569",
    "Pembayaran Danatopup\n89508089622130569",
    "Pembayaran QR\nke PECEL LELE Mas Dikky, pas\n601580938038",
    "Pembayaran QR\nke Syarkawi\n601581102500",
    "Biaya transaksi bank\nPembayaran Danatopup\n89508083175718201",
    "Pembayaran Danatopup\n89508083175718201",
    "Transfer BI Fast\nDari BCA\nPT BENDI NASHA NIAGA INDUSTRI 5411078192\n(CENAIDJA)",
    # Page 3
    "Pembayaran QR\nke TEMAN DENTAL AHMAD YAN 40\n601208674693",
    "Biaya transaksi bank\nPembayaran Danatopup\n89508089622130569",
    "Pembayaran Danatopup\n89508089622130569",
    "Penarikan tunai di ATM BANK\nMANDIRI SRG IM CIRUAS 01",
    "Penarikan tunai tanpa kartu\nDi ATM SRG MD CIRUAS 01\n089622130569",
    "Transfer BI Fast\nDari BANK BNI\nKARINA AMALIA DARMAW 1921323326",
    "Pembayaran QR ke\nwarung madura\n506115913713",
    "Penarikan tunai di ATM BANK\nMANDIRI SRG IM CIRUAS 01",
    "Transfer BI Fast\nDari BCA\nMULYATI 2452705525\n-",
    "Pembayaran QR\nke SPBU 3442109 KM 68 B 36\n601275499757",
    "Biaya transfer BI Fast\n-",
    "Transfer BI Fast\nKe BCA\nLUKMAN 1011284251",
    # Page 4
    "Transfer BI Fast\nDari BCA\nFERNANDUS NAINGGOLAN 8690976766\n-",
    "Penarikan tunai di ATM\nBANK MANDIRI SRG IM PAKUPATAN 01",
    "Biaya administrasi rekening"
]

for i, d in enumerate(descs, 1):
    lines = d.split("\n")
    widths = [get_text_width(l) for l in lines]
    max_w = max(widths)
    # ideal width is max_w + 5.0 pt margin
    ideal_w = round(max_w + 5.0, 1)
    print(f"Tx {i:02d} ({len(lines)} lines) | max_w={max_w:5.1f} | ideal_w={ideal_w:5.1f} | lines: {[round(w, 1) for w in widths]}")
