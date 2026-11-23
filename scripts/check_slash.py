import pdfplumber
from fontTools.ttLib import TTFont
import io

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\okt\0.pdf"

with pdfplumber.open(pdf_path) as pdf:
    doc = pdf.doc
    p1 = pdf.pages[0]
    res = p1.page_obj.resources
    for k in ['R1', 'R2', 'R3']:
        fobj = res['Font'][k].resolve()
        dfobj = fobj['DescendantFonts'][0].resolve()
        map_bytes = dfobj['CIDToGIDMap'].resolve().get_data()
        ff2_bytes = dfobj['FontDescriptor'].resolve()['FontFile2'].resolve().get_data()
        ttf = TTFont(io.BytesIO(ff2_bytes))
        glyphs = ttf.getGlyphOrder()
        
        cid = ord('/')
        gid = (map_bytes[cid*2] << 8) | map_bytes[cid*2 + 1]
        print(f"Font {k}: '/' (CID 47) -> GID {gid}")
        if gid < len(glyphs):
            gname = glyphs[gid]
            cnt = ttf['glyf'][gname].numberOfContours
            print(f"  Glyph: {gname}, Contours: {cnt}")
        else:
            print("  Out of range!")
