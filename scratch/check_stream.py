from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTTextLine

for page_layout in extract_pages(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf", page_numbers=[2]):
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            text = element.get_text()
            if '6.091.988,81' in text:
                print("Element bbox:", element.bbox)
                for text_line in element:
                    print("  Line bbox:", text_line.bbox, "text:", repr(text_line.get_text()))
                    for c in text_line:
                        if isinstance(c, LTChar):
                            print(f"    Char '{c.get_text()}' at ({c.x0:.2f}, {c.y0:.2f})")
