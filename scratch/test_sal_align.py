import sys, shutil
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient
import pdfplumber

shutil.copyfile(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf", r"scratch/test_sal_align.pdf")

client = PdfCraftClient()
doc_id = client.doc_open(r"scratch/test_sal_align.pdf")

# Line 127 on Page 3 is Row 34 saldo: ' 6.091.988,81'
res = client.call_tool("text_lines", {"doc": doc_id, "page": 3})
lines = res.get('lines', [])
for l in lines:
    if '6.091.988,81' in l.get('text', ''):
        print("Found line 127:", l)
        # Edit with align='right'
        client.edit_text(doc_id, page=3, line=l['line'], text=' 7.815.988,81', align='right')

client.doc_save(doc_id)
client.doc_close(doc_id)

with pdfplumber.open(r"scratch/test_sal_align.pdf") as pdf:
    p3 = pdf.pages[2]
    words = p3.extract_words()
    sal_words = [w for w in words if 725 <= w['top'] <= 745 and w['x0'] > 450]
    for w in sal_words:
        print(f"Result with align='right': '{w['text']}' at x0={w['x0']:.1f}, x1={w['x1']:.1f}")
