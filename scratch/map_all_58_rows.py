import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

client = PdfCraftClient()
doc_id = client.doc_open(r'scratch/test_copy.pdf')

all_found_rows = []

for p in range(1, 6):
    res = client.call_tool("text_lines", {"doc": doc_id, "page": p})
    lines = res.get('lines', [])
    min_y = 315 if p == 1 else 200
    
    # Find all WIB lines on this page, sorted by top
    wib_lines = [l for l in lines if l['rect'][1] >= min_y and l['rect'][1] <= 800 and 'WIB' in l.get('text', '')]
    wib_lines.sort(key=lambda x: x['rect'][1])
    
    print(f"=== PAGE {p}: {len(wib_lines)} rows ===")
    for row_idx, w_line in enumerate(wib_lines):
        y_wib = w_line['rect'][1]
        
        # 1. Date line: 50 <= x0 <= 60, top within 15 pt above y_wib
        date_candidates = [l for l in lines if 48 <= l['rect'][0] <= 60 and 0 < (y_wib - l['rect'][1]) <= 15]
        d_line = date_candidates[0] if date_candidates else None
        
        # 2. No line: 18 <= x0 <= 25, abs(top - y_wib) <= 12
        no_candidates = [l for l in lines if 18 <= l['rect'][0] <= 25 and abs(l['rect'][1] - y_wib) <= 12]
        no_line = no_candidates[0] if no_candidates else None
        
        # 3. Nominal line: 360 <= x0 <= 410, abs(top - y_wib) <= 12
        nom_candidates = [l for l in lines if 360 <= l['rect'][0] <= 410 and abs(l['rect'][1] - y_wib) <= 12]
        nom_line = nom_candidates[0] if nom_candidates else None
        
        # 4. Saldo line: 450 <= x0 <= 540, abs(top - y_wib) <= 12
        sal_candidates = [l for l in lines if 450 <= l['rect'][0] <= 540 and abs(l['rect'][1] - y_wib) <= 12]
        sal_line = sal_candidates[0] if sal_candidates else None
        
        all_found_rows.append({
            'page': p,
            'row_idx': row_idx,
            'wib_line': w_line,
            'date_line': d_line,
            'no_line': no_line,
            'nom_line': nom_line,
            'sal_line': sal_line
        })
        
        d_txt = d_line['text'] if d_line else 'MISSING'
        no_txt = no_line['text'] if no_line else 'MISSING'
        nom_txt = nom_line['text'] if nom_line else 'MISSING'
        sal_txt = sal_line['text'] if sal_line else 'MISSING'
        print(f"  Row {len(all_found_rows):2d}: No='{no_txt}' Date='{d_txt}' Time='{w_line['text']}' Nom='{nom_txt}' Sal='{sal_txt}'")

client.doc_close(doc_id, discard_changes=True)
print(f"Total rows found across 5 pages: {len(all_found_rows)}")
