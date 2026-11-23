import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_path)
    for p_num in range(1, 6):
        paras = client.get_paragraphs(doc_id, page=p_num)
        nom_paras = [p for p in paras if 370 <= p["rect"][0] <= 450 and ("+" in p["text"] or "-" in p["text"]) and p["rect"][1] > 200]
        print(f"Page {p_num} nominal right edges:")
        for p in nom_paras[:3]:
            print(f"  text={p['text']:>15}, rect={p['rect']}, right_x={p['rect'][2]:.2f}")
