import sys, json
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

client = PdfCraftClient()
doc_id = client.doc_open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf')
paras = client.get_paragraphs(doc_id, page=1)
for p in paras:
    if p['paragraph'] in [41, 42, 43, 44, 45]:
        print(f"P{p['paragraph']}:")
        print("  rect:", p['rect'])
        print("  text:", p.get('text'))
        print("  editor_text:", p.get('editor_text'))
        print("  lines:", p.get('lines'))
client.doc_close(doc_id, discard_changes=True)
