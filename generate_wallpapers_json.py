import os, json, re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

def generate_json(folder):
    exts = ('.jpg', '.jpeg', '.png', '.webp')
    files = [f for f in os.listdir(folder) if f.lower().endswith(exts)]
    files.sort(key=natural_sort_key)
    with open(os.path.join(folder, 'wallpapers.json'), 'w', encoding='utf-8') as f:
        json.dump(files, f, ensure_ascii=False, indent=2)
    print(f'✅ {folder}/wallpapers.json written with {len(files)} wallpapers.')

if __name__ == "__main__":
    for folder in ["Computer", "Phone"]:
        if os.path.isdir(folder):
            generate_json(folder)
        else:
            print(f"⚠️  Folder '{folder}' not found.")
