import pdfplumber

with pdfplumber.open('templates/master_page_1.pdf') as pdf:
    chars1 = set(c['text'] for c in pdf.pages[0].chars)
with pdfplumber.open('templates/master_page_intermediate.pdf') as pdf:
    chars_mid = set(c['text'] for c in pdf.pages[0].chars)

all_master_chars = chars1.union(chars_mid)

test_texts = [
    "Pembayaran QR ke JNT TANGERANG 601431482019",
    "Transfer BI Fast\nKe BCA\nMARWA ARSYIFA 2452913675",
    "Pembayaran QR\nke MCDONALDS SOK 21401\n601476229228",
    "Pembayaran QR\nke MCDONALDS SOK 21401\n601476371363"
]

for t in test_texts:
    missing = [c for c in t if c not in all_master_chars and c != '\n']
    print(f"Missing in {repr(t[:30])}: {missing}")
