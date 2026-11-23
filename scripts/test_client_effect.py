import shutil
import sys
import re
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

src = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"
dst = r"output\test_sep_client_save.pdf"
shutil.copyfile(src, dst)

with PdfCraftClient() as client:
    doc_id = client.doc_open(dst)
    # just edit one field: Name
    paras = client.get_paragraphs(doc_id, page=1)
    p_name = [p for p in paras if "ROY DARWIN REZERIUS" in p["text"]][0]
    client.edit_text(doc_id, page=1, paragraph=p_name["paragraph"], text="KEISYA AULIA")
    client.doc_save(doc_id)

with open(dst, "rb") as f:
    b = f.read()

objs = re.findall(rb'(\d+)\s+0\s+obj', b)
print("Objects after PdfCraftClient save:", [int(x) for x in objs])
m_xref = re.search(rb'startxref\s+(\d+)', b)
print("startxref:", m_xref.group(1).decode() if m_xref else "None")
