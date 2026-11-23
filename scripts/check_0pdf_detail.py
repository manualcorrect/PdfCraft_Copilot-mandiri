import pdfplumber

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf"

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages in 0.pdf: {len(pdf.pages)}")
    all_txs = []
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        min_top = 310 if p_idx == 0 else 180
        # extract row numbers in No column (x0 < 30)
        no_words = [w for w in words if min_top <= w['top'] <= 780 and 15 <= w['x0'] <= 35]
        no_words.sort(key=lambda w: w['top'])
        print(f"Page {p_idx+1}: {len(no_words)} No entries: {[w['text'] for w in no_words]}")
        
        # also let's look at WIB count on this page
        wibs = [w for w in words if min_top <= w['top'] <= 780 and w['text'] == 'WIB']
        print(f"  WIB count: {len(wibs)}")
        
        # let's look at Nominals (x0 between 370 and 420)
        noms = [w for w in words if min_top <= w['top'] <= 780 and 360 <= w['x0'] <= 430 and (w['text'].startswith('+') or w['text'].startswith('-'))]
        print(f"  Nominal count: {len(noms)}")

        # let's check saldos
        saldos = [w for w in words if min_top <= w['top'] <= 780 and 500 <= w['x0'] <= 570 and (',' in w['text'])]
        print(f"  Saldo count: {len(saldos)}")
