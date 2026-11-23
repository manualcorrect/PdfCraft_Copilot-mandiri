import re

def check_xref_info(pdf_path, name):
    with open(pdf_path, 'rb') as f:
        data = f.read()
    
    print(f"\n================ {name} ================")
    # find startxref
    sx_m = re.findall(rb'startxref[\r\n]+(\d+)', data)
    print("startxref:", sx_m)
    
    # find xref stream object
    m_xref = re.search(rb'(\d+)\s+0\s+obj\s*<<([^>]*/Type\s*/XRef[^>]*)>>', data)
    if m_xref:
        print(f"XRef stream object: {m_xref.group(1).decode()}")
    else:
        print("Traditional xref table?")
        m_trad = re.search(rb'xref\r?\n', data)
        if m_trad:
            print("Found traditional xref at offset", m_trad.start())

check_xref_info('output/REK_KEISYA_AUG_OUTPUT_1.pdf', 'AUG')
check_xref_info('output/REK_KEISYA_SEP_OUTPUT_1.pdf', 'SEP')
check_xref_info('output/REK_KEISYA_OKT_OUTPUT_1.pdf', 'OKT')
