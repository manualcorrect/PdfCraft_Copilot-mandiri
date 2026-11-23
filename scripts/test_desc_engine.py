import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

from src.description_layout_engine import DescriptionLayoutEngine

tests = [
    "Pembayaran Danatopup\n89508089528734111",
    "Pembayaran QR\nke Kantin Ka Rin\n507016923183",
    "Transfer dari BANK MANDIRI\nSIGIT BUDHI ARYONO 1550009926679",
    "Penarikan tunai di ATM\nBANK MANDIRI SRG IM CIRUAS 01",
    "Pembayaran QR\nke kantin wak kaji\n507028275939",
    "Pembayaran QR\nke Talon Kelidan\n507024268342",
    "Transfer dari BANK MANDIRI\nSIGIT BUDHI ARYONO 1550009926679",
    "Pembayaran QR\nke kantin wak kaji\n507029124072",
    "Transfer dari BANK MANDIRI\nSIGIT BUDHI ARYONO 1550009926679",
    "Penarikan tunai di ATM\nBANK MANDIRI SRG IM CIRUAS 01",
    # An unformatted raw text test
    "Transfer BI Fast Dari BCA PT BENDI NASHA NIAGA INDUSTRI 5411078192 (CENAIDJA)",
    "Pembayaran QR ke Shopee Express 605017752194",
    "Biaya administrasi rekening"
]

print("=== Testing DescriptionLayoutEngine ===")
for t in tests:
    formatted = DescriptionLayoutEngine.format_description(t)
    lines = formatted.split("\n")
    print(f"\nRaw: {repr(t)}")
    print(f"Lines ({len(lines)}):")
    for l in lines:
        print(f"  -> {repr(l)} (len={len(l)})")
