import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = "output/REK_GALANG_JUL_2026_STANDARDIZED.pdf"

with pdfplumber.open(pdf_path) as pdf:
    for page_idx in range(2):
        p_num = page_idx + 1
        page = pdf.pages[page_idx]
        print(f"\n>>> PAGE {p_num} DATES & TIMES <<<")
        words = page.extract_words()
        
        min_y = 320 if p_num == 1 else 200
        table_words = [w for w in words if min_y <= w['top'] <= 800]
        
        base_y_start = 343.92 if p_num == 1 else 227.92
        num_rows = 10 if p_num == 1 else 12
        
        for r_i in range(num_rows):
            row_y = base_y_start + r_i * 46.00
            row_words = [w for w in table_words if abs(w['top'] - row_y) < 25.0]
            
            # Find date day & time
            day_w = [w for w in row_words if 45 <= w['x0'] <= 55 and w['text'].isdigit() and int(w['text']) <= 31]
            time_w = [w for w in row_words if 45 <= w['x0'] <= 55 and ':' in w['text']]
            
            day_str = day_w[0]['text'] if day_w else '?'
            day_x0 = day_w[0]['x0'] if day_w else -1
            time_str = time_w[0]['text'] if time_w else '?'
            time_x0 = time_w[0]['x0'] if time_w else -1
            
            day_status = "PASS (52.00)" if abs(day_x0 - 52.00) < 0.05 else f"FAIL ({day_x0:.2f})"
            time_status = "PASS (52.00)" if abs(time_x0 - 52.00) < 0.05 else f"FAIL ({time_x0:.2f})"
            
            print(f"Row {r_i+1:2d} | Day={day_str:2s} ({day_status}) | Time={time_str:8s} ({time_status})")
