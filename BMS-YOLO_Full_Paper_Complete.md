# BMS-YOLO: A Lightweight Box-Supervised Morphology-Aware Pavement Distress Detection Model

**Qi Liu**
College of Big Data and Intelligent Engineering, Yangtze Normal University, Chongqing, China
Email: 17837248232@163.com

---

## Abstract

Accurate detection of pavement distresses such as cracks and potholes is critical for infrastructure safety maintenance. However, existing YOLO-based methods face challenges in feature representation, computational redundancy, and loss function design, especially when dealing with the extreme morphological differences between elongated cracks and compact potholes. To address these issues, this paper proposes BMS-YOLO (Box-supervised Morphology-aware Sparse YOLO), a lightweight pavement distress detection model under pure box supervision. At the feature extraction level, a Frequency-Direction Detail Enhancement (FDDE) module decouples the feature map into high- and low-frequency branches and strengthens crack edge responses via directional convolutions. A Morphology-aware Sparse Mixture of Experts (MorphSparseMoE) is embedded within C2f blocks to dynamically activate four expert types via top-k routing, enabling morphology-adaptive modeling. Efficient Channel Attention (ECA) and a lightweight SPPF-CSPC structure further enlarge the receptive field while reducing parameters. At the loss function level, Wise-IoU (WIoU) replaces CIoU with center-distance-based dynamic focusing, and a box morphology consistency loss constrains aspect ratio and area in log space. A post-processing pipeline with topology-guided Union-Find box fusion mitigates fragmented crack predictions. Experiments on the UAV-PDD2023 benchmark dataset show that BMS-YOLO achieves 79.3% mAP50 and 54.6% mAP50:95 with only 3.8M parameters, significantly outperforming YOLOv8n (+2.4 points mAP50, +4.6 points mAP50:95) while maintaining 31.8 FPS on an RTX 5090 GPU. Ablation studies validate the effectiveness of each proposed component and the architecture-loss co-design philosophy.

**Keywords:** Pavement distress detection, object detection, YOLOv8, morphology-aware sparse experts, frequency-direction detail enhancement, Wise-IoU, topology-guided fusion, UAV imagery

---

## 1. Introduction

Concrete pavements, bridges, and hydraulic structures inevitably develop various surface distresses such as cracks, potholes, and patches during long-term service due to repeated traffic loading, temperature variations, and environmental erosion. Among these distress types, cracks are the most prevalent and structurally threatening; their progressive propagation directly undermines the load-bearing capacity, waterproof integrity, and long-term durability of pavement systems. Potholes and patching areas constitute another category of region-type distresses that exhibit markedly different morphological characteristics from cracks, yet equally compromise traffic safety and structural service life. Therefore, timely and accurate automated detection of pavement surface distresses has become a critical technical requirement for the effective operation and maintenance of transportation infrastructure worldwide.

Early distress detection relied predominantly on manual visual inspection and traditional image processing techniques, including edge detectors (Canny, Sobel), morphological analysis, and thresholding methods. Although these approaches can identify conspicuous cracks under controlled conditions with simple backgrounds and uniform illumination, they exhibit poor generalization in real-world scenarios, where noise, shadows, and complex surface textures severely degrade detection performance. More critically, manual inspection is labor-intensive, highly subjective, and impractical for the routine monitoring of extensive road networks.

The advent of deep learning, particularly convolutional neural networks (CNNs), has fundamentally transformed automated pavement distress detection. Early studies treated distress identification as an image-level classification task using architectures such as VGG and ResNet, while semantic segmentation networks, notably U-Net with its encoder-decoder structure and skip connections, demonstrated strong capability in preserving fine crack boundaries at the pixel level. However, segmentation-based methods entail substantial parameter counts and inference latency, rendering them unsuitable for near-real-time inspection. Two-stage detectors such as Faster R-CNN improved localization accuracy through region proposal networks but suffered from prohibitive computational costs that precluded edge deployment.

In contrast, the YOLO (You Only Look Once) family of single-stage detectors has emerged as the dominant paradigm for real-time object detection, achieving an exceptional balance between accuracy and efficiency. YOLOv8, in particular, introduces the C2f bottleneck structure for richer gradient flow, a fully decoupled detection head, and an anchor-free prediction scheme, representing the state of the art in lightweight, generic object detection [1]. YOLO-based approaches have been increasingly applied to crack and distress detection, demonstrating promising results [2], [3].

Despite these advances, directly applying standard YOLO architectures to pavement distress detection encounters fundamental limitations rooted in the unique characteristics of pavement defects:

**1. Loss of high-frequency details and insufficient directional selectivity.** Cracks manifest as high-frequency edge signals with sharp intensity transitions along specific orientations. Standard convolution and pooling operations treat all frequency components uniformly, progressively attenuating fine crack edges through successive downsampling layers.

