import pdfplumber

pdf_source = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf"

with pdfplumber.open(pdf_source) as pdf:
    for p_idx, page in enumerate(pdf.pages):
        print(f"\n==================== 2.pdf PAGE {p_idx+1} ====================")
        words = page.extract_words()
        min_top = 320 if p_idx == 0 else 200
        table_words = [w for w in words if min_top <= w['top'] <= 800]
        
        # Let's see all text lines
        # Group words by top (tolerance 3 pt)
        lines = []
        curr_line = []
        curr_top = None
        for w in sorted(table_words, key=lambda x: (x['top'], x['x0'])):
            if curr_top is None or abs(w['top'] - curr_top) <= 3:
                curr_line.append(w)
                curr_top = w['top'] if curr_top is None else (curr_top * 0.7 + w['top'] * 0.3)
            else:
                lines.append(curr_line)
                curr_line = [w]
                curr_top = w['top']
        if curr_line:
            lines.append(curr_line)
            
        for l in lines:
            line_str = " ".join(w['text'] for w in l)
            print(f"  y={l[0]['top']:.1f}, x0={l[0]['x0']:.1f}: {line_str}")
