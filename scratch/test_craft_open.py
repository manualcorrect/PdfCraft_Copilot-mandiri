import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

client = PdfCraftClient()
try:
    doc_id = client.doc_open(r"scratch/test_replaced_stream.pdf")
    print("Opened successfully! doc_id:", doc_id)
    # save to scratch/test_repaired.pdf
    client.doc_save(doc_id, path=r"scratch/test_repaired.pdf")
    client.doc_close(doc_id)
    print("Repaired and saved!")
except Exception as e:
    print("Error:", e)
