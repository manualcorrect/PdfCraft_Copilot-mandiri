import shutil
import re
import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

pdf_src = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf"
pdf_test = "output/test_save.pdf"
shutil.copyfile(pdf_src, pdf_test)

with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_test)
    paras = client.get_paragraphs(doc_id, page=1)
    # edit one small thing
    p_name = [p for p in paras if "ROY" in p["text"]][0]
    client.edit_text(doc_id, page=1, paragraph=p_name["paragraph"], text="IBNU AGUN")
    client.doc_save(doc_id, pdf_test)
    client.doc_close(doc_id)

with open(pdf_test, "rb") as f:
    pdf_bytes = f.read()

page_matches = list(re.finditer(rb'(\d+)\s+0\s+obj\s*<<(?:(?!endobj).)*?/Type\s*/Page\b(?:(?!endobj).)*?>>\s*endobj', pdf_bytes, re.DOTALL))
print("Found pages count:", len(page_matches))
for idx, pm in enumerate(page_matches):
    p_oid = int(pm.group(1))
    p_text = pm.group(0).decode('latin1', errors='ignore')
    m_contents = re.search(r'/Contents\s+(\d+)\s+0\s+R', p_text)
    if m_contents:
        print(f"Page {idx+1} (OID {p_oid}): /Contents {m_contents.group(1)}")
