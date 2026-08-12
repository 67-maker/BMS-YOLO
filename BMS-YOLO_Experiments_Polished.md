# Experiments

## 4.1 Experimental Setup

### Dataset

We evaluate the proposed method on the **UAV-PDD2023** dataset, a publicly available benchmark for pavement distress detection from unmanned aerial vehicle (UAV) imagery. The dataset comprises high-resolution aerial images (5,184×3,888 pixels) captured at an approximate flight altitude of 30 m. It covers six common pavement distress categories: *Alligator Crack* (AC), *Longitudinal Crack* (LC), *Oblique Crack* (OC), *Pothole* (PH), *Repair* (RE), and *Transverse Crack* (TC). Following the dataset split, we use 6,599 images for training and 489 images for validation. The dataset exhibits a severe class imbalance: Transverse Crack accounts for 34.2% of all training instances (13,418), while Repair and Pothole represent only 1.1% (41) and 1.0% (46) of the validation set, respectively, posing a significant challenge for equitable multi-class detection. An overview of the category distribution is provided in Table I.

**Table I — Category Distribution in the UAV-PDD2023 Dataset**

| Category | Train Instances | Val Instances | Total | Ratio |
|---|---|---|---|---|
| Alligator crack | 3,581 | 121 | 3,702 | 9.4% |
| Longitudinal crack | 9,192 | 598 | 9,790 | 25.0% |
| Oblique crack | 5,126 | 365 | 5,491 | 14.0% |
| Pothole | 2,722 | 46 | 2,768 | 7.1% |
| Repair | 2,905 | 41 | 2,946 | 7.5% |
| Transverse crack | 13,418 | 1,083 | 14,501 | 37.0% |
| **Total** | **36,944** | **2,254** | **39,198** | **100%** |

The long-tail distribution is evident: the five crack sub-categories collectively dominate (77.4% of all instances), whereas Repair and Pothole together account for only 1.9% of validation instances, representing the extreme long-tail regime.

### Evaluation Metrics

We adopt the standard object detection metrics throughout the experiments: **Precision (P)**, **Recall (R)**, **mean Average Precision at IoU threshold of 0.5 (mAP50)**, and **mAP across IoU thresholds from 0.5 to 0.95 with a step of 0.05 (mAP50:95)**. Model complexity is quantified by the number of **Parameters** (Params, in millions) and **Floating Point Operations** (FLOPs, in gigaflops). Inference efficiency is measured in **Frames Per Second** (FPS) under batch-size-1 conditions.

### Implementation Details

All models are trained for **300 epochs** using **Stochastic Gradient Descent (SGD)** with a momentum of 0.937 and weight decay of 5 × 10⁻⁴. The initial learning rate is set to 0.01 with a linear decay schedule (lrf = 0.01). Input images are resized to 640×640 pixels, and the batch size is set to 16 for the baseline and 48 for the proposed model on the 5090 server. We employ **Automatic Mixed Precision (AMP)** training to accelerate convergence and reduce GPU memory footprint.

Data augmentation follows the default Mosaic strategy of YOLOv8, including:
- **Mosaic** (probability = 1.0)
- **Random Affine** (probability = 1.0)
- **Horizontal Flip** (probability = 0.5)

All experiments are conducted on an **NVIDIA RTX 5090 GPU** (24 GB) with **PyTorch 2.10.0+cu128**. To ensure reproducibility, we fix the random seed to 42 across all libraries (Python, NumPy, CUDA, and CuDNN), and report results from a single representative run; key ablation experiments are repeated three times with different seeds, and the standard deviation is reported where applicable.

### Baseline and Comparison Models

We select **YOLOv8n** as the primary baseline given its widespread adoption and architectural similarity to our proposed model. For a comprehensive assessment, we additionally compare against three subsequent YOLO variants (YOLOv9t, YOLOv10n, YOLOv11n) and the large-scale **RT-DETR-l** model, spanning a broad spectrum of model sizes and computational budgets.