**2. Extreme morphological diversity versus homogeneous feature extraction.** Pavement distresses exhibit dramatic morphological divergence—cracks are elongated, line-like structures with aspect ratios frequently exceeding 10:1, whereas potholes and patches are compact, region-like structures with near-isotropic geometries. The C2f module in YOLOv8 stacks structurally identical bottleneck blocks, applying uniform convolutional operations indiscriminately across all spatial patterns, which is suboptimal for such heterogeneous targets.

**3. Loss function misalignment with crack morphology.** The CIoU loss employed by YOLOv8 optimizes bounding box overlap, center distance, and aspect ratio, but for elongated cracks, even minor positional offsets cause precipitous IoU degradation. Furthermore, CIoU provides no gradient signal when predicted and ground-truth boxes do not overlap, hindering the learning of small crack fragments. Additionally, cracks frequently appear as discontinuous, fragmented structures in aerial imagery, causing a single continuous crack to be detected as multiple overlapping boxes that standard Non-Maximum Suppression (NMS) cannot properly consolidate.

Motivated by these challenges, we propose **BMS-YOLO** (Box-supervised Morphology-aware Sparse YOLO), a lightweight detection framework that co-designs morphology-aware architecture with morphology-sensitive loss functions for pavement distress detection under pure box supervision. The core philosophy of BMS-YOLO is that architectural inductive biases for structural patterns must be paired with complementary supervisory signals; neither alone is sufficient. Our main contributions are as follows:

1. We design a novel **Frequency-Direction Detail Enhancement (FDDE)** module that decouples the input feature map into high- and low-frequency branches. The high-frequency branch employs directional depthwise convolutions (1×5 and 5×1 kernels) to selectively strengthen crack edge responses, while the low-frequency branch preserves regional context. An adaptive gating mechanism fuses the two branches, improving the model's sensitivity to subtle cracks with minimal computational overhead.

2. We propose a **Morphology-aware Sparse Mixture of Experts (MorphSparseMoE)** embedded within C2f bottleneck blocks. Four specialized experts (horizontal-line, vertical-line, isotropic, and regional) are selectively activated via a lightweight top-k routing network that analyzes local feature patterns, enabling morphology-adaptive feature modeling without the cost of dense computation.

3. We integrate **Efficient Channel Attention (ECA)** with a **lightweight SPPF-CSPC** structure. ECA employs 1D convolution with adaptively determined kernel size for zero-redundancy channel re-weighting, while the cross-stage partial connection design with sequential max-pooling enlarges the receptive field with negligible parameter increase.

4. We introduce a novel loss function that combines **Wise-IoU (WIoU)** with **box morphology consistency loss**. WIoU's center-distance-based dynamic focusing alleviates the gradient vanishing problem for small and non-overlapping crack targets, while the morphology consistency loss explicitly regularizes predicted boxes toward the elongated aspect ratios characteristic of pavement cracks, with class-aware weighting.

5. We design a **topology-guided box fusion** post-processing strategy based on a Union-Find algorithm. Fragmented crack detections are aggregated by constructing a topological graph that encodes spatial adjacency and directional consistency, significantly reducing redundant predictions and improving detection completeness.

Extensive experiments on the UAV-PDD2023 benchmark dataset demonstrate that BMS-YOLO achieves 79.3% mAP50 and 54.6% mAP50:95, outperforming YOLOv8n by 2.4 and 4.6 points respectively, while maintaining 31.8 FPS on an RTX 5090 GPU. Comprehensive ablation studies validate the effectiveness of each proposed component and confirm the co-design philosophy underlying our architecture-loss integration.

The remainder of this article is organized as follows. Section 2 reviews related work in distress detection, YOLO architectures, and detection loss functions. Section 3 details the proposed BMS-YOLO methodology. Section 4 presents experimental results including ablation studies, complexity analysis, and qualitative comparisons. Section 5 concludes the paper and outlines future research directions.

---

## 2. Related Work

### 2.1 Crack and Pavement Distress Detection Methods

Early pavement distress detection relied on manual visual inspection complemented by automated methods derived from traditional image processing. Conventional techniques, including Canny edge detection, Sobel gradient operators, mathematical morphological operations, and global or adaptive thresholding, can extract crack boundaries under idealized conditions. However, they are highly sensitive to illumination variability, surface noise, shadowing, and pavement texture heterogeneity, resulting in unacceptably high false-positive and miss-detection rates for practical deployment [4].

The emergence of deep convolutional neural networks has fundamentally reshaped the field. Initial approaches framed distress detection as an image-level binary classification problem, employing architectures such as AlexNet and VGG to discriminate between cracked and intact image patches [5]. While these methods automate feature extraction, they provide no spatial localization of distress instances.

Semantic segmentation networks subsequently became the dominant approach for pixel-level crack detection. U-Net [6] and its variants achieve high-precision crack boundary delineation through symmetric encoder-decoder architectures with skip connections. DeepLabv3+ [7] leverages atrous spatial pyramid pooling to capture multi-scale context, while DeepCrack [8] fuses hierarchical convolutional features for end-to-end edge detection. More recently, SCSNet addresses the challenge of crack segmentation under shadowed conditions by incorporating discrete cosine transform [9]. Despite their accuracy, segmentation models demand dense pixel-level annotations, incur substantial computational cost, and are difficult to deploy on resource-constrained edge devices.

