import sys, shutil
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient
import pdfplumber

shutil.copyfile(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf", r"scratch/test_sal_dx.pdf")

client = PdfCraftClient()
doc_id = client.doc_open(r"scratch/test_sal_dx.pdf")

# Line 127 on Page 3 is Row 34 saldo: ' 6.091.988,81'
res = client.call_tool("text_lines", {"doc": doc_id, "page": 3})
lines = res.get('lines', [])
for l in lines:
    if '6.091.988,81' in l.get('text', ''):
        # target right x is 571.00
        # let's edit text and apply dx
        client.edit_text(doc_id, page=3, line=l['line'], text=' 7.815.988,81', dx=494.44)

client.doc_save(doc_id)
client.doc_close(doc_id)

with pdfplumber.open(r"scratch/test_sal_dx.pdf") as pdf:
    p3 = pdf.pages[2]
    words = p3.extract_words()
    for w in words:
        if '7.815.988,81' in w['text']:
            print(f"FOUND: '{w['text']}' at x0={w['x0']:.2f}, x1={w['x1']:.2f}, top={w['top']:.2f}")
