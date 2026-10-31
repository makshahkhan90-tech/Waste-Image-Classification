import os
from pathlib import Path

base_path = Path("D:/Waste-Classification-Project/dataset/garbage-classification")
# Find the actual Garbage classification folder inside
# It might be nested like .../Garbage classification/Garbage classification/
# Let's find all subfolders that contain images

def find_class_folders(root):
    class_folders = []
    for r, dirs, files in os.walk(root):
        # if folder contains jpg and no subfolders with jpg, it's a class folder
        if files and any(f.lower().endswith(('.jpg','.jpeg','.png')) for f in files):
            # avoid counting parent folders that have subfolders
            has_image_subfolders = False
            for d in dirs:
                sub_path = Path(r) / d
                if any(sub_path.rglob("*.jpg")):
                    has_image_subfolders = True
                    break
            if not has_image_subfolders:
                class_folders.append(Path(r))
    return class_folders

# Try to locate correctly
search_root = base_path
if not any(search_root.iterdir()):
    print(f"Dataset path empty: {search_root}")
    exit()

# The dataset structure is: garbage-classification/Garbage classification/Garbage classification/CLASS/*.jpg
# Let's walk
class_counts = {}
for folder in search_root.rglob("*"):
    if folder.is_dir():
        images = list(folder.glob("*.jpg")) + list(folder.glob("*.jpeg")) + list(folder.glob("*.png"))
        if images and len(images) < 5000: # likely a class folder
            # Check if its children are not class folders
            if not any((folder / sub).is_dir() and list((folder / sub).glob("*.jpg")) for sub in os.listdir(folder) if (folder / sub).is_dir()):
                if len(images) > 10: # valid class
                    class_counts[folder.name] = len(images)

# Sort and display
print("\n=== DATASET CLASS DISTRIBUTION ===")
total = 0
for cls, count in sorted(class_counts.items()):
    print(f"{cls:20s} : {count} images")
    total += count

print(f"\nTotal Classes: {len(class_counts)}")
print(f"Total Images : {total}")

# Save for report
with open("D:/Waste-Classification-Project/dataset_info.txt", "w") as f:
    f.write("Dataset: Garbage Classification (mostafaabla/garbage-classification)\n")
    f.write(f"Total Classes: {len(class_counts)}\n")
    f.write(f"Total Images: {total}\n\n")
    for cls, count in sorted(class_counts.items()):
        f.write(f"{cls}: {count}\n")

print("\nSaved dataset_info.txt")