import pdfplumber

with pdfplumber.open('output/REK_IBNU_SEP_OUTPUT_1.pdf') as pdf:
    doc = pdf.doc
    r1 = doc.getobj(111)
    print("R1:", r1)
    desc = r1['DescendantFonts'][0].resolve()
    print("DescendantFont:", desc)
    if 'W' in desc:
        print("W array:", desc['W'])
    if 'DW' in desc:
        print("DW:", desc['DW'])
