import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(pdf_path)
    for p_num in range(1, 6):
        paras = client.get_paragraphs(doc_id, page=p_num)
        base_y = 343.92 if p_num == 1 else 227.92
        num_rows = 10 if p_num == 1 else (4 if p_num == 5 else 12)
        print(f"\n--- Page {p_num} ({num_rows} rows) ---")
        for r_i in range(num_rows):
            row_y = base_y + r_i * 46.00
            p_date = [p for p in paras if abs(p["rect"][1] - (row_y - 4.0)) < 10 and 45 <= p["rect"][0] <= 85 and "WIB" not in p["text"]]
            p_time = [p for p in paras if abs(p["rect"][1] - (row_y + 5.0)) < 10 and 45 <= p["rect"][0] <= 85 and "WIB" in p["text"]]
            d_str = p_date[0]["text"] if p_date else "NOT FOUND"
            t_str = p_time[0]["text"] if p_time else "NOT FOUND"
            print(f"  Row {r_i+1:2d} (expected y~{row_y:.1f}): Date='{d_str}' Time='{t_str}'")
