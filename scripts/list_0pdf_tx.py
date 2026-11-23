import pdfplumber
import re

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\okt\0.pdf"

with pdfplumber.open(pdf_path) as pdf:
    total_tx = 0
    pdf_tx_list = []
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        # Find all transaction numbers in column 1 (x0 ~ 15..35)
        # In Mandiri statements, tx numbers are integer words with top > 150 and top < 800
        col_no = [w for w in words if 15 <= w['x0'] <= 35 and 150 <= w['top'] <= 800 and w['text'].isdigit()]
        col_no.sort(key=lambda w: w['top'])
        print(f"Page {p_idx+1} ({len(col_no)} tx):")
        for w in col_no:
            # find amount on the same line (top ~ w['top'] +/- 3)
            amt_words = [aw for aw in words if 350 <= aw['x0'] <= 440 and abs(aw['top'] - w['top']) <= 5]
            saldo_words = [sw for sw in words if 500 <= sw['x0'] <= 580 and abs(sw['top'] - w['top']) <= 5]
            amt_str = amt_words[0]['text'] if amt_words else '?'
            saldo_str = saldo_words[0]['text'] if saldo_words else '?'
            print(f"  Tx {w['text']:3s} (top={w['top']:.1f}): amt={amt_str:15s} saldo={saldo_str}")
            pdf_tx_list.append({
                'page': p_idx + 1,
                'no': w['text'],
                'top': w['top'],
                'amt': amt_str,
                'saldo': saldo_str
            })
        total_tx += len(col_no)
    print(f"\nTotal transactions detected in 0.pdf: {total_tx}")
