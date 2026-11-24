import sys
import shutil

sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

pdf_src = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\0.pdf"
pdf_test = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\scratch\test_desc_edit.pdf"
shutil.copyfile(pdf_src, pdf_test)

with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_test)
    paras = client.get_paragraphs(doc_id, page=3)
    
    # Tx 24
    p24 = [p for p in paras if "KARINA AMALIA DARMAW" in p["text"]]
    print("Tx 24 para found:", len(p24))
    if p24:
        new_desc24 = "Transfer BI Fast\nDari BCA\nPT BENDI NASHA NIAGA INDUSTRI 5411078192\n(CENAIDJA)"
        client.edit_text(doc_id, page=3, paragraph=p24[0]["paragraph"], text=new_desc24)
        print("Tx 24 edited successfully.")
        
    # Tx 33
    paras = client.get_paragraphs(doc_id, page=3)
    p33 = [p for p in paras if "Biaya transaksi bank" in p["text"] and 670 <= p["rect"][1] <= 700]
    print("Tx 33 para found:", len(p33))
    if p33:
        new_desc33 = "Pembayaran Danatopup\n89508089622130569"
        client.edit_text(doc_id, page=3, paragraph=p33[0]["paragraph"], text=new_desc33)
        print("Tx 33 edited successfully.")
        
    # Tx 34
    paras = client.get_paragraphs(doc_id, page=3)
    p34 = [p for p in paras if "Pembayaran Danatopup" in p["text"] and 720 <= p["rect"][1] <= 750]
    print("Tx 34 para found:", len(p34))
    if p34:
        new_desc34 = "Biaya administrasi rekening"
        client.edit_text(doc_id, page=3, paragraph=p34[0]["paragraph"], text=new_desc34)
        print("Tx 34 edited successfully.")
        
    client.doc_save(doc_id, pdf_test)
    client.doc_close(doc_id)

print("Saved test_desc_edit.pdf")
