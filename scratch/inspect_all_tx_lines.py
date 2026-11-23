import sys
sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient

client = PdfCraftClient()
doc_id = client.doc_open(r'scratch/test_copy.pdf')

for p in range(1, 6):
    res = client.call_tool("text_lines", {"doc": doc_id, "page": p})
    lines = res.get('lines', [])
    min_y = 315 if p == 1 else 200
    tx_lines = [l for l in lines if l['rect'][1] >= min_y and l['rect'][1] <= 800]
    print(f"=== PAGE {p} tx_lines count: {len(tx_lines)} ===")
    # Find WIB lines
    wib_lines = [l for l in tx_lines if 'WIB' in l.get('text', '')]
    print(f"  WIB lines count: {len(wib_lines)}")
    # Find Date lines (contains 'Mar 2026' or 'Aug 2026')
    date_lines = [l for l in tx_lines if '2026' in l.get('text', '') and 'WIB' not in l.get('text', '')]
    print(f"  Date lines count: {len(date_lines)}")

client.doc_close(doc_id, discard_changes=True)
