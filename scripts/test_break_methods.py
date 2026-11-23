import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient
import pdfplumber

# Let's test: can we pass \r\n or multiple spaces or something?
test_pdf = "output/test_split_breaks.pdf"
import shutil
shutil.copyfile("templates/master_page_1.pdf", test_pdf)

with PdfCraftClient() as client:
    doc_id = client.doc_open(test_pdf)
    
    # Test 1: width=175.0 with \r\n
    client.call_tool("text_edit", {
        "doc": doc_id, "page": 1, "paragraph": 55,
        "text": "Transfer BI Fast\r\nDari BCA\r\nPT BENDI NASHA NIAGA INDUSTRI 5411078192\r\n(CENAIDJA)",
        "width": 175.0,
        "line_spacing": 1.25
    })
    
    # Test 2: width=175.0 with \n\n?
    # Test 3: what if we pad with spaces? "Transfer BI Fast" + " " * 30 + "Dari BCA"?
    client.call_tool("text_edit", {
        "doc": doc_id, "page": 1, "paragraph": 61,
        "text": "Transfer BI Fast                         \nDari BCA                                 \nPT BENDI NASHA NIAGA INDUSTRI 5411078192\n(CENAIDJA)",
        "width": 175.0,
        "line_spacing": 1.25
    })

    client.doc_save(doc_id, path=test_pdf, full=True)
    client.doc_close(doc_id)

with pdfplumber.open(test_pdf) as pdf:
    p1 = pdf.pages[0]
    words = p1.extract_words()
    print("--- Test 1 (P55 with \r\n): ---")
    w55 = [w for w in words if 420 <= w['top'] <= 460 and 120 <= w['x0'] <= 365]
    lines55 = {}
    for w in sorted(w55, key=lambda x: (x['top'], x['x0'])):
        lines55.setdefault(round(w['top'], 1), []).append(w['text'])
    for top, ws in sorted(lines55.items()):
        print(f"  top={top:5.1f}: {' '.join(ws)}")

    print("\n--- Test 2 (P61 with padded spaces): ---")
    w61 = [w for w in words if 465 <= w['top'] <= 510 and 120 <= w['x0'] <= 365]
    lines61 = {}
    for w in sorted(w61, key=lambda x: (x['top'], x['x0'])):
        lines61.setdefault(round(w['top'], 1), []).append(w['text'])
    for top, ws in sorted(lines61.items()):
        print(f"  top={top:5.1f}: {' '.join(ws)}")
