import pdfplumber

with pdfplumber.open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\sep\0.pdf') as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    tx_count = 0
    for p_idx in range(4): # Pages 1..4
        page = pdf.pages[p_idx]
        words = page.extract_words()
        min_top = 310 if p_idx == 0 else 180
        t_words = [w for w in words if min_top <= w['top'] <= 780]
        wibs = sorted([w for w in t_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        print(f"\n--- Page {p_idx+1} ({len(wibs)} transactions) ---")
        for r_i, w in enumerate(wibs):
            tx_count += 1
            y = w['top']
            row_words = [x for x in t_words if abs(x['top'] - y) < 18]
            row_words.sort(key=lambda x: x['x0'])
            
            # Find No & Saldo (on same line or near y)
            saldos = [x for x in t_words if abs(x['top'] - y) < 8 and x['x0'] > 500]
            saldo_str = saldos[0]['text'] if saldos else 'NO_SALDO'
            
            # Find Nominal
            noms = [x for x in t_words if abs(x['top'] - y) < 8 and 350 <= x['x0'] <= 450]
            nom_str = noms[0]['text'] if noms else 'NO_NOM'
            
            # Find Date
            d_cand = [x for x in t_words if 0 < (y - x['top']) < 18 and 45 <= x['x0'] <= 95]
            d_cand.sort(key=lambda x: x['x0'])
            d_str = " ".join([x['text'] for x in d_cand])
            
            print(f"Tx {tx_count:2d} (P{p_idx+1} R{r_i+1:2d}) [Y={y:.1f}]: Date='{d_str}' Time='{w['text']}' Nom='{nom_str}' Saldo='{saldo_str}'")
