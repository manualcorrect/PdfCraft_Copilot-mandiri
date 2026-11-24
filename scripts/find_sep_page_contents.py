import re, zlib, pdfplumber

with open('output/test_sep_p3.pdf', 'rb') as f:
    data = f.read()

# Find all Page objects
page_objs = list(re.finditer(rb'(\d+)\s+0\s+obj\s*<<(.*?)>>\s*endobj', data, re.DOTALL))
for m in page_objs:
    oid = int(m.group(1))
    d = m.group(2)
    if b'/Type /Page\b' in d or b'/Type/Page\b' in d:
        m_c = re.search(rb'/Contents\s+(\d+)\s+0\s+R', d)
        c_oid = m_c.group(1).decode() if m_c else 'NO_CONTENTS'
        print(f"Page OID {oid} -> Contents OID {c_oid}")