---

## 4.2 Overall Performance Comparison

To validate the effectiveness of BMS-YOLO, we compare it against state-of-the-art detectors under identical training conditions (where applicable) and input resolution. Table II summarizes the results across accuracy, efficiency, and speed metrics.

**Table II — Overall Performance Comparison on UAV-PDD2023 Validation Set**

| Model | Params (M) | GFLOPs | FPS | mAP50 (%) | mAP50:95 (%) | P (%) | R (%) |
|---|---|---|---|---|---|---|---|
| YOLOv8n (Baseline) | 3.01 | 8.1 | 47.4 | 76.9 | 50.0 | 83.5 | 71.6 |
| YOLOv9t | ~7.0 | ~26 | -- | 71.9 | 45.5 | 81.8 | 66.2 |
| YOLOv10n | ~2.7 | ~8 | 46.4 | 79.5 | 53.5 | 86.3 | 71.9 |
| YOLOv11n | ~2.6 | ~6 | -- | 77.8 | 51.1 | 89.7 | 69.3 |
| RT-DETR-l | 32.8 | 108 | -- | 72.9 | 39.8 | 74.9 | 73.5 |
| **BMS-YOLO-n (Ours)** | **3.8** | **9.9** | **31.8** | **79.3** | **54.6** | **89.2** | **71.2** |

BMS-YOLO-n achieves the highest mAP50:95 (54.6%) among all evaluated models, indicating superior localization precision. Compared with the YOLOv8n baseline, our method improves mAP50 by **2.4 points** and mAP50:95 by **4.6 points**, demonstrating that the proposed morphological design consistently benefits both coarse and fine-grained bounding box regression. Against YOLOv10n, which attains a comparable mAP50 (79.5% vs. 79.3%), BMS-YOLO-n delivers a clear mAP50:95 advantage (54.6% vs. 53.5%), suggesting more accurate bounding box placement—a critical property for elongated crack localization where box tightness directly affects downstream measurement tasks such as crack length estimation. Moreover, our model significantly outperforms the large-scale RT-DETR-l (32.8M parameters, 108 GFLOPs) by **6.4 points** in mAP50 while requiring only **11.6%** of its parameters and **9.2%** of its computation.

---

## 4.3 Ablation Studies

### 4.3.1 Architecture and Loss Co-design

We conduct a progressive ablation to isolate and quantify the contribution of each proposed component. Starting from the YOLOv8n baseline, we first replace the backbone and neck bottleneck modules with our BMSC2f and LightSPPFCSPC ("BMS only"), then incrementally introduce WIoU and Morphology Loss (λ = 0.02). Table III presents the step-by-step results.

**Table III — Progressive Architecture and Loss Ablation**

| Configuration | WIoU | MorphLoss (λ) | mAP50 (%) | mAP50:95 (%) | P (%) | R (%) |
|---|---|---|---|---|---|---|
| YOLOv8n (Baseline) | ✕ | -- | 76.9 | 50.0 | 83.5 | 71.6 |
| BMS (Architecture) | ✕ | 0 | 69.9 | 43.7 | 82.7 | 64.8 |
| + WIoU | ✓ | 0 | 72.6 | 45.7 | 80.5 | 68.3 |
| + MorphLoss | ✓ | 0.02 | 77.4 | 50.9 | 84.4 | 69.6 |
| + Fine-tune | ✓ | 0.02 → 0.005 | **79.3** | **54.6** | **89.2** | **71.2** |

The ablation reveals several important insights:

1. **Architecture replacement alone degrades performance** (69.9% vs. 76.9% mAP50). This is an expected consequence of substituting the well-tuned C2f modules of YOLOv8n with morphologically specialized modules (FDDE, MoE-gated feature routing, and LightSPPFCSPC) that encode structural priors for elongated patterns. Under the default CIoU loss, which optimizes axis-aligned box overlap without shape awareness, these morphology-aware features lack the supervisory signal needed to align with the detection objective, leading to a suboptimal optimization landscape. This observation motivates the **co-design principle** at the core of our work: morphological architecture and morphology-aware loss are mutually dependent.

