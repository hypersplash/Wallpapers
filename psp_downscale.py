from PIL import Image, UnidentifiedImageError
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# ----- CONFIG -----
input_folder = "Computer"
output_folder = "PSP"
target_resolution = (480, 272)
max_workers = 4  # Adjust based on your CPU cores
# ------------------

os.makedirs(output_folder, exist_ok=True)
extensions = (".png", ".jpg", ".jpeg")
target_w, target_h = target_resolution

def process_image(filename):
    """Process a single image - designed for parallel execution"""
    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)

    try:
        with Image.open(input_path) as img:
            img.load()
            src_w, src_h = img.size

            # Scale to fill
            scale = max(target_w / src_w, target_h / src_h)
            new_w = int(src_w * scale)
            new_h = int(src_h * scale)

            # Use LANCZOS for quality, BILINEAR for speed
            img_resized = img.resize((new_w, new_h), Image.LANCZOS)

            # Centered crop
            left = (new_w - target_w) // 2
            top = (new_h - target_h) // 2
            img_cropped = img_resized.crop((left, top, left + target_w, top + target_h))

            # Save with optimization
            img_cropped.save(output_path, optimize=True, quality=85)

        return f"✅ Processed {filename}: {new_w}x{new_h} → {target_w}x{target_h}"

    except (OSError, UnidentifiedImageError) as e:
        return f"⚠ Skipped {filename}: {e}"

# Get all image files
image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(extensions)]

# Process in parallel
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    results = executor.map(process_image, image_files)
    for result in results:
        print(result)

print("🎉 All readable images processed for PSP!")