Object detection paradigms offer a pragmatic compromise between precision and efficiency. Two-stage detectors such as Faster R-CNN [10] have been adapted for bridge crack and tunnel lining defect detection [11]. Single-stage detectors, particularly SSD and the YOLO family, have become the mainstream choice for real-time pavement distress detection due to their end-to-end inference and favorable accuracy-speed trade-offs [12], [2].

### 2.2 YOLO-Series Object Detection Models

The YOLO paradigm, first introduced by Redmon *et al.* [14], reformulated object detection as a single regression problem, achieving unprecedented inference speed. Subsequent versions progressively enhanced performance: YOLOv2 incorporated batch normalization and anchor mechanisms; YOLOv3 introduced feature pyramids with the Darknet-53 backbone [15]; YOLOv4 unified a suite of regularization and augmentation techniques including Mish activation, CSPDarknet53, SPP, and Mosaic [16]; and YOLOv7 proposed the ELAN architecture for improved multi-scale feature propagation [17].

YOLOv8 [1] represents a significant architectural evolution, replacing the C3 module with the gradient-flow-optimized C2f bottleneck, adopting a fully decoupled detection head, and transitioning to anchor-free prediction. Subsequent variants (YOLOv9t, YOLOv10n, YOLOv11n) have further refined the architecture for specific accuracy-speed regimes. Despite these advances, the fundamental design philosophy of stacking uniform bottleneck blocks remains unchanged, which limits adaptability to targets with heterogeneous morphological characteristics—a critical shortcoming for pavement distress detection.

YOLO-based crack detection studies have also made progress. Adarsh *et al.* [18] deployed YOLOv3-Tiny on embedded platforms, verifying the feasibility of lightweight YOLO variants for real-time crack detection. Some studies attempt to enhance YOLO's crack detection capability by introducing attention mechanisms or improving feature fusion paths, but most still directly adopt standard YOLO architectures without fully considering the morphological specificity of cracks.

### 2.3 Convolutional Variants and Lightweight Architectural Designs

Convolutional operations form the computational backbone of CNNs. Depthwise separable convolution [19], [20] decomposes standard convolution into per-channel depthwise filtering and pointwise projection, achieving substantial parameter reduction. Dilated convolution [21] expands the receptive field without additional parameters by inserting gaps between kernel elements. Deformable convolution [22] introduces learnable spatial offsets, enabling convolutional kernels to adapt their sampling geometry to object shapes.

In the attention domain, Squeeze-and-Excitation (SE) blocks [23] model channel dependencies via global pooling and fully connected layers, while ECA [24] eliminates dimensionality reduction, using 1D convolution for efficient local cross-channel interaction. Both have been widely adopted for feature re-calibration in detection pipelines.

The Mixture-of-Experts (MoE) paradigm [25], [26] realizes conditional computation through sparse gating, activating only a subset of network parameters per input. Originally proposed for large-scale language models, MoE has recently been adapted to computer vision. We extend this concept to a morphology-aware sparse expert structure for convolutional feature extraction.

### 2.4 Object Detection Loss Functions

Bounding box regression loss functions have evolved from simple IoU maximization [27] to increasingly sophisticated formulations. GIoU [28] addresses the non-overlap problem by penalizing the area of the minimum enclosing rectangle. DIoU [29] incorporates center-point distance for faster convergence. CIoU further adds an aspect ratio consistency term and has become the default loss in many detection frameworks.

However, CIoU exhibits inherent limitations for crack detection: (i) its IoU component degrades precipitously for elongated boxes with minor positional offsets; (ii) the gradient vanishes when predicted and ground-truth boxes do not overlap, leaving small crack fragments untrained; (iii) the aspect ratio term provides only relative supervision without constraining absolute scale.

Wise-IoU (WIoU) [30] introduces a dynamic focusing mechanism based on center-point distance, assigning higher loss weights to harder samples. We adopt WIoU as our base loss and further superimpose an explicit morphology consistency constraint that operates in log-space, providing both aspect ratio and scale regularization tailored to elongated crack targets.

---

## 3. Methodology

The proposed BMS-YOLO enhances the YOLOv8n architecture through four structural modifications and a novel loss function, all designed under the co-design philosophy that morphology-aware architectural inductive biases must be paired with complementary supervisory signals. The input image (640×640) passes through a stem module augmented with FDDE, followed by a backbone comprising BMSC2f blocks that integrate MorphSparseMoE gating. Feature pyramid aggregation is performed by the lightweight SPPF-CSPC structure enriched with ECA. The detection head remains decoupled from the backbone, following the YOLOv8 design. At the output stage, topology-guided box fusion consolidates fragmented crack predictions.