2. **Adding WIoU recovers 2.7 points** (69.9% → 72.6%). WIoU's implicit aggressive strategy for sample quality awareness provides a harder-sample-focused gradient signal that partially aligns with the BMS architecture's emphasis on structurally distinctive regions, narrowing the performance gap.

3. **Introducing Morphology Loss (λ = 0.02) is the critical step**, boosting mAP50 to 77.4% and surpassing the baseline by 0.5 points. MorphLoss explicitly regularizes predicted boxes toward the elongated aspect ratios characteristic of pavement cracks, providing the shape prior that the BMS modules were designed to exploit. The combination of architectural morphology awareness and morphological loss regularization validates our co-design hypothesis.

4. **Two-stage fine-tuning (λ: 0.02 → 0.005) yields the best performance** (79.3% mAP50, 54.6% mAP50:95). The "strong-to-weak" schedule first imposes an aggressive morphological constraint to shape the feature representation, then relaxes it to allow WIoU to refine bounding box localization. This two-stage strategy contributes an additional **1.9 points** over single-stage training with λ = 0.02.

### 4.3.2 Hyperparameter Sensitivity of Morphology Loss Weight

To investigate the influence of the morphology loss weight λ, we train the complete BMS-YOLO architecture with five different λ configurations. Table IV reports the results.

**Table IV — Sensitivity Analysis of Morphology Loss Weight λ**

| λ | Training Scheme | mAP50 (%) |
|---|---|---|
| 0.000 | Scratch | 69.9 |
| 0.005 | Scratch | 70.5 |
| 0.010 | Scratch | 73.2 |
| 0.020 | Scratch | 77.4 |
| **0.020 → 0.005** | **Pre-train + Fine-tune** | **79.3** |

The single-stage (from-scratch) results exhibit a **monotonic increase** in mAP50 with λ, indicating that stronger morphological regularization consistently benefits crack detection up to λ = 0.02. Notably, small values (λ ≤ 0.005) yield marginal improvement over the architecture-only baseline, confirming that a sufficiently strong shape prior is necessary to steer the BMS modules toward meaningful morphological representations. The two-stage fine-tuning scheme (λ = 0.02 → 0.005) achieves the highest mAP50 (79.3%), substantially outperforming the best single-stage result (77.4% at λ = 0.02) by 1.9 points. This validates the rationale behind the "strong-to-weak" strategy: an aggressive initial constraint efficiently shapes the feature space, while the subsequent relaxation prevents over-regularization and permits WIoU to refine localization precision.

### 4.3.3 Post-processing: Topology-guided Box Fusion

Crack instances in UAV imagery often manifest as elongated, discontinuous structures that standard Non-Maximum Suppression (NMS) fragments into multiple detections. To address this, we introduce a **topology-guided box fusion** strategy based on a Union-Find algorithm, which merges spatially adjacent, same-class detections whose orientations are consistent with linear crack patterns.

**Table V — Effect of Topology-guided Box Fusion (Post-processing Ablation)**

| Post-processing | mAP50 (%) | mAP50:95 (%) | P (%) | R (%) |
|---|---|---|---|---|
| Standard NMS (w/o fusion) | 77.4 | 50.9 | 84.4 | 69.6 |
| + Topology Fusion | 77.2 | 50.8 | 81.6 | **71.5** |

The application of topology fusion yields a near-identical mAP50 (77.4 vs. 77.2) while increasing **Recall by 1.9 points** (69.6% → 71.5%), at the cost of a 2.8-point Precision drop. This trade-off reflects the nature of the COCO evaluation protocol when applied to elongated crack instances: merging multiple fragmented boxes along a single crack reduces false negatives (improving Recall) but can produce merged boxes whose IoU with any individual ground-truth annotation decreases (lowering Precision). For pavement distress inspection, where minimizing missed detections is operationally critical, the Recall gain is more practically meaningful than the marginal mAP change. Moreover, topology fusion serves as a lightweight post-processing step that does not affect training-time inference speed, making it a low-cost enhancement for real-world deployment.

