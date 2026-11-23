import sys, shutil
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

shutil.copyfile(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf', r'scratch/test_copy.pdf')

client = PdfCraftClient()
doc_id = client.doc_open(r'scratch/test_copy.pdf')

# Test editing Line 64 (Date: '01 Mar 2026' -> '01 Aug 2026')
print("Testing edit Line 64...")
res = client.edit_text(doc_id, page=1, line=64, text='01 Aug 2026')
print("Result:", res)

# Check line 64 after edit
res2 = client.call_tool("text_lines", {"doc": doc_id, "page": 1})
lines = res2.get('lines', [])
for l in lines:
    if '01 Aug 2026' in l.get('text', ''):
        print(f"Found edited line: Line {l['line']} rect={l['rect']} text='{l['text']}'")

client.doc_save(doc_id)
client.doc_close(doc_id)
