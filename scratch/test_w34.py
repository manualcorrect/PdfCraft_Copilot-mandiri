import sys
import shutil
import pdfplumber

sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

pdf_src = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\0.pdf"
pdf_test = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\scratch\test_w34.pdf"
shutil.copyfile(pdf_src, pdf_test)

with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_test)
    paras = client.get_paragraphs(doc_id, page=3)
    p34 = [p for p in paras if "Pembayaran Danatopup" in p["text"] and 720 <= p["rect"][1] <= 750][0]
    client.edit_text(doc_id, page=3, paragraph=p34["paragraph"], text="Biaya administrasi rekening", width=240.0)
    client.doc_save(doc_id, pdf_test)
    client.doc_close(doc_id)

with pdfplumber.open(pdf_test) as pdf:
    p3 = pdf.pages[2]
    words = [w for w in p3.extract_words() if 715 <= w["top"] <= 755 and 115 <= w["x0"] <= 300]
    lines = {}
    for w in sorted(words, key=lambda x: (x["top"], x["x0"])):
        lines.setdefault(round(w["top"], 1), []).append(w["text"])
    for top in sorted(lines.keys()):
        print(f"Top {top:5.1f}: {' '.join(lines[top])}")
