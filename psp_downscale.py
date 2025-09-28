from PIL import Image
import os

# ----- CONFIG -----
input_folder = "Computer"      # Folder with your original images
output_folder = "PSP"          # PSP output folder in the current directory
target_resolution = (480, 272) # PSP resolution
# ------------------

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Supported extensions
extensions = (".png", ".jpg", ".jpeg")

for filename in os.listdir(input_folder):
    if filename.lower().endswith(extensions):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # Open image
        img = Image.open(input_path)

        # Resize to PSP resolution using Lanczos
        img_resized = img.resize(target_resolution, resample=Image.LANCZOS)

        # Save downsized image
        img_resized.save(output_path)
        print(f"Downscaled {filename} → {target_resolution}")

print("All images downscaled to PSP resolution and saved in 'PSP' folder! ✅")
