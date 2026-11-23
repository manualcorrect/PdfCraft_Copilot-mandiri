import pdfplumber
from fontTools.ttLib import TTFont
import io

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\okt\0.pdf"

with pdfplumber.open(pdf_path) as pdf:
    doc = pdf.doc
    p1 = pdf.pages[0]
    res = p1.page_obj.resources
    for k in ['R1', 'R2']:
        fobj = res['Font'][k].resolve()
        dfobj = fobj['DescendantFonts'][0].resolve()
        map_bytes = dfobj['CIDToGIDMap'].resolve().get_data()
        ff2_bytes = dfobj['FontDescriptor'].resolve()['FontFile2'].resolve().get_data()
        ttf = TTFont(io.BytesIO(ff2_bytes))
        glyphs = ttf.getGlyphOrder()
        hmtx = ttf['hmtx']
        
        # Check /W array
        w_array = dfobj.get('W', [])
        # convert w_array to dict
        w_dict = {}
        i = 0
        while i < len(w_array):
            c_first = w_array[i]
            val = w_array[i+1]
            if isinstance(val, list):
                for offset, width in enumerate(val):
                    w_dict[c_first + offset] = width
                i += 2
            else:
                c_last = val
                width = w_array[i+2]
                for cid in range(c_first, c_last + 1):
                    w_dict[cid] = width
                i += 3
        
        print(f"\nFont {k} (8 pt widths):")
        test_str = "0123456789 .,-+dariof"
        for ch in test_str:
            cid = ord(ch)
            if cid in w_dict:
                w_pt = w_dict[cid] * 8.0 / 1000.0
                source = "W array"
            else:
                gid = (map_bytes[cid*2] << 8) | map_bytes[cid*2 + 1]
                gname = glyphs[gid]
                adv = hmtx[gname][0]
                w_pt = adv * 8.0 / 1000.0
                source = "hmtx"
            print(f"  '{ch}': {w_pt:.7f} ({source})")
