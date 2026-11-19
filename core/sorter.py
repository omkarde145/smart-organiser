import os
import shutil

CATEGORY_MAP = {
    "Documents": {".pdf", ".docx", ".txt", ".md", ".xlsx", ".pptx", ".csv"},
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"},
    "Archives": {".zip", ".tar", ".gz", ".rar", ".7z"},
    "Code": {".py", ".cpp", ".c", ".java", ".js", ".ts", ".html", ".css", ".json"},
    "Media": {".mp4", ".mkv", ".mp3", ".wav"},
}

def get_category(extension: str) -> str:
    ext = extension.lower()
    for category, extensions in CATEGORY_MAP.items():
        if ext in extensions:
            return category
    return "Others"

def resolve_collision(dest_path: str) -> str:
    """Append numeric suffix if destination filename already exists."""
    if not os.path.exists(dest_path):
        return dest_path
    base, ext = os.path.splitext(dest_path)
    counter = 1
    while os.path.exists(f"{base}_{counter}{ext}"):
        counter += 1
    return f"{base}_{counter}{ext}"

def organize_directory(target_dir: str, dry_run: bool = False) -> list[dict]:
    """Sort top-level files into category subfolders and return move records."""
    operations = []
    for item in os.listdir(target_dir):
        src_path = os.path.join(target_dir, item)
        if not os.path.isfile(src_path) or item.startswith("."):
            continue

        _, ext = os.path.splitext(item)
        category = get_category(ext)
        dest_dir = os.path.join(target_dir, category)
        dest_path = resolve_collision(os.path.join(dest_dir, item))

        operations.append({"src": src_path, "dest": dest_path})

        if not dry_run:
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(src_path, dest_path)

    return operations
