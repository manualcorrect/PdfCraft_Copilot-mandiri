import sys, shutil, pdfplumber
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

TEST_PDF = 'output/test_sep_p3.pdf'
shutil.copyfile(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\sep\0.pdf', TEST_PDF)

with PdfCraftClient() as client:
    doc_id = client.doc_open(TEST_PDF)
    
    # Tx 33 (Salary on Page 3)
    paras3 = client.get_paragraphs(doc_id, page=3)
    p33 = [p for p in paras3 if "ASHTI" in p["text"]][0]
    desc33 = "Transfer BI Fast\nDari BCA\nPT BENDI NASHA NIAGA INDUSTRI 5411078192\n(CENAIDJA)"
    client.edit_text(doc_id, page=3, paragraph=p33["paragraph"], text=desc33, width=240.0, dy=12.34)
    
    client.doc_save(doc_id, TEST_PDF)
    client.doc_close(doc_id)

with pdfplumber.open(TEST_PDF) as pdf:
    p3 = pdf.pages[2]
    words = p3.extract_words()
    print("=== TEST RESULTS ON PAGE 3 (Tx 33) ===")
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        if 660 <= w['top'] <= 715:
            print(f"{w['top']:.2f}, {w['x0']:.2f}-{w['x1']:.2f}: {w['text']}")
