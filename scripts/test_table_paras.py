import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

pdf_src = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_src)
    paras = client.get_paragraphs(doc_id, page=1)
    min_top = 310
    t_paras = [p for p in paras if min_top <= p["rect"][1] <= 780]
    print(f"Total table paragraphs on Page 1: {len(t_paras)}")
    wibs = [p for p in t_paras if "WIB" in p["text"]]
    print(f"WIB count: {len(wibs)}")
    for i, w in enumerate(wibs):
        y = w["rect"][1]
        nos = [p for p in t_paras if abs(p["rect"][1] - y) < 15 and 15 <= p["rect"][0] <= 35]
        sals = [p for p in t_paras if abs(p["rect"][1] - y) < 15 and 500 <= p["rect"][0] <= 580 and "," in p["text"]]
        n_str = nos[0]["text"] if nos else "NONE"
        s_str = sals[0]["text"] if sals else "NONE"
        print(f"Row {i+1}: y={y:.1f} | No={n_str:<5} | Saldo={s_str}")
    client.doc_close(doc_id)
