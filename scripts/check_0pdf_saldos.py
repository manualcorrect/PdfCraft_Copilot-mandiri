import pdfplumber

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

with pdfplumber.open(pdf_path) as pdf:
    tx_count = 0
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        min_top = 320 if p_idx == 0 else 200
        table_words = [w for w in words if min_top <= w['top'] <= 800]
        # find saldos: x0 >= 490
        wibs = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        print(f"\n--- Page {p_idx + 1} ({len(wibs)} transactions) ---")
        for r_i, w in enumerate(wibs):
            tx_count += 1
            # find saldo candidate near w['top']
            sal_cands = [x for x in table_words if abs(x['top'] - w['top']) < 15 and x['x0'] >= 480]
            sal_str = " ".join([x['text'] for x in sal_cands])
            nom_cands = [x for x in table_words if abs(x['top'] - w['top']) < 15 and 370 <= x['x0'] < 480]
            nom_str = " ".join([x['text'] for x in nom_cands])
            print(f"  Tx {tx_count:2d} (P{p_idx+1} R{r_i+1:2d}): Nom={nom_str:>16} Saldo={sal_str:>16}")
