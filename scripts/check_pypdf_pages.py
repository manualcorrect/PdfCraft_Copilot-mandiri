import pypdf

reader = pypdf.PdfReader('output/test_sep_p3.pdf')
print("Total pages:", len(reader.pages))
for p_idx, page in enumerate(reader.pages):
    contents = page.get_contents()
    if isinstance(contents, pypdf.generic.ArrayObject):
        c_oids = [c.indirect_reference.id for c in contents]
        print(f"Page {p_idx+1}: Array of contents: {c_oids}")
    elif hasattr(contents, 'indirect_reference'):
        print(f"Page {p_idx+1}: Contents OID {contents.indirect_reference.id}")
    else:
        print(f"Page {p_idx+1}: {contents}")
