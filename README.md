# BMS-YOLO: A Lightweight Box-Supervised Morphology-Aware Pavement Distress Detection Model

**Repository for supplementary materials and source files.**

## Paper

- **Title:** BMS-YOLO: A Lightweight Box-Supervised Morphology-Aware Pavement Distress Detection Model
- **Dataset:** [UAV-PDD2023](https://zenodo.org/records/8429208) (2,440 images, 11,158 annotations)
- **Target Journal:** IEEE Access

## Repository Structure

```
├── IEEE ACCESS_latex/          # LaTeX source for IEEE Access submission
│   ├── access_final.tex       # Main paper source (current version)
│   ├── references.bib          # 42 references
│   ├── figure1_architecture.pdf   # Overall architecture diagram
│   ├── figure2_modules.pdf       # Module structure diagrams
│   ├── fig3_ablation.pdf        # Ablation bar chart
│   ├── fig4_lambda_sensitivity.pdf   # Lambda sensitivity line chart
│   ├── fig5_category_comparison.pdf  # Per-category mAP comparison
│   ├── fig6_fps_params.pdf     # FPS vs. Parameters scatter plot
│   ├── qualitative_fig_*.pdf   # Qualitative result figures
│   ├── generate_architecture.py      # Figure 1 generation script
│   ├── generate_figure2_modules.py   # Figure 2 generation script
│   └── access_final.pdf        # Compiled PDF
├── r1_artifacts/              # Data split transparency (Reviewer R1)
│   ├── train_manifest.txt     # Train split file list + hashes
│   ├── val_manifest.txt       # Val split file list + hashes
│   ├── test_manifest.txt      # Test split file list + hashes
│   ├── augmentation_mapping.csv  # Augmented → original mapping
│   ├── augmentation_stats.csv    # Augmentation summary statistics
│   ├── leakage_report.txt     # Adjacent-frame leakage analysis
│   └── generate_r1_artifacts.py    # Manifest generation script
└── README.md
```

## Compilation

```bash
cd "IEEE ACCESS_latex"
xelatex access_final.tex
bibtex access_final
xelatex access_final.tex
xelatex access_final.tex
```

## Figure Generation

```bash
python generate_architecture.py        # Figure 1
python generate_figure2_modules.py     # Figure 2
```

## Data Split

- **Protocol:** 7:2:1 (train:val:test), random seed = 42
- **Augmentation:** Offline oversampling of 3 minority classes (train only)
- See `r1_artifacts/README.md` for full details
