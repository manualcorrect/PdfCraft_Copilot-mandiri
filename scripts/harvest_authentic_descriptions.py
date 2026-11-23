import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
import pdfplumber

files_to_scan = [
    r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Salman\REK APR26.pdf",
    r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\REK GALANG JUL 2026.pdf",
    r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\REK GALANG AUG 2026.pdf",
    r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\REK GALANG SEP 2026.pdf",
    r"D:\X_Files\rekening\Reference\Roy\ilovepdf_unlocked\Agu 2026_unlocked.pdf",
    r"D:\X_Files\rekening\Reference\Roy\ilovepdf_unlocked\Mei 2026_unlocked.pdf",
    r"D:\X_Files\rekening\Reference\nasih 2024 new unlocked\ilovepdf_unlocked\e-Statement_XXXXXXXXX9210_01 Des 2024-31 Des 2024_unlocked.pdf",
    r"D:\X_Files\rekening\Reference\suhanda unlocked\e-Statement_XXXXXXXXX9648_01 Apr 2026-30 Apr 2026_unlocked.pdf",
]

descriptions_catalog = []

for f_path in files_to_scan:
    if not os.path.exists(f_path):
        continue
    f_name = os.path.basename(f_path)
    with pdfplumber.open(f_path) as pdf:
        for page_idx, page in enumerate(pdf.pages):
            words = page.extract_words()
            # Filter table region
            min_y = 320 if page_idx == 0 else 200
            max_y = 780
            table_words = [w for w in words if min_y <= w['top'] <= max_y]
            
            # Group by row
            # Base rows
            base_start = 343.92 if page_idx == 0 else 227.92
            for r_i in range(12):
                row_y = base_start + r_i * 46.00
                row_desc_words = [w for w in table_words if 120 <= w['x0'] <= 360 and abs(w['top'] - row_y) < 22.0]
                if not row_desc_words:
                    continue
                
                # Check if there is a number or nominal in this row
                has_no = any(w['x0'] < 35 and w['text'].isdigit() for w in table_words if abs(w['top'] - row_y) < 22.0)
                if not has_no:
                    continue
                    
                # Group desc words by line (Y within 3pt)
                lines = {}
                for w in row_desc_words:
                    matched = False
                    for y_k in lines:
                        if abs(w['top'] - y_k) < 3.0:
                            lines[y_k].append(w)
                            matched = True
                            break
                    if not matched:
                        lines[w['top']] = [w]
                
                line_strs = []
                for y_k in sorted(lines.keys()):
                    l_str = " ".join([w['text'] for w in sorted(lines[y_k], key=lambda x: x['x0'])])
                    line_strs.append(l_str)
                    
                full_desc = "\n".join(line_strs)
                y_span = (min(lines.keys()), max(lines.keys()) + 8.0) if lines else (0, 0)
                
                descriptions_catalog.append({
                    "file": f_name,
                    "page": page_idx + 1,
                    "row": r_i + 1,
                    "lines": line_strs,
                    "line_count": len(line_strs),
                    "full_text": full_desc,
                    "y_span": y_span
                })

print(f"Total authentic descriptions harvested: {len(descriptions_catalog)}")

# Group by category / pattern prefix
categories = {}
for item in descriptions_catalog:
    txt = item["full_text"]
    first_line = item["lines"][0] if item["lines"] else ""
    cat = "OTHER"
    if "Transfer BI Fast" in txt or "Transfer BI FAST" in txt:
        cat = "BI_FAST"
    elif "Transfer" in txt and "BANK MANDIRI" in txt:
        cat = "MANDIRI_INHOUSE"
    elif "Penarikan tunai" in txt:
        cat = "ATM_WITHDRAWAL"
    elif "Pembayaran QR" in txt:
        cat = "QR_PAYMENT"
    elif "Pembayaran Shopee" in txt or "Pembayaran Tokopedia" in txt or "Pembayaran TikTok" in txt:
        cat = "ECOMMERCE"
    elif "Pembayaran" in txt or "Top-up" in txt:
        cat = "EWALLET_BILLER"
    elif "Biaya" in txt or "Bunga" in txt or "Pajak" in txt:
        cat = "BANK_FEE_INTEREST"
        
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(item)

for cat, items in sorted(categories.items()):
    print(f"\n=================== CATEGORY: {cat} ({len(items)} samples) ===================")
    # show unique structures
    unique_patterns = set()
    for it in items:
        struct = f"[{it['line_count']} lines] " + " // ".join(it["lines"])
        if struct not in unique_patterns:
            unique_patterns.add(struct)
            print(f"  * ({it['file']} p{it['page']} r{it['row']}): {struct}")
