import os
import random
import shutil

def random_rename(folder_path):
    """
    Renames ALL files in folder_path to: [random_digit].[original_extension]
    - No files are skipped
    - Numbers are assigned sequentially from 1 to N (where N = number of files)
    - Then shuffled randomly to avoid predictable patterns
    - Guarantees no gaps or jumps in the number sequence
    - Uses a temp folder to avoid conflicts during rename
    """
    # Get all files in the directory (exclude folders)
    all_files = [
        f for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    if not all_files:
        print(f"⚡ No files found in '{folder_path}'!")
        return

    # Create temp folder
    temp_folder = os.path.join(folder_path, "_temp_rename")
    os.makedirs(temp_folder, exist_ok=True)

    # Generate sequential numbers from 1 to N
    total_files = len(all_files)
    numbers = list(range(1, total_files + 1))
    random.shuffle(numbers)

    # Build rename mapping
    rename_map = {}
    for i, file in enumerate(all_files):
        file_ext = os.path.splitext(file)[1]
        new_name = f"{numbers[i]}{file_ext}"
        rename_map[file] = new_name

    # Phase 1: Move all files to temp folder
    for old_name in rename_map:
        old_path = os.path.join(folder_path, old_name)
        temp_path = os.path.join(temp_folder, old_name)
        shutil.move(old_path, temp_path)

    # Phase 2: Move files back with new names
    for old_name, new_name in rename_map.items():
        temp_path = os.path.join(temp_folder, old_name)
        final_path = os.path.join(folder_path, new_name)
        shutil.move(temp_path, final_path)

    # Clean up temp folder
    os.rmdir(temp_folder)

    print(f"✅ Renamed {total_files} files in '{folder_path}' → numbers 1-{total_files}, shuffled randomly!")

def main():
    random_rename("./Computer")
    random_rename("./Phone")

if __name__ == "__main__":
    main()
