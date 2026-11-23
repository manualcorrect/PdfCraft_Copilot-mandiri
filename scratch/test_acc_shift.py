import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient
import pdfplumber

client = PdfCraftClient()
doc_id = client.doc_open(r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\REK_KEISYA_AUG_OUTPUT_1.pdf")

res = client.call_tool("text_lines", {"doc": doc_id, "page": 1})
lines = res.get('lines', [])
for l in lines:
    if '1630016478664' in l.get('text', ''):
        print("Found line:", l)
        client.edit_text(doc_id, page=1, line=l['line'], text='1630016478664', dx=12.0)

client.doc_save(doc_id)
client.doc_close(doc_id)

with pdfplumber.open(r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\REK_KEISYA_AUG_OUTPUT_1.pdf") as pdf:
    p1 = pdf.pages[0]
    words = p1.extract_words()
    acc_words = [w for w in words if 180 <= w['top'] <= 210 and w['x0'] < 250]
    for w in acc_words:
        print(f"'{w['text']}' at x0={w['x0']:.1f}, x1={w['x1']:.1f}, top={w['top']:.1f}")
