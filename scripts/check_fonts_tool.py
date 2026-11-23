import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

ref3_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf"

with PdfCraftClient() as client:
    doc_id = client.doc_open(ref3_path)
    info = client.doc_info(doc_id)
    print("Doc info pages:", info.get("pages"))
    fonts_res = client.call_tool("text_fonts", {"doc": doc_id, "page": 1})
    print("Fonts:", fonts_res)
    client.doc_close(doc_id)
