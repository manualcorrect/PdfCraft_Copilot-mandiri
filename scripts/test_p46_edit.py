import sys
import shutil
import pdfplumber
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

pdf_src = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\okt\0.pdf'
pdf_test = r'c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\test_p46.pdf'
shutil.copyfile(pdf_src, pdf_test)

with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_test)
    client.edit_text(doc_id, page=4, paragraph=80, text="Biaya administrasi rekening", width=240.0, dy=-5.0)
    client.doc_save(doc_id, pdf_test)
    client.doc_close(doc_id)

with pdfplumber.open(pdf_test) as pdf:
    p4 = pdf.pages[3]
    words = p4.extract_words()
    p46_words = [w for w in words if 725 <= w['top'] <= 750 and 120 <= w['x0'] <= 300]
    p46_words.sort(key=lambda x: (x['top'], x['x0']))
    print("Edited P46 words with dy=-5.0:")
    for w in p46_words:
        print(f"  {w['text']} at top={w['top']:.2f}, bottom={w['bottom']:.2f}, x0={w['x0']:.2f}")
    
    # Also check nominal and saldo tops on row 12
    r12_words = [w for w in words if 725 <= w['top'] <= 750 and (w['x0'] > 300 or w['x0'] < 100)]
    print("\nRow 12 reference words:")
    for w in r12_words:
        print(f"  {w['text']} at top={w['top']:.2f}, bottom={w['bottom']:.2f}, x0={w['x0']:.2f}")
