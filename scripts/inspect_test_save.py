with open("output/test_save.pdf", "rb") as f:
    pdf_bytes = f.read()

print("File size:", len(pdf_bytes))
print("Header:", pdf_bytes[:50])
print("Tail:", pdf_bytes[-200:])
