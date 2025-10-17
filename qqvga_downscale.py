from PIL import Image, ImageFilter, ImageEnhance
import os

# ----- CONFIG -----
input_folder = "Phone"          # Folder with your original images
output_folder = "QQVGA"         # Output folder
target_resolution = (120, 160)  # QQVGA resolution (note: width x height)
sharpen_amount = 1.3            # 1.0 = normal, 1.5 = extra sharp
# ------------------

os.makedirs(output_folder, exist_ok=True)
extensions = (".png", ".jpg", ".jpeg")

target_w, target_h = target_resolution

for filename in os.listdir(input_folder):
    if filename.lower().endswith(extensions):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        img = Image.open(input_path)
        src_w, src_h = img.size

        # Step 1: maintain aspect ratio (scale to fill)
        scale = max(target_w / src_w, target_h / src_h)
        new_w = int(src_w * scale)
        new_h = int(src_h * scale)
        img_resized = img.resize((new_w, new_h), Image.BICUBIC)

        # Step 2: crop to target size (centered)
        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 2
        right = left + target_w
        bottom = top + target_h
        img_cropped = img_resized.crop((left, top, right, bottom))

        # Step 3: sharpen + enhance
        img_cropped = img_cropped.filter(ImageFilter.SHARPEN)
        enhancer = ImageEnhance.Sharpness(img_cropped)
        img_final = enhancer.enhance(sharpen_amount)

        # Step 4: save
        img_final = img_final.convert("RGB")
        img_final.save(output_path, quality=95)

        print(f"Processed {filename}: scaled to {new_w}x{new_h}, cropped & sharpened → {target_w}x{target_h}")

print("✅ All images resized, cropped, and sharpened for QQVGA output!")
