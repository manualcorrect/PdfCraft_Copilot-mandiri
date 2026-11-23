import sys, os
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

client = PdfCraftClient()
p1_path = r"templates/master_page_1.pdf"
if os.path.exists(p1_path):
    doc_id = client.doc_open(p1_path)
    paras = client.get_paragraphs(doc_id, page=1)
    for p in paras:
        if abs(p['rect'][1] - 343.92) < 20:
            print(f"Master P1 P{p['paragraph']}: rect={p['rect']} text='{p['text']}'")
    client.doc_close(doc_id, discard_changes=True)
else:
    print("master_page_1.pdf not found in templates/")
