from pathlib import Path
import uuid


def is_already_numbered(file_path: Path) -> bool:
    """
    Returns True if filename matches: number + extension
    Example: 1.jpg, 23.png, 7.txt
    """
    return file_path.is_file() and file_path.stem.isdigit() and file_path.suffix != ""


def random_rename(folder_path: str):
    folder = Path(folder_path)

    if not folder.is_dir():
        print(f"⚠ '{folder_path}' is not a valid folder.")
        return

    all_files = [p for p in folder.iterdir() if p.is_file()]

    # Keep files already matching: number.extension
    already_good = [p for p in all_files if is_already_numbered(p)]

    # Only rename the rest, sorted alphabetically
    to_rename = sorted(
        (p for p in all_files if not is_already_numbered(p)),
        key=lambda p: p.name.casefold()
    )

    if not to_rename:
        print(f"✅ No files needed renaming in '{folder_path}'.")
        return

    # Numbers already taken by files like 1.jpg, 2.png, etc.
    used_numbers = {int(p.stem) for p in already_good}

    # Assign the smallest available number in alphabetical order
    rename_map = []
    next_number = 1

    for file_path in to_rename:
        while next_number in used_numbers:
            next_number += 1

        new_name = f"{next_number}{file_path.suffix}"
        rename_map.append((file_path, new_name))
        used_numbers.add(next_number)
        next_number += 1

    # Phase 1: rename targets to temporary names
    temp_map = []
    for old_path, final_name in rename_map:
        temp_name = f".__tmp__{uuid.uuid4().hex}{old_path.suffix}"
        temp_path = folder / temp_name
        old_path.rename(temp_path)
        temp_map.append((temp_path, final_name))

    # Phase 2: rename temp names to final names
    for temp_path, final_name in temp_map:
        final_path = folder / final_name
        temp_path.rename(final_path)

    print(f"✅ Renamed {len(to_rename)} file(s) in '{folder_path}' alphabetically.")


def main():
    random_rename("./Computer")
    random_rename("./Phone")


if __name__ == "__main__":
    main()
