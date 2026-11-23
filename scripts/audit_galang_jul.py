import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\REK GALANG JUL 2026.pdf"

print(f"=== AUDITING {pdf_path} ===")

with pdfplumber.open(pdf_path) as pdf:
    for p_idx, page in enumerate(pdf.pages):
        p_num = p_idx + 1
        print(f"\n--- PAGE {p_num} ---")
        
        # 1. Fonts
        fonts = set(c["fontname"] for c in page.chars)
        print(f"Fonts: {sorted(fonts)}")
        
        # 2. Extract words
        words = page.extract_words()
        
        # Page 1 Header and Summary
        if p_num == 1:
            print("\n[Page 1 Header Info]")
            for w in words:
                if w["top"] < 250:
                    if any(k in w["text"] for k in ["GALANG", "Ciruas", "16300", "dari", "of", "Jul 2026", "Sep", "Oct", "Dicetak"]):
                        print(f"  {w['text']:20s} | x0={w['x0']:.2f}, x1={w['x1']:.2f}, top={w['top']:.2f}")

            print("\n[Page 1 Financial Summary]")
            for w in words:
                if 160 <= w["top"] <= 255 and w["x0"] > 480:
                    print(f"  {w['text']:20s} | x0={w['x0']:.2f}, x1={w['x1']:.2f}, top={w['top']:.2f}")

        # Table rows
        min_y = 320 if p_num == 1 else 200
        print(f"\n[Page {p_num} Transactions (top > {min_y})]")
        table_words = [w for w in words if min_y <= w["top"] <= 800]
        for w in table_words:
            # Check nominals & saldos
            if (w["text"].startswith("+") or w["text"].startswith("-")) and 350 <= w["x0"] <= 450:
                print(f"  Nominal: {w['text']:15s} | x0={w['x0']:.2f}, x1={w['x1']:.2f}, top={w['top']:.2f}")
            elif 480 <= w["x0"] <= 585 and ("," in w["text"] or "." in w["text"]):
                print(f"  Saldo:   {w['text']:15s} | x0={w['x0']:.2f}, x1={w['x1']:.2f}, top={w['top']:.2f}")
            elif w["x0"] < 80 and ("WIB" in w["text"] or ":" in w["text"] or w["text"].isdigit()):
                print(f"  Date/Time/No: {w['text']:12s} | x0={w['x0']:.2f}, x1={w['x1']:.2f}, top={w['top']:.2f}")
