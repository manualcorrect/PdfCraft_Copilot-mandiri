import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"output/REK_GALANG_JUL_2026_STANDARDIZED.pdf"

print(f"=== AUDITING STANDARDIZED: {pdf_path} ===")

with pdfplumber.open(pdf_path) as pdf:
    for p_idx, page in enumerate(pdf.pages):
        p_num = p_idx + 1
        print(f"\n--- PAGE {p_num} ---")
        words = page.extract_words()
        
        # Check header
        print("[Header Text Positions]")
        for w in words:
            if w["top"] < 140:
                if any(k in w["text"] for k in ["GALANG", "Ciruas", "16300", "dari", "of", "Jul", "Dicetak", "e-Statement"]):
                    print(f"  {w['text']:22s} | x0={w['x0']:6.2f}, x1={w['x1']:6.2f}, top={w['top']:6.2f}")
        
        # Check summary box
        if p_num == 1:
            print("\n[Summary Box Values]")
            for w in words:
                if 160 <= w["top"] <= 255 and w["x0"] > 480:
                    print(f"  {w['text']:22s} | x0={w['x0']:6.2f}, x1={w['x1']:6.2f}, top={w['top']:6.2f}")

        # Check transaction table
        print(f"\n[Table Elements Sample]")
        min_y = 320 if p_num == 1 else 200
        for w in words:
            if min_y <= w["top"] <= 800:
                if w["text"] in ["1", "2", "3", "10", "11", "22"]:
                    print(f"  No:      {w['text']:18s} | x0={w['x0']:6.2f}, x1={w['x1']:6.2f}, top={w['top']:6.2f}")
                elif any(m in w["text"] for m in ["Jul", "WIB"]):
                    print(f"  Date/Tm: {w['text']:18s} | x0={w['x0']:6.2f}, x1={w['x1']:6.2f}, top={w['top']:6.2f}")
                elif (w["text"].startswith("+") or w["text"].startswith("-") or w["text"] == "300.000,00") and 350 <= w["x0"] <= 450:
                    print(f"  Nominal: {w['text']:18s} | x0={w['x0']:6.2f}, x1={w['x1']:6.2f}, top={w['top']:6.2f}")
                elif 500 <= w["x0"] <= 585 and ("," in w["text"]):
                    print(f"  Saldo:   {w['text']:18s} | x0={w['x0']:6.2f}, x1={w['x1']:6.2f}, top={w['top']:6.2f}")
