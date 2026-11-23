import zlib

with open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf", "rb") as f:
    data = f.read()

# Find objects with stream
streams = []
pos = 0
while True:
    idx = data.find(b"stream", pos)
    if idx == -1: break
    end_idx = data.find(b"endstream", idx)
    if end_idx == -1: break
    stream_bytes = data[idx+6:end_idx].strip()
    try:
        decomp = zlib.decompress(stream_bytes)
        if b"6.091.988,81" in decomp:
            print("Found 6.091.988,81 in decompressed stream at idx", idx)
            # print surrounding
            loc = decomp.find(b"6.091.988,81")
            print("Surrounding:", decomp[max(0, loc-100):loc+150])
    except:
        if b"6.091.988,81" in stream_bytes:
            print("Found in uncompressed stream!")
    pos = end_idx + 9
