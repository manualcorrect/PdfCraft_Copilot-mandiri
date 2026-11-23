import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_path)
    
    # Tx 10: Page 1, Row 10 (y~757.9)
    paras_p1 = client.get_paragraphs(doc_id, page=1)
    p_tx10 = [p for p in paras_p1 if abs(p["rect"][1] - 757.9) < 15 and 370 <= p["rect"][0] <= 450]
    print(f"Tx 10 nominal: {p_tx10[0] if p_tx10 else 'NOT FOUND'}")
    
    # Tx 37: Page 4, Row 3 (y~319.9)
    paras_p4 = client.get_paragraphs(doc_id, page=4)
    p_tx37 = [p for p in paras_p4 if abs(p["rect"][1] - 319.9) < 15 and 370 <= p["rect"][0] <= 450]
    print(f"Tx 37 nominal: {p_tx37[0] if p_tx37 else 'NOT FOUND'}")

    # Tx 50: Page 5, Row 4 (y~365.9)
    paras_p5 = client.get_paragraphs(doc_id, page=5)
    p_tx50 = [p for p in paras_p5 if abs(p["rect"][1] - 365.9) < 15 and 370 <= p["rect"][0] <= 450]
    print(f"Tx 50 nominal: {p_tx50[0] if p_tx50 else 'NOT FOUND'}")
