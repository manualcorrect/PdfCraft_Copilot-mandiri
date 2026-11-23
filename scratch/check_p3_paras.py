import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

client = PdfCraftClient()
doc_id = client.doc_open(r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\REK_KEISYA_AUG_OUTPUT_1.pdf")
paras = client.get_paragraphs(doc_id, page=3)
row_y = 227.92 + 11 * 46.00 # row_idx = 11 -> 733.92
print(f"Target row_y = {row_y}")
for p in paras:
    if abs(p['rect'][1] - row_y) < 20:
        print(f"P{p['paragraph']}: rect={p['rect']} text='{p['text']}'")
client.doc_close(doc_id, discard_changes=True)
