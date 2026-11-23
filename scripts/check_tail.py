with open('output/REK_KEISYA_AUG_OUTPUT_1.pdf', 'rb') as f:
    pdf_data = f.read()

print("File size:", len(pdf_data))
print("Last 1000 bytes:")
print(pdf_data[-1000:])
