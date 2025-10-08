from PIL import Image, ImageFilter, ImageEnhance
import os

# ----- CONFIG -----
input_folder = "Phone"
output_folder = "QQVGA"
target_resolution = (120, 160)
sharpen_amount = 1.3  # 1.0 = normal, 1.5 = extra sharp
# ------------------

os.makedirs(output_folder, exist_ok=True)
extensions = (".png", ".jpg", ".jpeg")

for filename in os.listdir(input_folder):
    if filename.lower().endswith(extensions):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        img = Image.open(input_path)
        orig_w, orig_h = img.size
        target_w, target_h = target_resolution
        orig_ratio = orig_w / orig_h
        target_ratio = target_w / target_h

        # Scale to fill (only once)
        if orig_ratio > target_ratio:
            new_h = target_h
            new_w = int(new_h * orig_ratio)
        else:
            new_w = target_w
            new_h = int(new_w / orig_ratio)

        img = img.resize((new_w, new_h), Image.BICUBIC)

        # Center crop
        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 2
        img = img.crop((left, top, left + target_w, top + target_h))

        # Optional: slight sharpening
        img = img.filter(ImageFilter.SHARPEN)
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(sharpen_amount)

        # Save final image
        img = img.convert("RGB")
        img.save(output_path, quality=95)
        print(f"Downscaled + sharpened {filename} → {target_resolution}")

print("✅ All images crisped up and saved to 'QQVGA'!")