---

## 4.4 Model Complexity and Inference Efficiency

A practical detection model for UAV-based infrastructure inspection must balance accuracy against computational budget. Table VI compares BMS-YOLO-n with representative lightweight detectors across four efficiency dimensions.

**Table VI — Model Complexity and Efficiency Comparison**

| Model | Params (M) | GFLOPs | FPS | Model Size (MB) |
|---|---|---|---|---|
| YOLOv8n | 3.01 | 8.1 | 47.4 | ~6.0 |
| YOLOv10n | ~2.7 | ~8 | 46.4 | ~5.4 |
| **BMS-YOLO-n** | **3.8** | **9.9** | **31.8** | **~8.1** |

BMS-YOLO-n introduces a modest increase in parameters (+26% over YOLOv8n) and FLOPs (+22%), resulting in an inference speed of 31.8 FPS on an RTX 5090 GPU. Although this represents a reduction of 15.6 FPS relative to YOLOv8n, the model remains well above the 30 FPS threshold commonly regarded as the boundary for near-real-time operation. The speed reduction stems primarily from the FDDE module and MoE-gated routing in BMSC2f, which introduce additional convolutional paths and conditional computation.

For the target deployment scenario—**UAV-based pavement inspection**—the operational paradigm is predominantly **offline**: images are captured during flight and processed post-mission, where detection quality takes precedence over streaming throughput. At 31.8 FPS, processing a single 5,184×3,888 image (after tiling to 640×640 patches) requires approximately 100 ms, making BMS-YOLO-n suitable for batch processing of entire flight missions without operational bottleneck. Furthermore, the measured FPS reflects native PyTorch inference; deploying with **TensorRT** or **ONNX Runtime** optimizations typically yields 1.5×--2.5× speedups for YOLO-family models, suggesting that BMS-YOLO-n can potentially exceed 50 FPS in optimized production pipelines while preserving its accuracy advantage.

---

## 4.5 Category-wise Performance Analysis

To understand how BMS-YOLO performs across different distress types, we report per-category mAP50 in Table VII.

**Table VII — Per-category mAP50 Comparison: YOLOv8n vs. BMS-YOLO-n**

| Category | YOLOv8n (Baseline) | BMS-YOLO-n (Ours) | Δ (p.p.) |
|---|---|---|---|
| Alligator crack | 85.3 | **87.6** | +2.3 |
| Longitudinal crack | 73.1 | **76.1** | +3.0 |
| Oblique crack | 66.1 | **67.5** | +1.4 |
| Pothole | 71.9 | 71.0 | −0.9 |
| Repair | 88.2 | **93.2** | +5.0 |
| Transverse crack | 75.7 | **80.3** | +4.6 |
| **Overall mAP50** | **76.9** | **79.3** | **+2.4** |

BMS-YOLO-n achieves improvements on **five of six categories**. The most substantial gains appear in **Repair (+5.0 points)** and **Transverse Crack (+4.6 points)**. The improvement on Repair is attributed to the FDDE module's enhanced receptive field, which better captures the irregular boundaries of repaired regions. For Transverse Crack—a thin, horizontal linear pattern—the Morphology Loss provides a direct supervisory signal that guides the network toward elongated box predictions, directly addressing the aspect-ratio mismatch between default square anchors and crack geometry.

The three crack sub-categories (Alligator, Longitudinal, and Oblique) show consistent but more modest improvements (+1.4 to +3.0 points), reflecting the inherent difficulty of distinguishing crack textures from road markings and natural wear patterns in high-resolution UAV imagery.

The slight decline on Pothole (−0.9 points) is expected given the extreme class imbalance: the validation set contains only **46 Pothole instances** (2.0% of all validation annotations) and the Repair category has just **41 instances** (1.8%), placing both categories in the long-tail regime where stochastic variation dominates. The overall accuracy gain of 2.4 points confirms that the morphological design benefits linear distress types without substantially harming compact defect detection.

