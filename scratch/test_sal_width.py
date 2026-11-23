import sys, shutil
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient
import pdfplumber

shutil.copyfile(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf", r"scratch/test_sal_width.pdf")

client = PdfCraftClient()
doc_id = client.doc_open(r"scratch/test_sal_width.pdf")

res = client.call_tool("text_lines", {"doc": doc_id, "page": 3})
lines = res.get('lines', [])
for l in lines:
    if '6.091.988,81' in l.get('text', ''):
        # rect is [29.0, 732.0, 571.0, 742.0]
        # width = 571.0 - 29.0 = 542.0
        w = round(l['rect'][2] - l['rect'][0], 2)
        print(f"Line rect: {l['rect']}, w={w}")
        client.edit_text(doc_id, page=3, line=l['line'], text=' 7.815.988,81', width=w, align='right')

client.doc_save(doc_id)
client.doc_close(doc_id)

with pdfplumber.open(r"scratch/test_sal_width.pdf") as pdf:
    p3 = pdf.pages[2]
    words = p3.extract_words()
    sal_words = [w for w in words if 725 <= w['top'] <= 750]
    for w in sorted(sal_words, key=lambda x: x['x0']):
        if '7.815.988,81' in w['text']:
            print(f"Result with width={w['x1']}: '{w['text']}' at x0={w['x0']:.1f}, x1={w['x1']:.1f}")
