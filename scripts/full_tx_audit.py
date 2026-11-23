import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = "output/REK_GALANG_JUL_2026_STANDARDIZED.pdf"

print(f"=== FULL TRANSACTION AUDIT FOR: {pdf_path} ===")

with pdfplumber.open(pdf_path) as pdf:
    for page_idx in range(2):
        p_num = page_idx + 1
        page = pdf.pages[page_idx]
        print(f"\n>>> PAGE {p_num} TRANSACTIONS <<<")
        words = page.extract_words()
        
        min_y = 320 if p_num == 1 else 200
        table_words = [w for w in words if min_y <= w['top'] <= 800]
        
        # Group words by vertical position
        base_y_start = 343.92 if p_num == 1 else 227.92
        num_rows = 10 if p_num == 1 else 12
        
        for r_i in range(num_rows):
            row_y = base_y_start + r_i * 46.00
            row_words = [w for w in table_words if abs(w['top'] - row_y) < 25.0]
            
            # Find elements in this row
            no_w = [w for w in row_words if w['x0'] < 35 and w['text'].isdigit()]
            date_w = [w for w in row_words if 45 <= w['x0'] <= 55 and 'Jul' not in w['text'] and not w['text'].isdigit() and ':' not in w['text'] or (w['text'].isdigit() and 45 <= w['x0'] <= 55 and int(w['text']) <= 31)]
            # Nominals
            nom_w = [w for w in row_words if (w['text'].startswith('+') or w['text'].startswith('-')) and 350 <= w['x0'] <= 450]
            # Saldos
            sal_w = [w for w in row_words if 500 <= w['x0'] <= 585 and ',' in w['text'] and not w['text'].startswith('+') and not w['text'].startswith('-')]
            # Description
            desc_w = [w for w in row_words if 120 <= w['x0'] <= 130]
            
            no_str = no_w[0]['text'] if no_w else '?'
            no_x0 = no_w[0]['x0'] if no_w else -1
            nom_str = nom_w[0]['text'] if nom_w else '?'
            nom_x1 = nom_w[0]['x1'] if nom_w else -1
            sal_str = sal_w[0]['text'] if sal_w else '?'
            sal_x1 = sal_w[0]['x1'] if sal_w else -1
            desc_x0 = desc_w[0]['x0'] if desc_w else -1
            
            nom_status = "PASS (432.00)" if abs(nom_x1 - 432.00) < 0.05 else f"FAIL ({nom_x1:.2f})"
            sal_status = "PASS (571.00)" if abs(sal_x1 - 571.00) < 0.05 else f"FAIL ({sal_x1:.2f})"
            no_status = "PASS (20.00)" if abs(no_x0 - 20.00) < 0.05 else f"FAIL ({no_x0:.2f})"
            desc_status = "PASS (124.00)" if abs(desc_x0 - 124.00) < 0.05 else f"FAIL ({desc_x0:.2f})"
            
            print(f"Row {r_i+1:2d} | No={no_str:2s} ({no_status}) | Desc_x0={desc_status} | Nom={nom_str:15s} ({nom_status}) | Saldo={sal_str:13s} ({sal_status})")