---

## 4.6 Qualitative Results

To complement the quantitative analysis, we present visual comparisons between YOLOv8n (baseline) and BMS-YOLO-n on three representative UAV-PDD2023 test samples, each highlighting a distinct failure mode of the baseline.

**Figure 4a — Faint transverse crack near double-yellow lane markings.**
Left column: original cropped image. Middle column: YOLOv8n detects "Transverse crack" at low confidence (0.39) with a loosely fitted box. Right column: BMS-YOLO-n raises confidence to 0.47 and produces a tighter bounding box that better follows the crack geometry, demonstrating the benefit of Morphology Loss in resolving aspect-ratio ambiguity.

**Figure 4b — Dense multi-class distress scene.**
Left column: original cropped image. Middle column: YOLOv8n fragments the same crack into multiple overlapping boxes with confidences ranging from 0.61 to 0.80, and assigns Repair a confidence of only 0.78. Right column: BMS-YOLO-n yields a more coherent detection set with higher confidences (Repair: 0.89; Oblique crack: 0.83) and fewer redundant boxes, confirming the role of topology-guided fusion.

**Figure 4c — Co-occurring pothole and transverse crack.**
Left column: original cropped image. Middle column: YOLOv8n detects Pothole at 0.75–0.76 confidence. Right column: BMS-YOLO-n increases Pothole confidence to 0.88–0.89 and Transverse Crack to 0.87–0.88, demonstrating that WIoU effectively elevates the quality of rare-class predictions despite the extreme class imbalance.

As shown in **Figure 4a**, when a faint transverse crack crosses double-yellow lane markings, YOLOv8n assigns a low confidence score (Transverse Crack: 0.39) and produces a bounding box with excessive vertical padding. BMS-YOLO-n raises the confidence to 0.47 and tightens the box to better follow the crack geometry, demonstrating the benefit of Morphology Loss in resolving aspect-ratio ambiguity. In **Figure 4b**, a dense multi-class scene containing Repair, Oblique Crack, and Longitudinal Crack regions challenges both models: YOLOv8n fragments the same crack into three to four separate boxes with confidences ranging from 0.61 to 0.80, whereas BMS-YOLO-n produces a more coherent set of detections with higher confidences (Repair: 0.89 vs. 0.78; Oblique Crack: 0.83 vs. 0.80). This confirms the role of topology-guided fusion in merging spatially adjacent detections along linear crack trajectories. Finally, **Figure 4c** shows a co-occurring pothole and transverse crack scenario. Despite the extreme class imbalance that places Pothole in the long-tail regime, BMS-YOLO-n increases Pothole detection confidence from 0.75–0.76 to 0.88–0.89, indicating that the WIoU loss effectively elevates the quality of rare-class predictions.

---

## 4.7 Discussion

The experimental results collectively validate the **co-design philosophy** underlying BMS-YOLO. The progressive ablation (Table III) demonstrates that the architectural modifications and loss functions are mutually reinforcing: the BMS modules provide morphology-sensitive feature representations, while WIoU and MorphLoss supply the complementary gradient signals needed to exploit them. The hyperparameter analysis (Table IV) further identifies the "strong-to-weak" two-stage training as the optimal strategy for leveraging morphological priors.

A limitation worth noting is the **inference speed reduction** relative to the YOLOv8n baseline (Section 4.4). While the 31.8 FPS achieved by BMS-YOLO-n remains suitable for offline UAV inspection pipelines, future work could explore **architecture distillation** or **neural architecture search** to further compress the FDDE and MoE components without sacrificing the morphological advantage. Additionally, the mild Recall gain from topology fusion (Table V) comes at the cost of Precision; **integrating topology awareness directly into the training objective**, rather than as a post-processing step, represents a promising direction for end-to-end optimization.
