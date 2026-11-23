import zlib
import re

def inspect_p1_fonts(pdf_path, name):
    with open(pdf_path, 'rb') as f:
        data = f.read()
    
    print(f"\n================ {name} ================")
    # find page 1 object
    p1_m = re.search(rb'(\d+)\s+\d+\s+obj\s*<<[^>]*?/Type\s*/Page.*?>>', data, re.DOTALL)
    if not p1_m:
        print("Page 1 obj not found!")
        return
    p1_dict = p1_m.group(0).decode('latin1', errors='ignore')
    print("Page 1 dict:", p1_dict[:400])
    
    # Find Contents object ID
    c_m = re.search(r'/Contents\s+(\d+)\s+\d+\s+R', p1_dict)
    if c_m:
        cid = c_m.group(1)
        print(f"Contents ID: {cid}")
        # find contents object
        c_obj = re.search(rb'' + cid.encode() + rb'\s+\d+\s+obj\s*<<(.*?)>>\s*stream\r?\n(.*?)endstream', data, re.DOTALL)
        if c_obj:
            stream_data = zlib.decompress(c_obj.group(2))
            stext = stream_data.decode('latin1', errors='ignore')
            print(f"Stream len: {len(stext)}")
            # find what font names are used in stream
            fonts_used = set(re.findall(r'(/F\w+|/R\w+)\s+\d+(?:\.\d+)?\s+Tf', stext))
            print("Fonts used in stream:", fonts_used)

inspect_p1_fonts('output/REK_KEISYA_AUG_OUTPUT_1.pdf', 'AUG')
inspect_p1_fonts('output/REK_KEISYA_SEP_OUTPUT_1.pdf', 'SEP')
inspect_p1_fonts('output/REK_KEISYA_OKT_OUTPUT_1.pdf', 'OKT')
