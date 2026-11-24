import sys
import shutil
import pdfplumber
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

pdf_src = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\okt\0.pdf'
pdf_test = r'c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\test_p80.pdf'
shutil.copyfile(pdf_src, pdf_test)

new_desc = "Transfer BI Fast\nDari BCA\nPT BENDI NASHA NIAGA INDUSTRI 5411078192\n(CENAIDJA)"

with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_test)
    client.edit_text(doc_id, page=3, paragraph=80, text=new_desc, width=240.0)
    client.doc_save(doc_id, pdf_test)
    client.doc_close(doc_id)

with pdfplumber.open(pdf_test) as pdf:
    p3 = pdf.pages[2]
    words = p3.extract_words()
    p80_words = [w for w in words if 710 <= w['top'] <= 760 and 120 <= w['x0'] <= 300]
    p80_words.sort(key=lambda x: (x['top'], x['x0']))
    print("Edited P80 words:")
    for w in p80_words:
        print(f"  {w['text']} at top={w['top']:.2f}, bottom={w['bottom']:.2f}, x0={w['x0']:.2f}")
