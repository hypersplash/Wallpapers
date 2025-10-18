import os
from PIL import Image

# Define input and output directories
input_dir = "./Input"
output_dir = "./Output"

# Make sure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Loop through files in input directory
for file_name in os.listdir(input_dir):
    if file_name.lower().endswith(".webp"):  # only webp files
        input_path = os.path.join(input_dir, file_name)
        output_name = os.path.splitext(file_name)[0] + ".png"
        output_path = os.path.join(output_dir, output_name)

        # Open and save as PNG (lossless)
        with Image.open(input_path) as img:
            img.save(output_path, "PNG")

        print(f"Converted: {file_name} → {output_name}")

print("✅ Conversion complete.")