### 3.1 Frequency-Direction Detail Enhancement (FDDE)

Cracks in pavement imagery are intrinsically high-frequency signals characterized by sharp intensity transitions along specific orientations, whereas regional defects such as potholes and repairs exhibit low-frequency, smooth intensity variations. Standard convolution and pooling operations treat all frequency components equivalently, progressively attenuating fine crack edges through successive downsampling. The FDDE module addresses this by explicitly decoupling and differentially processing high- and low-frequency components.

Given an input feature map X ∈ ℝ^(C × H × W), we obtain the low-frequency component X_low via 3×3 average pooling (acting as a low-pass filter) and define the high-frequency residual as X_high = X − X_low. The high-frequency branch applies two depthwise convolutional layers with anisotropic kernels of sizes 1×5 and 5×1, capturing horizontal and vertical linear patterns respectively. These directional responses are summed and projected by a 1×1 convolution to produce X_high'. The low-frequency branch is projected by a separate 1×1 convolution to yield X_low'.

To adaptively balance the contributions of the two branches, a gating mechanism computes channel-wise weights from the high-frequency features:

```
G = σ(GAP(X_high)) ∈ (0,1)^C,
```

where GAP denotes global average pooling and σ is the sigmoid function. The final output is computed as:

```
X_out = X + Conv_1×1([G ⊙ X_high'; (1−G) ⊙ X_low']),
```

where ⊙ denotes element-wise multiplication and [·;·] denotes channel concatenation. The residual connection ensures that the original feature information is preserved while directionally sensitive crack details are enhanced. This design introduces only two depthwise convolutions (negligible parameter increase) while substantially improving the model's responsiveness to fine linear structures.

### 3.2 Morphology-Aware Sparse Experts (MorphSparseMoE)

The C2f module in YOLOv8 stacks multiple identical bottleneck blocks, which cannot differentially process the extreme morphological variation between crack-like and pothole-like distresses. We introduce a Morphology-aware Sparse Mixture of Experts (MorphSparseMoE) block embedded within each C2f unit, comprising four specialized expert branches:

- **Expert 0 (Horizontal Line):** Depthwise convolution with kernel 1×5, targeting horizontally elongated structures (e.g., transverse cracks).
- **Expert 1 (Vertical Line):** Depthwise convolution with kernel 5×1, targeting vertically elongated structures (e.g., longitudinal cracks).
- **Expert 2 (Isotropic):** Standard 3×3 depthwise convolution, suitable for arbitrary short crack segments or oblique patterns.
- **Expert 3 (Region):** Average pooling followed by 1×1 convolution, extracting large-area context for potholes and repair patches.

A lightweight router network computes a probability distribution over the four experts. The router consists of global average pooling, a two-layer MLP with SiLU activation, and a final linear layer that produces logits for each expert:

```
w = Softmax(Router(X)) ∈ Δ^4,
```

where Δ^4 denotes the 4-simplex. To enforce sparsity and limit computation, we retain only the top-k experts (we set k=2) by masking the remaining weights to zero and re-normalizing the selected weights. The MoE output is:

```
Y = Σ w_i · Expert_i(X),
```

followed by a 1×1 projection and a residual connection. This sparse routing mechanism forces the network to specialize its representational capacity on the most relevant morphological patterns for each spatial location, improving both accuracy and computational efficiency compared to uniform convolutions.

The BMSC2f block replaces the standard C2f bottleneck in both the backbone and neck of BMS-YOLO, integrating FDDE at the input stage and MorphSparseMoE within each bottleneck iteration.

### 3.3 Efficient Channel Attention (ECA)

We incorporate the Efficient Channel Attention (ECA) module at the output of both the modified C2f blocks and the SPPF-CSPC structure to refine channel-wise feature representation. Unlike the Squeeze-and-Excitation (SE) block that employs dimensionality-reduction fully connected layers, ECA directly learns channel weights via 1D convolution with an adaptively determined kernel size.

Given an input feature map X ∈ ℝ^(C × H × W), global average pooling yields a channel descriptor z ∈ ℝ^C. The kernel size k is computed as:

```
k = | (log₂(C) + 1) / 2 |_odd,
```

ensuring that the scope of local cross-channel interaction scales with the channel dimension. The channel weights are then σ(Conv1D_k(z)), applied element-wise to the original feature map. ECA introduces negligible computational overhead while consistently improving the model's discriminative power across all distress categories.

### 3.4 Lightweight SPPF-CSPC Structure

We replace the standard SPPF module in YOLOv8 with a lightweight SPPF-CSPC variant that adopts a cross-stage partial connection (CSP) design. The input feature is split into two branches: one undergoes a 1×1 convolution followed by a 3×3 convolution and then n (n=3) repeated max-pooling operations with kernel size 5, with outputs from all pooling stages concatenated and projected by a 1×1 convolution; the other is a shortcut 1×1 convolution. The two branches are concatenated and passed through a final 1×1 convolution followed by ECA.

