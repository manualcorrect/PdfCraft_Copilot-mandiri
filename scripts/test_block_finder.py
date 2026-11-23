import zlib
import re

def find_blocks(pdf_path, name, contents_oid):
    with open(pdf_path, 'rb') as f:
        data = f.read()
    
    pat = re.compile(rb'\b' + str(contents_oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', re.DOTALL)
    m = pat.search(data)
    decomp = zlib.decompress(m.group(2)).decode('latin1', errors='ignore')
    
    # 1. Block 1 (Colons & Labels)
    # Starts before '446.12 667 cm'
    pos_c1 = decomp.find('446.12 667 cm')
    start_b1 = decomp.rfind('q', 0, pos_c1)
    # Ends after '446.12 597 cm' ET Q
    pos_c4 = decomp.find('446.12 597 cm')
    end_b1 = decomp.find('ET Q', pos_c4) + 4
    
    # 2. Block 2 (Values)
    # Ends before '16 676 cm'
    pos_now = decomp.find('16 676 cm')
    end_b2 = decomp.rfind('q', 0, pos_now)
    # Starts before the first value around 667 cm
    # Search backwards from end_b2 for the start of the summary value chain
    # It starts with 'q 1 0 0 1 <x> 667 cm'
    val_m = re.search(r'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+667\s+cm', decomp[:end_b2])
    # The last occurrence before end_b2 that is past end_b1:
    matches = list(re.finditer(r'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+667\s+cm', decomp[end_b1:end_b2]))
    assert matches, f"Value start not found in {name}"
    start_b2 = end_b1 + matches[-1].start()
    
    print(f"\n{name}:")
    print(f"  Block 1: [{start_b1}:{end_b1}] len={end_b1-start_b1}")
    print(f"  Block 2: [{start_b2}:{end_b2}] len={end_b2-start_b2}")
    print(f"  Snippet between B1 and B2: {repr(decomp[end_b1:end_b1+100])}")
    print(f"  Start of B2: {repr(decomp[start_b2:start_b2+80])}")
    print(f"  End of B2: {repr(decomp[end_b2-50:end_b2])}")

find_blocks('output/REK_KEISYA_AUG_OUTPUT_1.pdf', 'AUG', 11)
find_blocks('output/REK_KEISYA_SEP_OUTPUT_1.pdf', 'SEP', 10)
find_blocks('output/REK_KEISYA_OKT_OUTPUT_1.pdf', 'OKT', 12)
