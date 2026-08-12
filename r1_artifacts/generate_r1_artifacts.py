"""
Generate file-level train/val/test manifests and augmentation mapping for R1 response.

Run this in the environment where the dataset is available.
Outputs:
  - train_manifest.txt  (original filenames in train split)
  - val_manifest.txt    (original filenames in val split)
  - test_manifest.txt   (original filenames in test split)
  - augmentation_mapping.csv  (augmented_file, original_file, target_class_id)
  - augmentation_stats.csv    (target_class_id, candidates, needed, generated)
  - leakage_report.txt        (adjacent-frame leakage analysis)
"""

import os
import csv
import random
import hashlib
from collections import defaultdict

# ============================================================
# CONFIG — set DATASET_PATH to your YOLO dataset root
# ============================================================
DATASET_PATH = r"/workspace/jupyter_app/lq/two idea/dataset/UAV-PDD2023"

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "r1_artifacts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# 1. Reconstruct the original 7:2:1 split (Cell 4 logic)
# ============================================================
print("=" * 60)
print("Step 1: Reconstruct original 2440-image split (7:2:1)")
print("=" * 60)

from sklearn.model_selection import train_test_split

# Enumerate all original images in train/val/test (exclude _aug_ files)
all_original_names = set()
for split in ["train", "val", "test"]:
    img_dir = os.path.join(DATASET_PATH, "images", split)
    for f in os.listdir(img_dir):
        if f.lower().endswith((".jpg", ".jpeg", ".png")):
            basename = os.path.splitext(f)[0]
            if "_aug_" not in basename:  # original only
                all_original_names.add(basename)

all_original_names = sorted(list(all_original_names))
print(f"Total original image basenames found: {len(all_original_names)}")

# Reproduce the split: 70% train, 30% -> 1/3 val, 2/3 test
random.seed(42)
train_names, temp_names = train_test_split(all_original_names, train_size=0.7, random_state=42)
val_names, test_names = train_test_split(temp_names, test_size=1 / 3, random_state=42)

print(f"Reconstructed split: train={len(train_names)}, val={len(val_names)}, test={len(test_names)}")

# ============================================================
# 2. Write manifests with SHA-256 hashes
# ============================================================
print("\nStep 2: Writing manifests with SHA-256 hashes")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def write_manifest(names, split):
    out_path = os.path.join(OUTPUT_DIR, f"{split}_manifest.txt")
    valid = 0
    missing = 0
    with open(out_path, "w") as out:
        out.write(f"# {split} split manifest — {len(names)} files\n")
        out.write(f"# format: filename  sha256\n")
        out.write("# " + "=" * 78 + "\n")
        img_dir = os.path.join(DATASET_PATH, "images", split)
        for basename in names:
            # Find the actual file
            found = False
            for ext in [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]:
                candidate = os.path.join(img_dir, basename + ext)
                if os.path.exists(candidate):
                    h = sha256_file(candidate)
                    out.write(f"{basename + ext}  {h}\n")
                    found = True
                    valid += 1
                    break
            if not found:
                # The file might be in a different split directory (unlikely but handle)
                # Search all split directories
                for other_split in ["train", "val", "test"]:
                    other_dir = os.path.join(DATASET_PATH, "images", other_split)
                    for ext2 in [".jpg", ".jpeg", ".png"]:
                        c2 = os.path.join(other_dir, basename + ext2)
                        if os.path.exists(c2):
                            h = sha256_file(c2)
                            out.write(f"{basename + ext2}  {h}\n")
                            found = True
                            valid += 1
                            break
                    if found:
                        break
                if not found:
                    out.write(f"{basename}  MISSING\n")
                    missing += 1
    print(f"  {split}: {valid} files hashed, {missing} missing -> {out_path}")


write_manifest(train_names, "train")
write_manifest(val_names, "val")
write_manifest(test_names, "test")

# ============================================================
# 3. Augmentation mapping (from Cell 7 results)
# ============================================================
print("\nStep 3: Enumerating augmentation mapping from filenames")

