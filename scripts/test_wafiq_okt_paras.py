import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

pdf_path = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\okt\0.pdf'
with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_path)
    for p in range(1, 5):
        paras = client.get_paragraphs(doc_id, page=p)
        print(f"=== Page {p} Header Paras ===")
        for hp in paras:
            if hp['rect'][1] < 150:
                print(f"  P{hp['paragraph']}: {hp['rect']} -> {repr(hp['text'])}")
    client.doc_close(doc_id)
