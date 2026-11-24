import re
import zlib

pdf_path = r'c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\test_p46.pdf'
with open(pdf_path, 'rb') as f:
    pdf_bytes = f.read()

page_content_oids = {1: 10, 2: 112, 3: 211, 4: 310}

for p_num, oid in page_content_oids.items():
    m_obj = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream(\r\n|\n)', pdf_bytes)
    dict_data = m_obj.group(1)
    m_len = re.search(rb'/Length\s+(\d+)', dict_data)
    length = int(m_len.group(1))
    stream_start = m_obj.end()
    stream_data = pdf_bytes[stream_start : stream_start + length]
    decomp = zlib.decompress(stream_data)
    
    # check row_pattern
    row_pattern = re.compile(
        rb'(q\s+1\s+0\s+0\s+1\s+(?:19\.\d+|20(?:\.0+)?)\s+([\d\.]+)\s+cm\s+BT\s+0\s+0\s+0\s+rg/R1\s+8\s+Tf(/R\d+\s+gs).*?0\.07451\s+0\.294118\s+0\.729412\s+rg/R2\s+8\s+Tf.*?ET\s+Q)',
        re.DOTALL
    )
    row_matches = list(row_pattern.finditer(decomp))
    
    # check page num matches
    m_it = re.search(rb'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+726\s+cm\s+BT\s+0\s+0\s+0\s+rg/R3\s+8\s+Tf(/R\d+\s+gs).*?ET\s+Q', decomp, re.DOTALL)
    bold_blocks = list(re.finditer(rb'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+736\s+cm\s+BT\s+0\s+0\s+0\s+rg/R2\s+8\s+Tf(/R\d+\s+gs).*?ET\s+Q', decomp, re.DOTALL))
    
    print(f"Page {p_num} (OID {oid}): {len(row_matches)} rows found | Italic pagenum: {m_it is not None} | Bold pagenum: {len(bold_blocks)}")
