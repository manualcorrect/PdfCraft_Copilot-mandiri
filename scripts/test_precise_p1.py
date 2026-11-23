import os
import sys
import shutil

sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient
import pdfplumber

src_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_SEP_2026.pdf"
test_pdf = "output/test_sep_align.pdf"
shutil.copyfile(src_pdf, test_pdf)

with PdfCraftClient() as client:
    doc_id = client.doc_open(test_pdf)
    
    # Row 1: p41
    print("Editing Row 1 (p41)...")
    client.edit_text(doc_id, page=1, paragraph=41, text="Penarikan tunai di ATM\nBANK MANDIRI SRG IM CIRUAS 01", width=180.0, line_spacing=1.25)
    up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == 41][0]
    print(f"After text edit: rect={up['rect']}")
    # row_y = 343.92, 2 lines -> ideal top = 338.92
    dx = 124.00 - up["rect"][0]
    dy = 338.92 - up["rect"][1]
    print(f"Applying dx={dx:.2f}, dy={dy:.2f}")
    client.edit_text(doc_id, page=1, paragraph=41, dx=dx, dy=dy)
    up2 = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == 41][0]
    print(f"After shift: rect={up2['rect']}")

    # Row 2: In REK_GALANG_SEP_2026.pdf, p42 is "Transfer BI Fast Dari BCA INDRA MIDIAN 2452372917", p43 is "-", p49 is "Ke BCA DEBORA DIAN FITRESIA 2453460819"
    # Empty p43 and p49!
    print("Emptying p43 and p49 in Row 2...")
    client.edit_text(doc_id, page=1, paragraph=43, text="")
    client.edit_text(doc_id, page=1, paragraph=49, text="")
    # Now edit p42
    desc_r2 = "Transfer BI Fast\nDari BCA\nINDRA MIDIAN 2452372917\n-"
    # 4 lines -> ideal top = 389.92 - 15.0 = 374.92
    client.edit_text(doc_id, page=1, paragraph=42, text=desc_r2, width=150.0, line_spacing=1.25)
    up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == 42][0]
    dx = 124.00 - up["rect"][0]
    dy = 374.92 - up["rect"][1]
    client.edit_text(doc_id, page=1, paragraph=42, dx=dx, dy=dy)
    up2 = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == 42][0]
    print(f"Row 2 after shift: rect={up2['rect']}")

    # Row 3: In REK_GALANG_SEP_2026.pdf:
    # p55 is: rect=[124.0, 435.92, 187.72, 453.92], text='Biaya administrasi kartu debit'
    print("Row 3 p55:", [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == 55][0])
    
    # Row 5: p67 is: "Transfer BI Fast Ke BCA KARINA AMALIA DARMAW 2452998221 Jangan kapok yah Na Thank you"
    desc_r5 = "Transfer BI Fast\nKe BCA\nKARINA AMALIA DARMAW 2452998221\n-"
    client.edit_text(doc_id, page=1, paragraph=67, text=desc_r5, width=200.0, line_spacing=1.25)
    up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == 67][0]
    dx = 124.00 - up["rect"][0]
    dy = (527.92 - 15.0) - up["rect"][1]
    client.edit_text(doc_id, page=1, paragraph=67, dx=dx, dy=dy)
    
    # Row 7: p79 is: "Transfer BI Fast Ke SEABANK INDONESIA MARWA ARSYIVA 901159417428 MAKASIH YA WA"
    desc_r7 = "Transfer BI Fast\nKe SEABANK INDONESIA\nMARWA ARSYIVA 901159417428\n-"
    client.edit_text(doc_id, page=1, paragraph=79, text=desc_r7, width=180.0, line_spacing=1.25)
    up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == 79][0]
    dx = 124.00 - up["rect"][0]
    dy = (619.92 - 15.0) - up["rect"][1]
    client.edit_text(doc_id, page=1, paragraph=79, dx=dx, dy=dy)

    client.doc_save(doc_id, path=test_pdf, full=True)
    client.doc_close(doc_id)

print("\n--- Telemetry on test_sep_align.pdf Page 1 ---")
with pdfplumber.open(test_pdf) as pdf:
    for c in pdf.pages[0].chars:
        if c['text'] == 'P' and c['top'] > 330 and c['top'] < 360 and c['x0'] > 120:
            print(f"Row 1 'P': x0={c['x0']:.2f}, top={c['top']:.2f}, font={c['fontname']}")
