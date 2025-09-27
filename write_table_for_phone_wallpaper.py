import os

# Path to your folder
folder = "./Phone"  # change this to your folder path

# List all image files (adjust extensions as needed)
images = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.xcf'))]

# Make two-column rows
table = "| Preview | Filename | Preview | Filename |\n"
table += "|---------|---------|---------|---------|\n"

for i in range(0, len(images), 2):
    first = f"![]({folder}/{images[i]}) | {images[i]}"
    second = ""
    if i+1 < len(images):
        second = f"![]({folder}/{images[i+1]}) | {images[i+1]}"
    else:
        second = " | "
    table += f"{first} | {second} |\n"

# Output
print(table)
