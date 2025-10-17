from PIL import Image
import os

# ----- CONFIG -----
input_folder = "Computer"      # Folder with your original images
output_folder = "PSP"          # PSP output folder in the current directory
target_resolution = (480, 272) # PSP screen resolution
# ------------------

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Supported extensions
extensions = (".png", ".jpg", ".jpeg")

target_w, target_h = target_resolution

for filename in os.listdir(input_folder):
    if filename.lower().endswith(extensions):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # Open image
        img = Image.open(input_path)
        src_w, src_h = img.size

        # Step 1: maintain aspect ratio (scale to fill)
        scale = max(target_w / src_w, target_h / src_h)
        new_w = int(src_w * scale)
        new_h = int(src_h * scale)
        img_resized = img.resize((new_w, new_h), Image.LANCZOS)

        # Step 2: crop to target size (centered)
        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 2
        right = left + target_w
        bottom = top + target_h
        img_cropped = img_resized.crop((left, top, right, bottom))

        # Step 3: save result
        img_cropped.save(output_path)
        print(f"Processed {filename}: scaled to {new_w}x{new_h}, cropped to {target_w}x{target_h}")

print("✅ All images scaled, cropped, and saved perfectly for PSP!")
