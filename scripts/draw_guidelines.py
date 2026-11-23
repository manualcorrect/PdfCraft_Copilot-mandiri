from PIL import Image, ImageDraw

brain_dir = r'C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098'

def add_guidelines(img_path, out_path):
    img = Image.open(img_path).convert('RGB')
    draw = ImageDraw.Draw(img)
    w, h = img.size
    
    # In 300 dpi, 1 pt = 300/72 = 4.1667 pixels.
    # Crop box was (280, 160, 580, 260)
    # y = 160 is top = 0 px.
    # Row 1: baseline y_top = 175.0 pt -> (175.0 - 160) * 300/72 = 62.5 px
    # Row 2: baseline y_top = 198.0 pt -> (198.0 - 160) * 300/72 = 158.33 px
    # Row 3: baseline y_top = 221.0 pt -> (221.0 - 160) * 300/72 = 254.17 px
    # Row 4: baseline y_top = 245.0 pt -> (245.0 - 160) * 300/72 = 354.17 px
    
    scale = 300.0 / 72.0
    baselines = [
        (175.0 - 160.0) * scale,
        (198.0 - 160.0) * scale,
        (221.0 - 160.0) * scale,
        (245.0 - 160.0) * scale
    ]
    
    for y_px in baselines:
        draw.line([(0, int(round(y_px))), (w, int(round(y_px)))], fill=(255, 0, 0), width=1)
        
    img.save(out_path)
    print(f"Saved {out_path}")

add_guidelines(f"{brain_dir}/sb_crop_ref.png", f"{brain_dir}/guideline_ref.png")
add_guidelines(f"{brain_dir}/sb_crop_old_aug.png", f"{brain_dir}/guideline_old_aug.png")
add_guidelines(f"{brain_dir}/sb_crop_new_aug.png", f"{brain_dir}/guideline_new_aug.png")
