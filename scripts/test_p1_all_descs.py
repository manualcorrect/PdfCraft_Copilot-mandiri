import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from pdfcraft_client import PdfCraftClient
import pdfplumber

# Let's test on a copy of master_page_1.pdf
with PdfCraftClient() as client:
    doc_id = client.doc_open("templates/master_page_1.pdf")
    
    # Harvest descriptions from 2.pdf page 1
    pdf_source = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf"
    with pdfplumber.open(pdf_source) as pdf:
        words = pdf.pages[0].extract_words()
        wib_words = sorted([w for w in words if w['text'] == 'WIB' and w['top'] > 320], key=lambda x: x['top'])
        for r_i, ww in enumerate(wib_words):
            row_y = 343.92 + r_i * 46.00
            desc_words = sorted([w for w in words if abs(w['top'] - ww['top']) < 22 and 120 <= w['x0'] <= 365], key=lambda x: (x['top'], x['x0']))
            lines = []
            curr_l = []
            curr_y = None
            for w in desc_words:
                if curr_y is None or abs(w['top'] - curr_y) < 4:
                    curr_l.append(w['text'])
                    curr_y = w['top'] if curr_y is None else (curr_y * 0.7 + w['top'] * 0.3)
                else:
                    lines.append(" ".join(curr_l))
                    curr_l = [w['text']]
                    curr_y = w['top']
            if curr_l:
                lines.append(" ".join(curr_l))
            
            desc_text = "\n".join(lines)
            num_lines = len(lines)
            dy = (num_lines - 1) * 5.0
            
            paras = client.get_paragraphs(doc_id, page=1)
            p_desc = [p for p in paras if abs(p["rect"][1] - row_y) < 20 and 120 <= p["rect"][0] <= 135]
            if p_desc:
                client.call_tool("text_edit", {
                    "doc": doc_id,
                    "page": 1,
                    "paragraph": p_desc[0]["paragraph"],
                    "text": desc_text,
                    "dy": dy,
                    "line_spacing": 1.25,
                    "width": 230.0
                })
                
    client.doc_save(doc_id, path="output/test_all_desc_p1.pdf")
    client.doc_close(doc_id)

print("=== Checking Output Tops in test_all_desc_p1.pdf ===")
with pdfplumber.open("output/test_all_desc_p1.pdf") as pdf:
    p1 = pdf.pages[0]
    words = p1.extract_words()
    for r in range(1, 11):
        row_y = 343.92 + (r - 1) * 46.00
        desc_w = sorted([w for w in words if abs(w['top'] - row_y) < 22 and 120 <= w['x0'] <= 365], key=lambda x: (x['top'], x['x0']))
        lines = {}
        for w in desc_w:
            lines.setdefault(round(w['top'], 1), []).append(w['text'])
        print(f"Row {r:02d} (row_y={row_y:.2f}):")
        for top in sorted(lines.keys()):
            print(f"    top={top:5.1f}: {' '.join(lines[top])}")