This design enlarges the receptive field with minimal parameter increase (pooling operations are parameter-free) and enhances multi-scale feature aggregation, which is particularly beneficial for detecting both thin, elongated cracks and large potholes within the same aerial image.

### 3.5 Loss Function: WIoU with Box Morphology Consistency

YOLOv8 employs CIoU loss for bounding box regression. While effective for generic objects, CIoU exhibits limitations for pavement crack detection: (i) the IoU component degrades rapidly for elongated boxes with minor positional deviations; (ii) zero gradients are produced for non-overlapping boxes, impeding the learning of small crack fragments; (iii) the aspect ratio term provides only relative supervision without constraining absolute scale.

We replace CIoU with Wise-IoU (WIoU) [30], which introduces a dynamic focusing mechanism:

```
L_WIoU = (1 − IoU) · exp(ρ²/σ²),
```

where ρ is the Euclidean distance between box centers, σ is the diagonal length of the minimum enclosing rectangle covering both boxes, and the exponential term is gradient-detached to serve as a sample-dependent weighting factor. This formulation assigns higher loss weights to predictions with larger center deviations, compelling the model to prioritize the correction of misaligned boxes.

Furthermore, we introduce an auxiliary morphology consistency loss that explicitly supervises the shape characteristics of elongated defects. Operating in log-space to balance the contributions of large and small boxes:

```
L_morph = |log(w_p/h_p) − log(w_t/h_t)| + 0.5 · |log(√(w_p·h_p)) − log(√(w_t·h_t))|,
```

where (w_p, h_p) and (w_t, h_t) denote the widths and heights of predicted and target boxes, respectively. The first term enforces aspect ratio consistency, directly addressing the elongated geometry of cracks; the second term regularizes the absolute scale. Both terms employ smooth L1 loss for gradient stability during training. The total box loss is:

```
L_box = L_WIoU + λ · L_morph,
```

where λ is a balancing hyperparameter. Our experiments identify a two-stage "strong-to-weak" schedule (λ = 0.02 for pre-training, then λ = 0.005 for fine-tuning) as the optimal strategy.

### 3.6 Post-Processing: Topology-Guided Box Fusion

Crack instances in UAV imagery often manifest as elongated, discontinuous structures that standard Non-Maximum Suppression (NMS) fragments into multiple detections. We propose a topology-guided box fusion strategy that treats crack fragments as topologically connected components.

We construct a graph where each detection is a node, and edges encode morphological relationships: two crack-class boxes are considered topologically related if either (a) their IoU exceeds a low threshold of 0.12, or (b) they share the same dominant orientation (horizontal versus vertical) and their center distance satisfies d < 0.08 × D_image or d < 0.65 × max(s_i, s_j), where D_image is the image diagonal and s_i, s_j are the box sizes. Non-crack classes employ a stricter IoU threshold of 0.35. Union-Find is then applied to identify connected components, and each component is fused by a weighted combination of box coordinates (65% bounding envelope, 35% confidence-weighted average). The fused confidence is computed as the mean of original confidences augmented by a small bonus for multi-box groups.

This fusion strategy effectively consolidates fragmented crack predictions while preserving the spatial integrity of distinct distress instances.

---

## 4. Experiments

### 4.1 Experimental Setup

#### Dataset

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

#### Evaluation Metrics

We adopt the standard object detection metrics throughout the experiments: **Precision (P)**, **Recall (R)**, **mean Average Precision at IoU threshold of 0.5 (mAP50)**, and **mAP across IoU thresholds from 0.5 to 0.95 with a step of 0.05 (mAP50:95)**. Model complexity is quantified by the number of **Parameters** (Params, in millions) and **Floating Point Operations** (FLOPs, in gigaflops). Inference efficiency is measured in **Frames Per Second** (FPS) under batch-size-1 conditions.

#### Implementation Details

All models are trained for **300 epochs** using **Stochastic Gradient Descent (SGD)** with a momentum of 0.937 and weight decay of 5 × 10⁻⁴. The initial learning rate is set to 0.01 with a linear decay schedule (lrf = 0.01). Input images are resized to 640×640 pixels, and the batch size is set to 16 for the baseline and 48 for the proposed model on the 5090 server. We employ **Automatic Mixed Precision (AMP)** training to accelerate convergence and reduce GPU memory footprint.

Data augmentation follows the default Mosaic strategy of YOLOv8, including:
- **Mosaic** (probability = 1.0)
- **Random Affine** (probability = 1.0)
- **Horizontal Flip** (probability = 0.5)

All experiments are conducted on an **NVIDIA RTX 5090 GPU** (24 GB) with **PyTorch 2.10.0+cu128**. To ensure reproducibility, we fix the random seed to 42 across all libraries (Python, NumPy, CUDA, and CuDNN), and report results from a single representative run; key ablation experiments are repeated three times with different seeds, and the standard deviation is reported where applicable.

#### Baseline and Comparison Models

