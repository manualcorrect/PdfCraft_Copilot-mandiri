with open('output/REK_KEISYA_AUG_OUTPUT_1.pdf', 'rb') as f:
    data = f.read()

print("Offset 40282:")
print(data[40282:40282+500])
