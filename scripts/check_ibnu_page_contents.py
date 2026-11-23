import re

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf"
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

page_matches = list(re.finditer(rb'(\d+)\s+0\s+obj\s*<<(?:(?!endobj).)*?/Type\s*/Page\b(?:(?!endobj).)*?>>\s*endobj', pdf_bytes, re.DOTALL))
print("Found pages count:", len(page_matches))
for idx, pm in enumerate(page_matches):
    p_oid = int(pm.group(1))
    p_text = pm.group(0).decode('latin1', errors='ignore')
    m_contents = re.search(r'/Contents\s+(\d+)\s+0\s+R', p_text)
    if m_contents:
        print(f"Page {idx+1} (OID {p_oid}): /Contents {m_contents.group(1)}")
