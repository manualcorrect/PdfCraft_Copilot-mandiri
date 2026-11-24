import sys, shutil, pdfplumber
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

TEST_PDF = 'output/test_edit_p3.pdf'
shutil.copyfile(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\0.pdf', TEST_PDF)

with PdfCraftClient() as client:
    doc_id = client.doc_open(TEST_PDF)
    
    # Tx 24
    paras3 = client.get_paragraphs(doc_id, page=3)
    p24 = [p for p in paras3 if "KARINA AMALIA DARMAW" in p["text"]][0]
    desc24 = "Transfer BI Fast\nDari BCA\nPT BENDI NASHA NIAGA INDUSTRI 5411078192\n(CENAIDJA)"
    client.edit_text(doc_id, page=3, paragraph=p24["paragraph"], text=desc24, width=240.0, dy=2.34)
    
    # Tx 33 (Penarikan tunai di ATM)
    paras3 = client.get_paragraphs(doc_id, page=3)
    p33 = [p for p in paras3 if "Biaya transaksi bank" in p["text"] and 670 <= p["rect"][1] <= 700][0]
    desc33 = "Penarikan tunai di ATM\nBANK MANDIRI SRG AM PURI ANGREK 01"
    client.edit_text(doc_id, page=3, paragraph=p33["paragraph"], text=desc33, width=240.0, dy=-5.0)
    
    # Tx 34 (Biaya administrasi rekening)
    paras3 = client.get_paragraphs(doc_id, page=3)
    p34 = [p for p in paras3 if "Pembayaran Danatopup" in p["text"] and 720 <= p["rect"][1] <= 750][0]
    desc34 = "Biaya administrasi rekening"
    client.edit_text(doc_id, page=3, paragraph=p34["paragraph"], text=desc34, width=240.0, dy=-5.0)
    
    client.doc_save(doc_id, TEST_PDF)
    client.doc_close(doc_id)

with pdfplumber.open(TEST_PDF) as pdf:
    p3 = pdf.pages[2]
    words = p3.extract_words()
    print("=== TEST RESULTS ON PAGE 3 ===")
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        if (250 <= w['top'] <= 300) or (680 <= w['top'] <= 750):
            print(f"{w['top']:.2f}, {w['x0']:.2f}-{w['x1']:.2f}: {w['text']}")
