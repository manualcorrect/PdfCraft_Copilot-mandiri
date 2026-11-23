with open('output/test_aug_perfect_sb.pdf', 'rb') as f:
    data = f.read()

print("File size:", len(data))
print("Searching for '552 0 obj':", data.find(b'552 0 obj'))
print("Searching for '553 0 obj':", data.find(b'553 0 obj'))
print("Last 500 bytes:\n", data[-500:])
