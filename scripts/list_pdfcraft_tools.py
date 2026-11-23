import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient

with PdfCraftClient() as client:
    res = client._send_request("tools/list", {})
    tools = res.get("result", {}).get("tools", [])
    print(f"Total tools: {len(tools)}")
    for t in tools:
        print(f"  {t['name']}: {t.get('description', '')[:80]}")