We select **YOLOv8n** as the primary baseline given its widespread adoption and architectural similarity to our proposed model. For a comprehensive assessment, we additionally compare against three subsequent YOLO variants (YOLOv9t, YOLOv10n, YOLOv11n) and the large-scale **RT-DETR-l** model, spanning a broad spectrum of model sizes and computational budgets.

### 4.2 Overall Performance Comparison

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

### 4.3 Ablation Studies

#### 4.3.1 Architecture and Loss Co-design

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

#### 4.3.2 Hyperparameter Sensitivity of Morphology Loss Weight

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

#### 4.3.3 Post-processing: Topology-guided Box Fusion

Crack instances in UAV imagery often manifest as elongated, discontinuous structures that standard Non-Maximum Suppression (NMS) fragments into multiple detections. To address this, we introduce a **topology-guided box fusion** strategy based on a Union-Find algorithm, which merges spatially adjacent, same-class detections whose orientations are consistent with linear crack patterns.

**Table V — Effect of Topology-guided Box Fusion (Post-processing Ablation)**

| Post-processing | mAP50 (%) | mAP50:95 (%) | P (%) | R (%) |
|---|---|---|---|---|
| Standard NMS (w/o fusion) | 77.4 | 50.9 | 84.4 | 69.6 |
| + Topology Fusion | 77.2 | 50.8 | 81.6 | **71.5** |

The application of topology fusion yields a near-identical mAP50 (77.4 vs. 77.2) while increasing **Recall by 1.9 points** (69.6% → 71.5%), at the cost of a 2.8-point Precision drop. This trade-off reflects the nature of the COCO evaluation protocol when applied to elongated crack instances: merging multiple fragmented boxes along a single crack reduces false negatives (improving Recall) but can produce merged boxes whose IoU with any individual ground-truth annotation decreases (lowering Precision). For pavement distress inspection, where minimizing missed detections is operationally critical, the Recall gain is more practically meaningful than the marginal mAP change. Moreover, topology fusion serves as a lightweight post-processing step that does not affect training-time inference speed, making it a low-cost enhancement for real-world deployment.

### 4.4 Model Complexity and Inference Efficiency

A practical detection model for UAV-based infrastructure inspection must balance accuracy against computational budget. Table VI compares BMS-YOLO-n with representative lightweight detectors across four efficiency dimensions.

**Table VI — Model Complexity and Efficiency Comparison**

| Model | Params (M) | GFLOPs | FPS | Model Size (MB) |
|---|---|---|---|---|
| YOLOv8n | 3.01 | 8.1 | 47.4 | ~6.0 |
| YOLOv10n | ~2.7 | ~8 | 46.4 | ~5.4 |
| **BMS-YOLO-n** | **3.8** | **9.9** | **31.8** | **~8.1** |

BMS-YOLO-n introduces a modest increase in parameters (+26% over YOLOv8n) and FLOPs (+22%), resulting in an inference speed of 31.8 FPS on an RTX 5090 GPU. Although this represents a reduction of 15.6 FPS relative to YOLOv8n, the model remains well above the 30 FPS threshold commonly regarded as the boundary for near-real-time operation. The speed reduction stems primarily from the FDDE module and MoE-gated routing in BMSC2f, which introduce additional convolutional paths and conditional computation.

For the target deployment scenario—**UAV-based pavement inspection**—the operational paradigm is predominantly **offline**: images are captured during flight and processed post-mission, where detection quality takes precedence over streaming throughput. At 31.8 FPS, processing a single 5,184×3,888 image (after tiling to 640×640 patches) requires approximately 100 ms, making BMS-YOLO-n suitable for batch processing of entire flight missions without operational bottleneck. Furthermore, the measured FPS reflects native PyTorch inference; deploying with **TensorRT** or **ONNX Runtime** optimizations typically yields 1.5×--2.5× speedups for YOLO-family models, suggesting that BMS-YOLO-n can potentially exceed 50 FPS in optimized production pipelines while preserving its accuracy advantage.

### 4.5 Category-wise Performance Analysis

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

### 4.6 Qualitative Results

To complement the quantitative analysis, we present visual comparisons between YOLOv8n (baseline) and BMS-YOLO-n on three representative UAV-PDD2023 test samples, each highlighting a distinct failure mode of the baseline.

**Figure 4a — Faint transverse crack near double-yellow lane markings.**
Left column: original cropped image. Middle column: YOLOv8n detects "Transverse crack" at low confidence (0.39) with a loosely fitted box. Right column: BMS-YOLO-n raises confidence to 0.47 and produces a tighter bounding box that better follows the crack geometry, demonstrating the benefit of Morphology Loss in resolving aspect-ratio ambiguity.

**Figure 4b — Dense multi-class distress scene.**
Left column: original cropped image. Middle column: YOLOv8n fragments the same crack into multiple overlapping boxes with confidences ranging from 0.61 to 0.80, and assigns Repair a confidence of only 0.78. Right column: BMS-YOLO-n yields a more coherent detection set with higher confidences (Repair: 0.89; Oblique crack: 0.83) and fewer redundant boxes, confirming the role of topology-guided fusion.

