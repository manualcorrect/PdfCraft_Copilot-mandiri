import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf") as pdf:
    p = pdf.pages[0]
    # Check pdfminer font objects
    res = p.page_obj.resources
    print("Resources keys:", list(res.keys()) if hasattr(res, 'keys') else res)
    fonts = res.get('Font', {}) if hasattr(res, 'get') else {}
    for obj_id, font in fonts.items():
        font_dict = font.resolve() if hasattr(font, 'resolve') else font
        print("Font object:", obj_id, font_dict.get('BaseFont'))
        print("  font_dict keys:", list(font_dict.keys()))
        df = font_dict.get('DescendantFonts')
        if df:
            df_resolved = [x.resolve() for x in df]
            print("  DescendantFonts:", df_resolved)
            for d in df_resolved:
                desc = d.get('FontDescriptor')
                if desc:
                    desc_dict = desc.resolve()
                    print("  Descriptor keys:", list(desc_dict.keys()))
                    for k in ['FontFile', 'FontFile2', 'FontFile3']:
                        if k in desc_dict:
                            print(f"  Has {k}!")
                            data = desc_dict[k].resolve().get_data()
                            print(f"  Length: {len(data)} bytes")
                            with open(f"output/{obj_id}_{k}.ttf", "wb") as f:
                                f.write(data)
                            print(f"  Saved to output/{obj_id}_{k}.ttf")
                    stream_obj = desc_dict[k].resolve()
                    data = stream_obj.get_data()
                    print(f"  Stream length: {len(data)} bytes")
                    # write out to file
                    with open(f"output/{obj_id}_{k}.ttf", "wb") as f:
                        f.write(data)
                    print(f"  Saved to output/{obj_id}_{k}.ttf")
