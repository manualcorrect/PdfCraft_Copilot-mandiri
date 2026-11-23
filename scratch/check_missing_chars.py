import pdfplumber

test_str = "Pembayaran QR ke JNT TANGERANG 601431482019"
with pdfplumber.open('templates/master_page_1.pdf') as pdf:
    chars = set(c['text'] for c in pdf.pages[0].chars)
    missing = [c for c in test_str if c not in chars]
    print("Missing chars for JNT:", missing)
