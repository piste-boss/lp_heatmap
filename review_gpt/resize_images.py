from PIL import Image
import os

# 画像のパスを指定
source_base_dir = '/Users/ishikawasuguru/review-gpt-LP'
# ファイルが見つかった assets ディレクトリ
source_dir = os.path.join(source_base_dir, 'assets')
# 出力先ディレクトリ
output_dir = '/Users/ishikawasuguru/lp_heatmap/review_gpt/output_images'

os.makedirs(output_dir, exist_ok=True)

target_files = [
    'ad_empathy_01.webp',
    'ad_pricing_01.webp',
    'ad_results_01.webp'
]

resize_specs = [
    {
        'suffix': '_landscape.png',
        'width': 1200,
        'height': 628,
        'desc': 'Landscape (1.91:1)'
    },
    {
        'suffix': '_square.png',
        'width': 1200,
        'height': 1200,
        'desc': 'Square (1:1)'
    }
]

print(f"Processing images from {source_dir}...")

processed_count = 0

for filename in target_files:
    source_path = os.path.join(source_dir, filename)
    name_without_ext = os.path.splitext(filename)[0]
    
    if not os.path.exists(source_path):
        print(f"File not found: {source_path}")
        # public フォルダも確認してみる
        alt_source_path = os.path.join(source_base_dir, 'public', filename)
        if os.path.exists(alt_source_path):
            source_path = alt_source_path
            print(f"Found in public folder: {source_path}")
        else:
            print(f"Skipping {filename}")
            continue

    try:
        with Image.open(source_path) as img:
            # WebPなども扱えるように念のためRGB変換（PNG保存時はRGBA推奨だが、Google広告は透過なしが安全な場合もある。今回はPNG指定なのでRGBAでも良いが、念の為RGBに変換して背景を白にするなどの処理は不要か？ -> 指定なしなのでそのまま）
            # ガイドラインには「透過背景は許可されない」という記述はないが、写真画像ならRGBで良いはず。
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                img = img.convert('RGBA')
            else:
                img = img.convert('RGB')
                
            for spec in resize_specs:
                target_w = spec['width']
                target_h = spec['height']
                target_ratio = target_w / target_h
                img_ratio = img.width / img.height
                
                if img_ratio > target_ratio:
                    # 画像の方が横長 -> 高さに合わせてリサイズし、左右をクロップ
                    resize_h = target_h
                    resize_w = int(resize_h * img_ratio)
                    res_img = img.resize((resize_w, resize_h), Image.LANCZOS)
                    
                    left = (resize_w - target_w) / 2
                    top = 0
                    right = left + target_w
                    bottom = target_h
                    cropped_img = res_img.crop((left, top, right, bottom))
                else:
                    # 画像の方が縦長 -> 幅に合わせてリサイズし、上下をクロップ
                    resize_w = target_w
                    resize_h = int(resize_w / img_ratio)
                    res_img = img.resize((resize_w, resize_h), Image.LANCZOS)
                    
                    left = 0
                    top = (resize_h - target_h) / 2
                    right = target_w
                    bottom = top + target_h
                    cropped_img = res_img.crop((left, top, right, bottom))
                
                output_filename = f"{name_without_ext}{spec['suffix']}"
                output_path = os.path.join(output_dir, output_filename)
                cropped_img.save(output_path, "PNG")
                print(f"Generated: {output_filename} ({spec['desc']})")
                processed_count += 1
                
    except Exception as e:
        print(f"Error processing {filename}: {e}")

print(f"Done. Processed {processed_count} images.")
