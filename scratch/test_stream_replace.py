import zlib, shutil

src = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf"
dst = r"scratch/test_stream_replace.pdf"
shutil.copyfile(src, dst)

with open(dst, "rb") as f:
    pdf_bytes = f.read()

# Let's find all streams in pdf_bytes
# A stream is: b"stream\r\n" ... b"endstream" or b"stream\n" ... b"endstream"
# We can decompress each stream, search for target bytes, replace, recompress, and rebuild!

target_old = '6.091.988,81'.encode('utf-16-be')
target_new = '7.815.988,81'.encode('utf-16-be')

print("target_old:", target_old)
print("target_new:", target_new)

# Let's check how many times target_old appears across all streams
pos = 0
found_streams = []
while True:
    s_idx = pdf_bytes.find(b"stream", pos)
    if s_idx == -1: break
    # find newline after stream
    data_start = s_idx + 6
    if pdf_bytes[data_start:data_start+2] == b"\r\n":
        data_start += 2
    elif pdf_bytes[data_start:data_start+1] == b"\n":
        data_start += 1
        
    e_idx = pdf_bytes.find(b"endstream", data_start)
    if e_idx == -1: break
    stream_data = pdf_bytes[data_start:e_idx]
    if stream_data.endswith(b"\r\n"):
        stream_data = stream_data[:-2]
    elif stream_data.endswith(b"\n"):
        stream_data = stream_data[:-1]
        
    try:
        decomp = zlib.decompress(stream_data)
        if target_old in decomp:
            print(f"Found target_old in stream starting at {s_idx}!")
            found_streams.append((s_idx, data_start, e_idx, decomp))
    except:
        pass
    pos = e_idx + 9

print(f"Total matching streams found: {len(found_streams)}")
