import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

nasih_path = r"D:\X_Files\rekening\Reference\nasih 2024 new unlocked\ilovepdf_unlocked\e-Statement_XXXXXXXXX9210_01 Des 2024-31 Des 2024_unlocked.pdf"
roy_path = r"D:\X_Files\rekening\Reference\Roy\ilovepdf_unlocked\Agu 2026_unlocked.pdf"

with pdfplumber.open(nasih_path) as pdf_n, pdfplumber.open(roy_path) as pdf_r:
    words_n = pdf_n.pages[0].extract_words()
    words_r = pdf_r.pages[0].extract_words()
    
    print("=== Left Alignment (x0) Analysis ===")
    from collections import defaultdict
    x0_n = defaultdict(list)
    for w in words_n:
        x0_n[round(w['x0'], 1)].append(w['text'])
        
    x0_r = defaultdict(list)
    for w in words_r:
        x0_r[round(w['x0'], 1)].append(w['text'])
        
    common_x0 = sorted(set(x0_n.keys()).intersection(set(x0_r.keys())))
    for x in common_x0:
        print(f"\nx0 = {x:5.1f} pt:")
        print(f"  Nasih: {x0_n[x][:8]}")
        print(f"  Roy:   {x0_r[x][:8]}")
        
    print("\n=== Right Alignment (x1) Analysis ===")
    x1_n = defaultdict(list)
    for w in words_n:
        x1_n[round(w['x1'], 1)].append(w['text'])
        
    x1_r = defaultdict(list)
    for w in words_r:
        x1_r[round(w['x1'], 1)].append(w['text'])
        
    common_x1 = sorted(set(x1_n.keys()).intersection(set(x1_r.keys())))
    for x in common_x1:
        print(f"\nx1 = {x:5.1f} pt:")
        print(f"  Nasih: {x1_n[x][:8]}")
        print(f"  Roy:   {x1_r[x][:8]}")