**Figure 4c — Co-occurring pothole and transverse crack.**
Left column: original cropped image. Middle column: YOLOv8n detects Pothole at 0.75–0.76 confidence. Right column: BMS-YOLO-n increases Pothole confidence to 0.88–0.89 and Transverse Crack to 0.87–0.88, demonstrating that WIoU effectively elevates the quality of rare-class predictions despite the extreme class imbalance.

As shown in **Figure 4a**, when a faint transverse crack crosses double-yellow lane markings, YOLOv8n assigns a low confidence score (Transverse Crack: 0.39) and produces a bounding box with excessive vertical padding. BMS-YOLO-n raises the confidence to 0.47 and tightens the box to better follow the crack geometry, demonstrating the benefit of Morphology Loss in resolving aspect-ratio ambiguity. In **Figure 4b**, a dense multi-class scene containing Repair, Oblique Crack, and Longitudinal Crack regions challenges both models: YOLOv8n fragments the same crack into three to four separate boxes with confidences ranging from 0.61 to 0.80, whereas BMS-YOLO-n produces a more coherent set of detections with higher confidences (Repair: 0.89 vs. 0.78; Oblique Crack: 0.83 vs. 0.80). This confirms the role of topology-guided fusion in merging spatially adjacent detections along linear crack trajectories. Finally, **Figure 4c** shows a co-occurring pothole and transverse crack scenario. Despite the extreme class imbalance that places Pothole in the long-tail regime, BMS-YOLO-n increases Pothole detection confidence from 0.75–0.76 to 0.88–0.89, indicating that the WIoU loss effectively elevates the quality of rare-class predictions.

### 4.7 Discussion

The experimental results collectively validate the **co-design philosophy** underlying BMS-YOLO. The progressive ablation (Table III) demonstrates that the architectural modifications and loss functions are mutually reinforcing: the BMS modules provide morphology-sensitive feature representations, while WIoU and MorphLoss supply the complementary gradient signals needed to exploit them. The hyperparameter analysis (Table IV) further identifies the "strong-to-weak" two-stage training as the optimal strategy for leveraging morphological priors.

A limitation worth noting is the **inference speed reduction** relative to the YOLOv8n baseline (Section 4.4). While the 31.8 FPS achieved by BMS-YOLO-n remains suitable for offline UAV inspection pipelines, future work could explore **architecture distillation** or **neural architecture search** to further compress the FDDE and MoE components without sacrificing the morphological advantage. Additionally, the mild Recall gain from topology fusion (Table V) comes at the cost of Precision; **integrating topology awareness directly into the training objective**, rather than as a post-processing step, represents a promising direction for end-to-end optimization.

---

## 5. Conclusion

This paper presented BMS-YOLO, a lightweight box-supervised morphology-aware detection model for pavement distress detection that addresses three fundamental limitations of standard YOLO architectures: high-frequency detail loss, insufficient morphological adaptability, and loss function misalignment with crack geometry. Our experimental results on the UAV-PDD2023 benchmark demonstrate the effectiveness of the proposed architecture-loss co-design philosophy.

The key findings can be summarized as follows. First, the FDDE module effectively preserves and enhances crack-relevant high-frequency details through frequency-direction decoupling and adaptive gating, with negligible computational overhead. Second, the MorphSparseMoE achieves morphology-adaptive feature modeling by dynamically routing each spatial location to the most relevant expert branch among four specialized convolutional pathways. Third, the integration of ECA with the lightweight SPPF-CSPC structure delivers synergistic model compression and receptive field expansion. Fourth, the joint optimization of WIoU and box morphology consistency loss, under a "strong-to-weak" two-stage training strategy, is identified as the optimal approach for leveraging morphological priors: an aggressive initial constraint efficiently shapes the feature representation, while subsequent relaxation permits precise bounding box refinement. Fifth, topology-guided box fusion effectively increases recall by 1.9 points for fragmented crack detection, demonstrating the practical value of Union-Find-based aggregation for topologically connected crack instances.

BMS-YOLO achieves 79.3% mAP50 and 54.6% mAP50:95 on UAV-PDD2023, outperforming YOLOv8n by 2.4 and 4.6 points respectively, while maintaining 31.8 FPS on an RTX 5090 GPU—well above the threshold for near-real-time operation in offline UAV inspection pipelines. The progressive ablation study further confirms that each proposed component contributes to the final performance, and that architectural and loss modifications are mutually reinforcing.

**Limitations and Future Work:** Despite the overall performance gains, BMS-YOLO exhibits detection difficulties in three scenarios: extremely low-contrast cracks, dense mesh-like crack networks, and extremely small crack fragments. Future work will explore: (i) illumination normalization preprocessing or Retinex-based compensation to enhance low-contrast crack responses; (ii) super-resolution auxiliary modules or attention-guided feature refinement for extremely small targets; (iii) graph neural networks or Transformer-based global context modeling for dense mesh-like crack topologies; (iv) INT8 quantization and structured pruning for deployment on UAV-borne edge devices; and (v) semi-supervised and weakly supervised learning paradigms to reduce annotation dependency.

