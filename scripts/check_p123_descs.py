import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

ref3_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(ref3_path)
    for p_num in range(1, 4):
        paras = client.get_paragraphs(doc_id, page=p_num)
        base_y = 343.92 if p_num == 1 else 227.92
        num_rows = 10 if p_num == 1 else 12
        print(f"\n--- Page {p_num} Keterangan Paras ---")
        for r_i in range(num_rows):
            row_y = base_y + r_i * 46.00
            p_desc = [p for p in paras if abs(p["rect"][1] - row_y) < 22 and 120 <= p["rect"][0] <= 135]
            if p_desc:
                p_obj = p_desc[0]
                print(f"Row {r_i+1:2d} (row_y={row_y:.2f}): para {p_obj['paragraph']} rect={p_obj['rect']} text={repr(p_obj['text'])}")
            else:
                print(f"Row {r_i+1:2d} (row_y={row_y:.2f}): NO DESC PARA FOUND!")
    client.doc_close(doc_id)
