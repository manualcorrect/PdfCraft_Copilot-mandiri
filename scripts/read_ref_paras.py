import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

ref_pdf = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\.user_uploaded\media_1794538873844_ae928147.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(ref_pdf)
    paras = client.get_paragraphs(doc_id, page=1)
    print("--- REFERENCE PARAGRAPHS ON PAGE 1 (top 150..260) ---")
    for p in paras:
        if 150 <= p["rect"][1] <= 260 and p["rect"][0] > 280:
            print(f"  Para {p['paragraph']:02d} rect={p['rect']}: text='{p['text']}'")
    client.doc_close(doc_id)
