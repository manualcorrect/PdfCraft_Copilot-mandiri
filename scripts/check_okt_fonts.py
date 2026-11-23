import pdfplumber
import zlib
import re
from fontTools.ttLib import TTFont
import io

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\okt\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

print(f"Read 0.pdf: {len(pdf_bytes)} bytes")

# Find all fonts via pdfplumber
with pdfplumber.open(pdf_path) as pdf:
    doc = pdf.doc
    p1 = pdf.pages[0]
    res = p1.page_obj.resources
    print("Page 1 Fonts:", res.get('Font'))
    for k, v in res.get('Font', {}).items():
        fobj = v.resolve()
        basefont = fobj.get('BaseFont')
        print(f"\nFont {k}: {basefont}")
        for df in fobj.get('DescendantFonts', []):
            dfobj = df.resolve()
            df_base = dfobj.get('BaseFont')
            print(f"  Descendant: {df_base}")
            w = dfobj.get('W', [])
            print(f"  W entries: {len(w)}")
            # Check CIDToGIDMap
            map_ref = dfobj.get('CIDToGIDMap')
            print(f"  CIDToGIDMap: {map_ref}")
            # Check FontDescriptor -> FontFile2
            fdesc = dfobj.get('FontDescriptor').resolve()
            ff2_ref = fdesc.get('FontFile2')
            print(f"  FontFile2: {ff2_ref}")
            if ff2_ref:
                ff2_obj = ff2_ref.resolve()
                stream = ff2_obj.get_data()
                ttf = TTFont(io.BytesIO(stream))
                glyphs = ttf.getGlyphOrder()
                print(f"  TTF glyph count: {len(glyphs)}")
                # Check characters: 'c', 'I', 'b', 'n', 'u', 'A', 'g', 'O', 'k', 't', 'S', 'e', 'r', 'a'
                check_chars = "IBNU AGUN KCP Serang Ciceri 01 Oct 2026 - 31 Oct 2026"
                print(f"  Testing characters for {k}...")
                # Check CIDToGIDMap stream
                map_obj = map_ref.resolve()
                map_bytes = map_obj.get_data()
                missing = []
                for ch in check_chars:
                    cid = ord(ch)
                    gid = (map_bytes[cid*2] << 8) | map_bytes[cid*2 + 1]
                    if gid >= len(glyphs):
                        missing.append((ch, f"gid={gid} >= len={len(glyphs)}"))
                    else:
                        gname = glyphs[gid]
                        num_contours = ttf['glyf'][gname].numberOfContours
                        if num_contours == 0 and ch != ' ':
                            missing.append((ch, f"gid={gid} ({gname}) has 0 contours"))
                if missing:
                    print(f"  WARNING: Missing/empty glyphs in {k}: {missing}")
                else:
                    print(f"  SUCCESS: All characters in '{check_chars}' have valid glyphs in {k}!")