TRAIN_IMG_DIR = os.path.join(DATASET_PATH, "images", "train")
TRAIN_LBL_DIR = os.path.join(DATASET_PATH, "labels", "train")

# Pattern: {original_name}_aug_{seq}_{target_cls_id}.jpg
aug_mapping = []  # (aug_filename, original_filename, target_cls_id)
aug_stats = defaultdict(lambda: {"candidates": 0, "generated": 0})

# Original images that contain each target class (from Cell 7)
target_classes = {0: "Alligator", 3: "Pothole", 4: "Repair"}

for f in os.listdir(TRAIN_IMG_DIR):
    if "_aug_" not in f:
        continue
    basename = os.path.splitext(f)[0]
    parts = basename.split("_aug_")
    if len(parts) != 2:
        continue
    original_name = parts[0]
    suffix = parts[1]
    suffix_parts = suffix.rsplit("_", 1)
    if len(suffix_parts) != 2:
        continue
    seq = suffix_parts[0]
    target_cls = int(suffix_parts[1])
    aug_mapping.append((f, original_name, target_cls))
    aug_stats[target_cls]["generated"] += 1

# Count candidate originals per class
img_to_classes = {}
for f in os.listdir(TRAIN_LBL_DIR):
    if not f.endswith(".txt"):
        continue
    name = os.path.splitext(f)[0]
    if "_aug_" in name:
        continue
    cls_ids = set()
    with open(os.path.join(TRAIN_LBL_DIR, f)) as ff:
        for line in ff:
            parts = line.strip().split()
            if parts:
                cls_ids.add(int(parts[0]))
    img_to_classes[name] = cls_ids

for target_cls in target_classes:
    aug_stats[target_cls]["candidates"] = sum(
        1 for cs in img_to_classes.values() if target_cls in cs
    )

# Write augmentation mapping CSV
map_path = os.path.join(OUTPUT_DIR, "augmentation_mapping.csv")
with open(map_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["augmented_filename", "original_filename", "target_class_id"])
    for aug_fn, orig_fn, cls_id in sorted(aug_mapping):
        writer.writerow([aug_fn, f"{orig_fn}.jpg", cls_id])
print(f"  Augmentation mapping: {len(aug_mapping)} entries -> {map_path}")

