import zlib
import re

def inspect_p1_stream(pdf_path, name, contents_oid):
    with open(pdf_path, 'rb') as f:
        data = f.read()
    
    pat = re.compile(rb'\b' + str(contents_oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', re.DOTALL)
    m = pat.search(data)
    assert m, f"Obj {contents_oid} not found in {name}"
    
    decomp = zlib.decompress(m.group(2)).decode('latin1', errors='ignore')
    print(f"\n================ {name} (Obj {contents_oid}, len={len(decomp)}) ================")
    
    # Check for Colons & Labels (Block 1)
    pos_c1 = decomp.find('446.12 667 cm')
    pos_c4 = decomp.find('446.12 597 cm')
    start_b1 = decomp.rfind('q', 0, pos_c1)
    end_b1 = decomp.find('Q', pos_c4) + 1
    print(f"Block 1: {start_b1} to {end_b1}")
    print("Block 1 snippet:", repr(decomp[start_b1:start_b1+150]))
    
    # Check for Values (Block 2)
    pos_vals = decomp.find('505.96 667 cm')
    if pos_vals == -1:
        # maybe different x?
        pos_vals = decomp.find('667 cm')
        print(f"Alternative pos_vals: {pos_vals}")
    start_b2 = decomp.rfind('q', 0, pos_vals)
    pos_now = decomp.find('16 676 cm')
    end_b2 = decomp.rfind('q', 0, pos_now)
    print(f"Block 2: {start_b2} to {end_b2}")
    print("Block 2 snippet:", repr(decomp[start_b2:start_b2+150]))

inspect_p1_stream('output/REK_KEISYA_AUG_OUTPUT_1.pdf', 'AUG', 11)
inspect_p1_stream('output/REK_KEISYA_SEP_OUTPUT_1.pdf', 'SEP', 10)
inspect_p1_stream('output/REK_KEISYA_OKT_OUTPUT_1.pdf', 'OKT', 12)
