import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = "output/REK_GALANG_JUL_2026_STANDARDIZED.pdf"

with pdfplumber.open(pdf_path) as pdf:
    for page_idx in range(2):
        p_num = page_idx + 1
        page = pdf.pages[page_idx]
        print(f"\n==================== PAGE {p_num} ====================")
        words = page.extract_words()
        
        # Check Name section
        name_words = [w for w in words if 90 <= w['top'] <= 125 and 120 <= w['x0'] <= 230]
        print("NAME WORDS:")
        for w in sorted(name_words, key=lambda x: (x['top'], x['x0'])):
            print(f"  '{w['text']}' top={w['top']:.2f}, bottom={w['bottom']:.2f}, x0={w['x0']:.2f}, x1={w['x1']:.2f}")
            
        # Group name by lines
        lines = {}
        for w in name_words:
            # find line
            matched = False
            for y_k in lines:
                if abs(w['top'] - y_k) < 3.0:
                    lines[y_k].append(w)
                    matched = True
                    break
            if not matched:
                lines[w['top']] = [w]
                
        print(f"Name detected lines count: {len(lines)}")
        for y_k in sorted(lines.keys()):
            line_str = " ".join([w['text'] for w in sorted(lines[y_k], key=lambda x: x['x0'])])
            x0 = min(w['x0'] for w in lines[y_k])
            x1 = max(w['x1'] for w in lines[y_k])
            print(f"  Line @ Y_top={y_k:.2f}: '{line_str}' (x0={x0:.2f}, x1={x1:.2f})")
            
        print("\nTRANSACTION DESCRIPTIONS:")
        base_y_start = 343.92 if p_num == 1 else 227.92
        num_rows = 10 if p_num == 1 else 12
        for r_i in range(num_rows):
            row_y = base_y_start + r_i * 46.00
            desc_words = [w for w in words if abs(w['top'] - row_y) < 24.0 and 120 <= w['x0'] <= 360]
            # group into lines
            d_lines = {}
            for w in desc_words:
                matched = False
                for y_k in d_lines:
                    if abs(w['top'] - y_k) < 3.0:
                        d_lines[y_k].append(w)
                        matched = True
                        break
                if not matched:
                    d_lines[w['top']] = [w]
            
            line_texts = []
            for y_k in sorted(d_lines.keys()):
                l_txt = " ".join([w['text'] for w in sorted(d_lines[y_k], key=lambda x: x['x0'])])
                line_texts.append(f"[Y={y_k:.1f}] {l_txt}")
            
            print(f"Row {r_i+1:2d} (Y_base={row_y:.2f}, lines={len(d_lines)}): {' // '.join(line_texts)}")
