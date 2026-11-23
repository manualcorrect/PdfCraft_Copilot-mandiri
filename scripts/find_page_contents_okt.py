import re
import zlib
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

# Let's inspect pages catalog
m_pages = re.search(rb'/Pages\s+(\d+)\s+0\s+R', pdf_bytes)
pages_oid = int(m_pages.group(1))
print("Pages root OID:", pages_oid)

# Let's find all /Type/Page
page_matches = list(re.finditer(rb'(\d+)\s+0\s+obj\s*<<(?:(?!endobj).)*?/Type\s*/Page\b(?:(?!endobj).)*?>>\s*endobj', pdf_bytes, re.DOTALL))
print("Found pages count:", len(page_matches))
for idx, pm in enumerate(page_matches):
    p_oid = int(pm.group(1))
    p_text = pm.group(0).decode('latin1', errors='ignore')
    m_contents = re.search(r'/Contents\s+(\d+)\s+0\s+R', p_text)
    m_contents_arr = re.search(r'/Contents\s*\[(.*?)\]', p_text)
    if m_contents:
        c_oid = m_contents.group(1)
        print(f"Page {idx+1} (OID {p_oid}): /Contents {c_oid}")
    elif m_contents_arr:
        c_arr = m_contents_arr.group(1)
        print(f"Page {idx+1} (OID {p_oid}): /Contents [{c_arr}]")
    else:
        print(f"Page {idx+1} (OID {p_oid}): No /Contents directly found in dict")
