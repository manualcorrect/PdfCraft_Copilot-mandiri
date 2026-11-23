import sys
sys.path.insert(0, "src")
import shutil
import base64
from pdfcraft_client import PdfCraftClient
from PIL import Image
import pdfplumber

test_pdf = "output/test_acc_shift.pdf"
shutil.copyfile(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf", test_pdf)

with PdfCraftClient() as client:
    doc = client.doc_open(test_pdf)
    paras = client.get_paragraphs(doc, page=1)
    
    p_acc = [p for p in paras if "1650003584860" in p["text"] or "1660003584860" in p["text"]][0]
    print("Found p_acc:", p_acc)
    
    # Edit text
    client.edit_text(doc, page=1, paragraph=p_acc["paragraph"], text="1630016287487")
    
    # Check its updated position
    up = [p for p in client.get_paragraphs(doc, page=1) if p["paragraph"] == p_acc["paragraph"]][0]
    print("Updated rect before dx:", up["rect"])
    dx = 160.0 - up["rect"][0]
    print("Calculated dx:", dx)
    if abs(dx) > 0.05:
        client.edit_text(doc, page=1, paragraph=p_acc["paragraph"], dx=dx)
        up2 = [p for p in client.get_paragraphs(doc, page=1) if p["paragraph"] == p_acc["paragraph"]][0]
        print("Updated rect after dx:", up2["rect"])

    client.doc_save(doc, path=test_pdf, full=True)
    
    # Render preview
    res = client.call_tool("page_render", {"doc": doc, "page": 1, "dpi": 150})
    b64_data = res["content"][0]["data"]
    with open("output/test_acc_shift.png", "wb") as f:
        f.write(base64.b64decode(b64_data))
    client.doc_close(doc)

with pdfplumber.open(test_pdf) as pdf:
    print("\n=== Result chars ===")
    for c in pdf.pages[0].chars:
        if 140 <= c["x0"] <= 230 and abs(c["top"] - 190) < 5:
            print(f"Char: {repr(c['text']):5s} x0={c['x0']:.1f}")

im = Image.open("output/test_acc_shift.png")
w, h = im.size
# crop account number area
crop = im.crop((0, int(h * 0.2), int(w * 0.5), int(h * 0.35)))
crop.save("C:/Users/Wisnu/.gemini/antigravity/brain/5e8306ab-a513-43f6-bf81-265c0e523098/acc_num_crop.png")
print("Saved acc_num_crop.png!")
