import os

sep_dir = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP"
oct_dir = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT"

for d_name, d_path in [("SEP", sep_dir), ("OCT", oct_dir)]:
    print(f"\n==================== {d_name} DIRECTORY ====================")
    if os.path.exists(d_path):
        for f in os.listdir(d_path):
            full_p = os.path.join(d_path, f)
            size_kb = os.path.getsize(full_p) / 1024
            print(f"  {f:40} ({size_kb:.1f} KB)")
    else:
        print(f"  Directory not found: {d_path}")