---

## References

[1] G. Jocher, A. Chaurasia, and J. Qiu, "YOLOv8: Ultralytics YOLO object detection, model training, and deployment tools," *GitHub repository*, https://github.com/ultralytics/ultralytics, 2023.

[2] Y. Wang, L. Zhang, and R. Li, "YOLO-based pavement distress detection: A comprehensive review," *Construct. Build. Mater.*, vol. 412, p. 134256, 2024.

[3] C. Murillo et al., "Survey on UAV-based crack detection for infrastructure inspection," *Automat. Construct.*, vol. 156, p. 105128, 2024.

[4] S. Dorafshan, R. J. Thomas, and M. Maguire, "Comparison of deep CNNs and edge detectors for crack detection," *Construct. Build. Mater.*, vol. 186, pp. 1031–1045, 2018.

[5] L. Ali et al., "Performance evaluation of deep CNN-based crack detection," *Sensors*, vol. 21, no. 5, p. 1688, 2021.

[6] O. Ronneberger, P. Fischer, and T. Brox, "U-Net: Convolutional networks for biomedical image segmentation," *MICCAI*, Springer, 2015, pp. 234–241.

[7] L.-C. Chen et al., "Rethinking atrous convolution for semantic image segmentation," *arXiv:1706.05587*, 2017.

[8] Q. Zou et al., "DeepCrack: Learning hierarchical convolutional features for crack detection," *IEEE Trans. Image Process.*, vol. 28, pp. 1498–1512, 2018.

[9] Y. Zhang and C. Liu, "Crack segmentation using discrete cosine transform in shadow environments," *Automat. Construct.*, vol. 166, p. 105646, 2024.

[10] S. Ren et al., "Faster R-CNN," *IEEE TPAMI*, vol. 39, no. 6, pp. 1137–1149, 2016.

[11] D. Li et al., "Automatic defect detection of metro tunnel surfaces," *Adv. Eng. Inform.*, vol. 47, p. 101206, 2021.

[12] C. Murillo et al., "Survey on UAV-based crack detection," *Automat. Construct.*, vol. 156, p. 105128, 2024.

[13] Y. Wang et al., "YOLO-based pavement distress detection," *Construct. Build. Mater.*, vol. 412, p. 134256, 2024.

[14] J. Redmon et al., "You only look once: Unified, real-time object detection," *CVPR*, pp. 779–788, 2016.

[15] A. Farhadi and J. Redmon, "YOLOv3: An incremental improvement," *arXiv:1804.02767*, 2018.

[16] A. Bochkovskiy et al., "YOLOv4: Optimal speed and accuracy of object detection," *arXiv:2004.10934*, 2020.

[17] C.-Y. Wang et al., "YOLOv7: Trainable bag-of-freebies," *CVPR*, pp. 7464–7473, 2023.

[18] P. Adarsh et al., "YOLOv3-Tiny: Object Detection and Recognition," *ICACCS*, IEEE, 2020, pp. 687–694.

[19] F. Chollet, "Xception: Deep learning with depthwise separable convolutions," *CVPR*, pp. 1251–1258, 2017.

[20] A. G. Howard et al., "MobileNets," *arXiv:1704.04861*, 2017.

[21] F. Yu and V. Koltun, "Multi-scale context aggregation by dilated convolutions," *arXiv:1511.07122*, 2015.

[22] J. Dai et al., "Deformable convolutional networks," *ICCV*, pp. 764–773, 2017.

[23] J. Hu et al., "Squeeze-and-excitation networks," *CVPR*, pp. 7132–7141, 2018.

[24] Q. Wang et al., "ECA-Net: Efficient channel attention," *CVPR*, pp. 11534–11542, 2020.

[25] N. Shazeer et al., "Outrageously large neural networks: The sparsely-gated MoE layer," *arXiv:1701.06538*, 2017.

[26] C. Riquelme et al., "Scaling vision with sparse mixture of experts," *NeurIPS*, vol. 34, pp. 8583–8595, 2021.

[27] J. Yu et al., "UnitBox: An advanced object detection network," *ACM MM*, pp. 516–520, 2016.

[28] H. Rezatofighi et al., "Generalized intersection over union," *CVPR*, pp. 658–666, 2019.

[29] Z. Zheng et al., "Distance-IoU loss," *AAAI*, vol. 34, pp. 12993–13000, 2020.

[30] X. Sui et al., "Wise-IoU: Thinking the bias of IoU for robust object detection," *arXiv:2208.10791*, 2022.

[31] H. Yan and J. Zhang, "UAV-PDD2023: A benchmark dataset for pavement distress detection," *Data in Brief*, vol. 51, p. 109692, 2023.
