import os
import subprocess
from datetime import datetime

def get_date_password():
    """Generate password: daymonthtwodigitsyear (e.g., 291025)"""
    now = datetime.now()
    return f"{now.day:02d}{now.month:02d}{now.year % 100:02d}"

def get_file_size(filepath):
    """Get file size in bytes"""
    return os.path.getsize(filepath)

def compress_folder(folder_path, password, max_size_mb=500):
    """Compress folder into multiple independent archives of max_size_mb each"""
    folder_name = os.path.basename(folder_path.rstrip('/\\'))
    max_size_bytes = max_size_mb * 1024 * 1024

    print(f"\nProcessing: {folder_name}")

    # Collect all files with their sizes
    files_to_compress = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.exists(file_path):
                files_to_compress.append(file_path)

    if not files_to_compress:
        print(f"⚠ {folder_name} is empty")
        return False

    # Split files into batches based on size
    batches = []
    current_batch = []
    current_size = 0

    for file_path in files_to_compress:
        file_size = get_file_size(file_path)

        # If adding this file exceeds limit and we have files in current batch, start new batch
        if current_size + file_size > max_size_bytes and current_batch:
            batches.append(current_batch)
            current_batch = [file_path]
            current_size = file_size
        else:
            current_batch.append(file_path)
            current_size += file_size

    # Add last batch
    if current_batch:
        batches.append(current_batch)

    print(f"  Splitting into {len(batches)} archive(s)")

    # Compress each batch
    try:
        for batch_num, batch_files in enumerate(batches, start=1):
            archive_name = f"{folder_name}_{batch_num}.7z"

            # Create list file for 7z
            list_file = f".temp_list_{folder_name}_{batch_num}.txt"
            with open(list_file, 'w', encoding='utf-8') as f:
                for file_path in batch_files:
                    f.write(f"{file_path}\n")

            cmd = [
                '7z',
                'a',
                '-t7z',
                '-mx=9',
                '-mhe=on',
                f'-p{password}',
                '-mfb=273',
                '-md=128m',
                archive_name,
                f'@{list_file}'
            ]

            result = subprocess.run(cmd, check=True, capture_output=True, text=True)

            # Clean up list file
            os.remove(list_file)

            archive_size = get_file_size(archive_name) / (1024 * 1024)
            print(f"  ✓ {archive_name} ({archive_size:.2f} MB, {len(batch_files)} files)")

        print(f"✓ Done: {folder_name}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {folder_name}")
        print(f"  {e.stderr}")
        # Clean up any temp files
        for i in range(1, len(batches) + 1):
            temp_list = f".temp_list_{folder_name}_{i}.txt"
            if os.path.exists(temp_list):
                os.remove(temp_list)
        return False
    except FileNotFoundError:
        print("✗ 7z not found. Install 7-Zip and add to PATH")
        return False

def main():
    folders = ['./Computer', './Phone', './PSP']
    password = get_date_password()

    print(f"Password: {password}")

    existing = [f for f in folders if os.path.exists(f) and os.path.isdir(f)]
    missing = [f for f in folders if f not in existing]

    if missing:
        print(f"\n⚠ Missing: {', '.join(missing)}")

    if not existing:
        print("✗ No folders found")
        return

    success = 0
    for folder in existing:
        if compress_folder(folder, password):
            success += 1

    print(f"\n{'='*40}")
    print(f"Done: {success}/{len(existing)} folders")
    print(f"{'='*40}")

if __name__ == "__main__":
    main()
