import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

pdf_path = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\okt\0.pdf'
with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_path)
    paras = client.get_paragraphs(doc_id, page=3)
    p_bot = [p for p in paras if p['rect'][1] > 700]
    p_bot.sort(key=lambda x: (x['rect'][1], x['rect'][0]))
    for p in p_bot:
        print(f"P{p['paragraph']}: {p['rect']} -> {repr(p['text'])}")
    client.doc_close(doc_id)