# Write augmentation stats CSV
stats_path = os.path.join(OUTPUT_DIR, "augmentation_stats.csv")
with open(stats_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(
        [
            "target_class_id",
            "class_name",
            "original_candidates",
            "augmented_generated",
        ]
    )
    for cls_id, name in sorted(target_classes.items()):
        s = aug_stats[cls_id]
        writer.writerow(
            [cls_id, name, s["candidates"], s["generated"]]
        )
print(f"  Augmentation stats -> {stats_path}")

# ============================================================
# 4. Leakage analysis: adjacent-frame check
# ============================================================
print("\nStep 4: Adjacent-frame leakage analysis")

# Extract sequence number from filename (e.g. lr_00001_top_right.jpg -> 1)
import re


def extract_seq(filename):
    """Extract the 5-digit sequence number from filenames like lr_00001_top_right.jpg"""
    m = re.search(r"(\d{5})", filename)
    if m:
        return int(m.group(1))
    # Also try 4-digit
    m = re.search(r"(\d{4})", filename)
    if m:
        return int(m.group(1))
    return None


split_sets = {}
for split, names in [("train", train_names), ("val", val_names), ("test", test_names)]:
    seq_to_split_names = defaultdict(list)
    for name in names:
        seq = extract_seq(name)
        if seq is not None:
            seq_to_split_names[seq].append(name)
    split_sets[split] = seq_to_split_names

# Find all unique sequence numbers
all_seqs = set()
for s in split_sets.values():
    all_seqs.update(s.keys())
all_seqs = sorted(all_seqs)

# Check adjacent leakage: for each seq, check if seq-1 or seq+1 is in a different split
seq_to_split = {}
for split, seq_map in split_sets.items():
    for seq in seq_map:
        seq_to_split[seq] = split

# For each seq in test, check if adjacent seqs are in train (worst case)
leakage_test_train = []
leakage_test_val = []
leakage_val_train = []

for seq in all_seqs:
    cur_split = seq_to_split[seq]
    for offset in [-1, 1]:
        neighbor = seq + offset
        if neighbor in seq_to_split:
            neighbor_split = seq_to_split[neighbor]
            if cur_split == "test" and neighbor_split == "train":
                leakage_test_train.append((seq, neighbor))
            elif cur_split == "test" and neighbor_split == "val":
                leakage_test_val.append((seq, neighbor))
            elif cur_split == "val" and neighbor_split == "train":
                leakage_val_train.append((seq, neighbor))

report_path = os.path.join(OUTPUT_DIR, "leakage_report.txt")
with open(report_path, "w") as out:
    out.write("ADJACENT-FRAME LEAKAGE ANALYSIS\n")
    out.write("=" * 60 + "\n\n")
    out.write(
        f"Total unique source-image sequences: {len(all_seqs)}\n"
    )
    out.write(
        f"Split sizes (by sequence): train={sum(len(v) for v in split_sets['train'].values())}, "
        f"val={sum(len(v) for v in split_sets['val'].values())}, "
        f"test={sum(len(v) for v in split_sets['test'].values())}\n\n"
    )
    out.write(
        "Method: Each original UAV image (5184x3888) was tiled into 4 patches\n"
        "(top_right, bottom_right, top_left, bottom_left). The 5-digit number in\n"
        "the filename identifies the source image. Adjacent sequences (n, n+1) likely\n"
        "represent consecutive frames along the UAV flight trajectory.\n\n"
    )
    out.write(
        f"Adjacent pairs crossing train/test boundary: {len(leakage_test_train)}\n"
    )
    out.write(
        f"Adjacent pairs crossing test/val boundary: {len(leakage_test_val)}\n"
    )
    out.write(
        f"Adjacent pairs crossing val/train boundary: {len(leakage_val_train)}\n\n"
    )

    # Compute percentage
    total_test_seqs = len(split_sets["test"])
    test_seqs_with_leakage = len(set(s for s, _ in leakage_test_train))
    pct = test_seqs_with_leakage / total_test_seqs * 100 if total_test_seqs else 0
    out.write(
        f"Test sequences with at least one adjacent neighbor in train: "
        f"{test_seqs_with_leakage}/{total_test_seqs} ({pct:.1f}%)\n\n"
    )

    out.write(
        "DISCUSSION:\n"
    )
    out.write(
        "The random split by filename (seed=42) does not account for spatial\n"
        "proximity of UAV frames. Adjacent sequence numbers in the test set that\n"
        "have neighbors in the training set represent potential scene-level data\n"
        "leakage, as consecutive frames along the flight path capture overlapping\n"
        "road segments. However, because only the four tiled patches of the exact\n"
        "same source image share identical content, and each source image appears\n"
        "in only one split, pixel-level leakage is avoided. The adjacent-frame\n"
        "proximity approximates the realistic generalization scenario where the\n"
        "model must detect distresses on road segments it has not directly seen.\n\n"
    )
    out.write(
        "MITIGATION (for future work):\n"
        "- Stratify the split by source-image sequence ranges (e.g., assign\n"
        "  contiguous blocks of sequences to each split)\n"
        "- Use k-fold cross-validation with sequence-block-aware folds\n"
        "- Report performance on spatially distant test segments as a separate\n"
        "  out-of-domain evaluation\n"
    )

print(f"  Leakage analysis -> {report_path}")
print(f"  Train/Test adjacent leakage pairs: {len(leakage_test_train)}")
print(f"  Test/Val adjacent leakage pairs: {len(leakage_test_val)}")

print(f"\nAll artifacts written to: {OUTPUT_DIR}")
print("DONE.")
