from pathlib import Path
import shutil


def clear_directory(path: str, include_subdir=False):
    for item in Path(path).iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir() & include_subdir:
            shutil.rmtree(item)