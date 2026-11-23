import sys
sys.path.insert(0, "src")
import base64
from pdfcraft_client import PdfCraftClient
from PIL import Image

with PdfCraftClient() as client:
    doc = client.doc_open("output/REK_GALANG_OCT_2026_CHRONOLOGICAL.pdf")
    for p in range(1, 4):
        res = client.call_tool("page_render", {"doc": doc, "page": p, "dpi": 150})
        b64_data = res["content"][0]["data"]
        raw_path = f"output/oct_rendered_p{p}.png"
        with open(raw_path, "wb") as f:
            f.write(base64.b64decode(b64_data))
        im = Image.open(raw_path)
        w, h = im.size
        # crop top half
        crop = im.crop((0, 0, w, int(h * 0.6)))
        crop.save(f"C:/Users/Wisnu/.gemini/antigravity/brain/5e8306ab-a513-43f6-bf81-265c0e523098/oct_preview_p{p}.png")
        print(f"Saved P{p} preview to brain!")
    client.doc_close(doc)
