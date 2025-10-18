import os
import re
import random

def random_rename(folder_path):
    """
    Renames files in folder_path to: [random_digit].[original_extension]
    - Files already matching [digit].[ext] are skipped
    - New numbers start from (highest_existing_digit + 1) and continue randomly
    - No number overlaps, regardless of file type
    """

    # Pattern to match [digit].[extension]
    pattern = re.compile(r'^(\d+)\.[^.]+$')

    # Get all files in the directory
    all_files = [
        f for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    if not all_files:
        print(f"⚡ No files found in '{folder_path}'!")
        return

    # Separate files that match the pattern vs those that need renaming
    used_numbers = set()
    files_to_rename = []

    for file in all_files:
        match = pattern.match(file)
        if match:
            used_numbers.add(int(match.group(1)))
        else:
            files_to_rename.append(file)

    if not files_to_rename:
        print(f"⚡ All files already match the pattern in '{folder_path}'!")
        return

    # Find the highest existing digit
    highest_digit = max(used_numbers) if used_numbers else 0

    # Generate new unique numbers starting from highest + 1
    start_num = highest_digit + 1
    new_numbers = list(range(start_num, start_num + len(files_to_rename)))
    random.shuffle(new_numbers)

    # Build rename mapping
    rename_map = {}
    for i, file in enumerate(files_to_rename):
        file_ext = os.path.splitext(file)[1]
        new_name = f"{new_numbers[i]}{file_ext}"
        rename_map[file] = new_name

    # Execute renames
    for old_name, new_name in rename_map.items():
        old_path = os.path.join(folder_path, old_name)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)

    print(f"✅ Renamed {len(files_to_rename)} files in '{folder_path}' → starting from digit {start_num}, no overlaps!")

def main():
    random_rename("./Computer")
    random_rename("./Phone")

if __name__ == "__main__":
    main()
