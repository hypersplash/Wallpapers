import os
import random

def random_rename(folder_path):
    # Get all files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Shuffle a list of numbers from 1 to number of files
    random_numbers = list(range(1, len(files) + 1))
    random.shuffle(random_numbers)

    # Step 1: Rename to temporary names (to avoid name collisions)
    temp_names = []
    for file in files:
        old_path = os.path.join(folder_path, file)
        temp_name = f"__TEMP__{random.randint(100000,999999)}__{file}"
        temp_path = os.path.join(folder_path, temp_name)
        os.rename(old_path, temp_path)
        temp_names.append(temp_name)

    # Step 2: Rename temp files to random numbered names
    for i, temp_file in enumerate(temp_names):
        temp_path = os.path.join(folder_path, temp_file)
        file_ext = os.path.splitext(temp_file.split('__', 2)[-1])[1]
        new_name = f"{random_numbers[i]}{file_ext}"
        new_path = os.path.join(folder_path, new_name)
        os.rename(temp_path, new_path)

    print(f"✅ Renamed {len(files)} files randomly!")

def main():
    random_rename("./Computer")
    random_rename("./Phone")

main()

# Example usage:
# random_rename("/path/to/your/folder")
