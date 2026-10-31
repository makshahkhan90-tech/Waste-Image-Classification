import kagglehub
import shutil
import os
from pathlib import Path

print("Downloading Garbage Classification dataset...")

path = kagglehub.dataset_download("mostafaabla/garbage-classification")
print(f"Dataset downloaded at temp path: {path}")

project_dataset_path = Path("D:/Waste-Classification-Project/dataset/garbage-classification")
project_dataset_path.mkdir(parents=True, exist_ok=True)

source_path = Path(path)
for item in source_path.rglob("*"):
    if item.is_file():
        rel_path = item.relative_to(source_path)
        dest = project_dataset_path / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, dest)

print(f"\nDataset successfully copied to: {project_dataset_path}")
print("\nListing files:")
for root, dirs, files in os.walk(project_dataset_path):
    level = root.replace(str(project_dataset_path), '').count(os.sep)
    indent = ' ' * 2 * level
    print(f'{indent}{os.path.basename(root)}/')
    subindent = ' ' * 2 * (level + 1)
    for f in files[:5]:
        print(f'{subindent}{f}')
    if len(files) > 5:
        print(f'{subindent}... and {len(files)-5} more files')

print("\nDONE - Dataset Ready!")