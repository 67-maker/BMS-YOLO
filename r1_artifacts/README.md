# R1 Artifacts — Data Split and Augmentation Transparency

These files address Reviewer R1: "Reconstruct data lineage and split."

## Files

| File | Description |
|------|-------------|
| `train_manifest.txt` | 1,707 original training image filenames + SHA-256 hashes |
| `val_manifest.txt` | 489 original validation image filenames + SHA-256 hashes |
| `test_manifest.txt` | 244 original test image filenames + SHA-256 hashes |
| `augmentation_mapping.csv` | 4,892 rows: each augmented image → source original image → target class ID |
| `augmentation_stats.csv` | Summary: 3 target classes with candidate counts and augmented counts |
| `leakage_report.txt` | Adjacent-frame leakage analysis across split boundaries |

## How to Generate

1. Ensure the UAV-PDD2023 dataset is available at the path specified in `generate_r1_artifacts.py`
2. Install dependencies: `pip install scikit-learn`
3. Run: `python generate_r1_artifacts.py`

## Split Protocol

- **Source:** 2,440 original images from Zenodo record 8429208
- **Split ratio:** 7:2:1 (train:val:test)
- **Random seed:** 42
- **Splitting method:** `sklearn.model_selection.train_test_split` with `random_state=42`
  - First pass: 70% train, 30% temp
  - Second pass: temp split into val (2/3) and test (1/3)
- **Augmentation:** Applied only to training set minority classes (Alligator Crack, Pothole, Repair)

## Augmentation Details

| Target Class | ID | Original Instances | Augmented Images Generated |
|---|---|---|---|
| Alligator Crack | 0 | 400 | 1,519 |
| Pothole | 3 | 132 | 1,707 |
| Repair | 4 | 212 | 1,666 |

**Total augmented images:** 4,892 (added to 1,707 originals = 6,599 training images)

**Naming convention:** `{original_name}_aug_{sequence}_{target_class_id}.jpg`

**Transformations (Albumentations):**
- Horizontal Flip (p=0.5)
- Random Rotate 90° (p=0.3)
- Shift-Scale-Rotate (p=0.5)
- Random Brightness/Contrast (p=0.6)
- HSV Shift (p=0.5)
- Gaussian Blur (p=0.2)
- `min_visibility=0.3`

## Leakage Analysis

See `leakage_report.txt` for the full analysis. Summary:
- Four patches of each source image always stay in the same split (no pixel-level leakage)
- Adjacent frames (consecutive sequence numbers) may straddle train/test boundaries
- This approximates realistic generalization: detecting on unseen road segments
