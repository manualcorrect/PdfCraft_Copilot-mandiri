import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

docs = [
    (r"D:\X_Files\rekening\Reference\nasih 2024 new unlocked\ilovepdf_unlocked\e-Statement_XXXXXXXXX9210_01 Des 2024-31 Des 2024_unlocked.pdf", "1. Nasih Des 2024"),
    (r"D:\X_Files\rekening\Reference\Roy\ilovepdf_unlocked\Agu 2026_unlocked.pdf", "2. Roy Agu 2026"),
    (r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\REK GALANG JUL 2026.pdf", "3. Galang Jul Original"),
    (r"C:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\REK_GALANG_JUL_2026_STANDARDIZED.pdf", "4. Galang Jul Standardized")
]

for path, name in docs:
    print(f"\n=======================================================")
    print(f"   {name}")
    print(f"=======================================================")
    with pdfplumber.open(path) as pdf:
        p1 = pdf.pages[0]
        words = p1.extract_words()
        
        # 1. Bank Address top right
        addr = [w for w in words if 45 <= w["top"] <= 75 and w["x0"] > 280]
        addr_line = " ".join(w["text"] for w in sorted(addr, key=lambda x: x["x0"]))
        if addr:
            print(f"[Bank Address] x0={addr[0]['x0']:.2f}, x1={addr[-1]['x1']:.2f} | {addr_line}")

        # 2. Customer Name & Branch
        name_words = [w for w in words if 95 <= w["top"] <= 112 and 110 <= w["x0"] <= 240]
        if name_words:
            print(f"[Customer Name] x0={name_words[0]['x0']:.2f}, x1={name_words[-1]['x1']:.2f} | {' '.join(w['text'] for w in name_words)}")
        
        branch_words = [w for w in words if 118 <= w["top"] <= 135 and 110 <= w["x0"] <= 240]
        if branch_words:
            print(f"[Branch]        x0={branch_words[0]['x0']:.2f}, x1={branch_words[-1]['x1']:.2f} | {' '.join(w['text'] for w in branch_words)}")

        # 3. Periode & Dicetak Pada
        per_words = [w for w in words if 95 <= w["top"] <= 112 and 330 <= w["x0"] <= 460]
        if per_words:
            print(f"[Periode Value] x0={per_words[0]['x0']:.2f}, x1={per_words[-1]['x1']:.2f} | {' '.join(w['text'] for w in per_words)}")

        print_words = [w for w in words if 118 <= w["top"] <= 135 and 330 <= w["x0"] <= 460]
        if print_words:
            print(f"[Dicetak Value] x0={print_words[0]['x0']:.2f}, x1={print_words[-1]['x1']:.2f} | {' '.join(w['text'] for w in print_words)}")

        # 4. Page numbering top right
        pnum_words = [w for w in words if 95 <= w["top"] <= 125 and w["x0"] > 520]
        print(f"[Page Numbers]")
        for pw in pnum_words:
            print(f"   {pw['text']:12s} | x0={pw['x0']:.2f}, x1={pw['x1']:.2f}, top={pw['top']:.2f}")

        # 5. Financial Summary Box
        print(f"[Financial Summary Box]")
        sum_words = [w for w in words if 160 <= w["top"] <= 255 and w["x0"] > 480]
        for sw in sum_words:
            print(f"   {sw['text']:16s} | x0={sw['x0']:.2f}, x1={sw['x1']:.2f}, top={sw['top']:.2f}")

        # 6. Table Header (top ~294..315)
        print(f"[Table Headers]")
        th_words = [w for w in words if 290 <= w["top"] <= 318]
        for th in sorted(th_words, key=lambda x: x["x0"]):
            print(f"   {th['text']:20s} | x0={th['x0']:.2f}, x1={th['x1']:.2f}, top={th['top']:.2f}")

        # 7. First 3 Transaction Rows
        print(f"[First 3 Rows Data]")
        t_words = [w for w in words if 320 <= w["top"] <= 460]
        for tw in sorted(t_words, key=lambda x: (round(x['top']/10)*10, x['x0'])):
            if tw["x0"] < 80 or tw["x0"] > 350:
                print(f"   {tw['text']:16s} | x0={tw['x0']:.2f}, x1={tw['x1']:.2f}, top={tw['top']:.2f}")
