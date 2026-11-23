import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

client = PdfCraftClient()
doc_id = client.doc_open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_SEP_2026.pdf")
paras = client.get_paragraphs(doc_id, page=1)
for p in paras:
    if abs(p['rect'][1] - 343.92) < 20:
        print(f"Galang Sep P{p['paragraph']}: rect={p['rect']} text='{p['text']}'")
client.doc_close(doc_id, discard_changes=True)
