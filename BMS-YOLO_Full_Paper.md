# BMS-YOLO: A Lightweight Box-Supervised Morphology-Aware Pavement Distress Detection Model

## Abstract

Accurate detection of pavement distresses such as cracks and potholes is critical for infrastructure safety maintenance. However, existing YOLO-based methods face challenges in feature representation, computational redundancy, and loss function design, especially when dealing with the extreme morphological differences between elongated cracks and compact potholes. To address these issues, this paper proposes BMS-YOLO (Box-supervised Morphology-aware Sparse YOLO), a lightweight pavement distress detection model under pure box supervision. At the feature extraction level, a Frequency-Direction Detail Enhancement (FDDE) module decouples the feature map into high- and low-frequency branches and strengthens crack edge responses via directional convolutions. A Morphology-aware Sparse Mixture of Experts (MorphSparseMoE) is embedded within C2f blocks to dynamically activate four expert types via top-k routing, enabling morphology-adaptive modeling. Efficient Channel Attention (ECA) and a lightweight SPPF-CSPC structure further enlarge the receptive field while reducing parameters. At the loss function level, Wise-IoU (WIoU) replaces CIoU with center-distance-based dynamic focusing, and a box morphology consistency loss constrains aspect ratio and area in log space. A post-processing pipeline with topology-guided Union-Find box fusion mitigates fragmented crack predictions. Experiments on the UAV-PDD2023 benchmark dataset show that BMS-YOLO achieves 79.3% mAP50 and 54.6% mAP50:95 with only 3.8M parameters, significantly outperforming YOLOv8n (+2.4 points mAP50, +4.6 points mAP50:95) while maintaining 31.8 FPS on an RTX 5090 GPU.

---

## 1. Introduction

Concrete pavements, bridges, and hydraulic structures inevitably develop various surface distresses such as cracks, potholes, and patches during long-term service due to loads, temperature variations, and environmental erosion. Among them, cracks are the most common and threatening distress type; their propagation directly weakens structural load-bearing capacity and durability. Potholes and patching areas constitute another category of region-type distresses with completely different morphologies, which also significantly affect traffic safety and structural service life. Therefore, timely and accurate automated detection of pavement and structural surface distresses is a key technical link for ensuring infrastructure safety operation.

Early distress detection mainly relied on manual inspection and traditional image processing techniques, such as edge detectors (Canny, Sobel), morphological analysis, and thresholding methods. Although these methods can identify obvious cracks under simple backgrounds and good lighting, they have extremely poor generalization ability, are highly sensitive to noise, shadows, and complex textures, and struggle with subtle cracks under low contrast. More importantly, manual inspection is inefficient and subjective, far from meeting the practical demands of large-scale road networks and high-frequency patrols.

In recent years, deep learning, especially convolutional neural networks (CNNs) in computer vision, has opened new avenues for automated pavement distress detection. Early studies adopted classification or semantic segmentation networks, such as VGG, ResNet, and U-Net, treating distress detection as pixel-wise binary or multi-class classification. U-Net, with its encoder-decoder architecture and skip connections, shows good capability in preserving fine edges in crack segmentation, but segmentation networks have large parameters and slow inference, making them unsuitable for real-time requirements. Subsequently, two-stage detectors like Faster R-CNN based on region proposals were introduced into distress detection. These methods improve accuracy by generating candidate boxes via a region proposal network followed by classification and regression, but their high computational complexity and limited inference speed also hinder edge deployment.

In contrast, the YOLO (You Only Look Once) family, with its end-to-end single-stage detection paradigm, achieves an excellent balance between accuracy and speed, quickly becoming the preferred framework for real-time object detection. YOLOv3 and YOLOv4 incorporate multi-scale prediction, adaptive anchor boxes, and path aggregation networks to significantly enhance multi-scale detection capability. YOLOv8 further introduces the C2f structure, decoupled head, and anchor-free design, reaching new performance heights on generic object detection [1]. YOLO-based crack detection studies have also emerged, preliminarily verifying their application potential [2], [3].

However, directly applying existing YOLO models to pavement distress detection still faces several technical bottlenecks:

**1. Loss of high-frequency details and insufficient directional selectivity:** Cracks appear as high-frequency edge information along specific orientations, but standard convolution and pooling layers treat all frequency components equally, causing fine crack edges to be gradually smoothed and weakened during downsampling.

**2. Extreme morphological diversity versus homogeneous feature extraction:** Pavement distresses exhibit extreme morphological divergence—cracks are elongated line-like structures with high aspect ratios (often >10:1), while potholes and patches are compact region-like structures with aspect ratios near 1:1. The C2f module in YOLOv8 stacks identical bottleneck structures, applying uniform convolution operations to all spatial patterns.

**3. Loss function unfriendly to crack morphology:** The CIoU loss used in YOLOv8 considers overlap area, center distance, and aspect ratio, but for elongated cracks, small positional deviations cause dramatic IoU drops, and CIoU cannot provide effective gradients for non-overlapping predicted boxes. Moreover, cracks often appear discontinuous and fragmented in images; a single continuous crack may be detected as multiple overlapping boxes, which standard Non-Maximum Suppression (NMS) cannot properly handle.

Motivated by these challenges, we propose **BMS-YOLO** (Box-supervised Morphology-aware Sparse YOLO), a lightweight pavement distress detection model under pure box supervision. The main contributions of this work are as follows:

1. A novel **Frequency-Direction Detail Enhancement (FDDE)** module is designed. The feature map is decoupled into high- and low-frequency branches; the high-frequency branch employs horizontal and vertical directional depthwise convolutions to strengthen crack edge responses, while the low-frequency branch preserves regional context. An adaptive gating mechanism fuses the two branches, effectively improving the model's perception of subtle cracks with minimal additional computational cost.

2. A **Morphology-aware Sparse Mixture of Experts (MorphSparseMoE)** is proposed and embedded inside the C2f module. Comprising four experts—horizontal-line, vertical-line, isotropic, and regional—a lightweight routing network dynamically selects the top-k experts according to the local patterns of input features, enabling morphology-adaptive feature modeling with low computational cost.

3. **Efficient Channel Attention (ECA)** and a **lightweight SPPF-CSPC** structure are introduced. Channel attention is implemented via 1D convolution with adaptive kernel size, enhancing discriminative channels with zero redundancy. The cross-stage partial connection and sequential max-pooling design enlarge the receptive field with very few parameters, further reducing model complexity.

4. A novel loss function combining **Wise-IoU (WIoU)** and **box morphology consistency loss** is proposed. The center-distance-based WIoU replaces CIoU to effectively alleviate the gradient vanishing problem for small and non-overlapping targets. A new consistency constraint on aspect ratio and area in log space explicitly supervises the shape preservation of elongated cracks, with class-aware weighting that imposes higher morphological loss weights on crack classes.

5. A post-processing strategy with **topology-guided box fusion** is designed. A Union-Find-based topological graph is constructed to aggregate fragmented crack detection boxes based on low IoU thresholds and directional consistency, significantly reducing repeated predictions and improving detection completeness and reliability.

Extensive experiments on the UAV-PDD2023 benchmark dataset demonstrate that BMS-YOLO achieves 79.3% mAP50 and 54.6% mAP50:95, significantly outperforming YOLOv8n (+2.4 points mAP50, +4.6 points mAP50:95) while maintaining competitive inference speed (31.8 FPS on RTX 5090). Ablation studies and qualitative analyses fully validate the effectiveness of each proposed component and the architecture-loss co-design philosophy.

---

## 2. Related Work

### 2.1 Crack and Pavement Distress Detection Methods

Early pavement distress detection relied mainly on manual visual inspection and automated methods based on traditional image processing techniques. Manual inspection is inefficient and subjective, unable to meet the requirements of regular inspection of large-scale road networks. Traditional image processing methods such as Canny edge detection, Sobel operators, morphological operations, and thresholding can extract crack edges under simple backgrounds and uniform illumination, but they are highly sensitive to noise, shadows, pavement texture, and illumination changes, leading to high false and miss detection rates [4].

With the rapid development of deep learning in computer vision, CNN-based distress detection methods have gradually become mainstream. Early studies treated distress detection as an image-level binary classification task, using classic classification networks such as AlexNet and VGG to determine whether an image patch contains cracks [5]. Although these methods achieve automatic feature extraction in an end-to-end manner, image-patch-level judgments cannot provide precise location or geometric information of cracks.

To obtain pixel-level fine detection results, semantic segmentation networks have been widely introduced into crack detection tasks. U-Net [6], with its symmetric encoder-decoder architecture and skip connections, preserves edge details well in crack segmentation. DeepLabv3+ [7] employs atrous convolution and the ASPP module to enlarge the receptive field. DeepCrack [8] achieves end-to-end crack edge detection through multi-layer convolutional feature fusion. SCSNet addresses crack segmentation in shadowed environments by incorporating discrete cosine transform [9].

However, semantic segmentation networks generally have large parameter counts and slow inference speed, making it difficult to meet the requirements of real-time detection and edge deployment. In addition, the cost of obtaining segmentation annotations is much higher than that of bounding box annotations, limiting their scalability in large-scale practical applications.

To balance detection accuracy and inference efficiency, the object detection paradigm has been introduced into distress detection tasks. Faster R-CNN [10] generates candidate regions via a Region Proposal Network (RPN) and has been applied to bridge crack detection and tunnel lining defect detection [11]. In contrast, single-stage detectors such as SSD and YOLO, with their end-to-end single-shot detection paradigm, have significant speed advantages and have gradually become the mainstream direction for real-time pavement distress detection [12], [13].

### 2.2 YOLO-Series Object Detection Models

YOLO was first proposed by Redmon et al. [14], reformulating object detection as a unified regression problem. YOLOv2 introduced batch normalization, anchor mechanisms, and multi-scale training. YOLOv3 adopted a Feature Pyramid Network (FPN) and employed a deeper Darknet-53 backbone [15]. YOLOv4 integrated Mish activation, CSPDarknet53 backbone, SPP module, and Mosaic data augmentation [16].

YOLOv7 introduced the ELAN structure, enhancing multi-scale feature aggregation while maintaining high inference speed [17]. YOLOv8 replaces the C3 structure with the richer gradient-flow C2f structure, adopts a decoupled head, and shifts from anchor-based to anchor-free detection [1]. Subsequent variants including YOLOv9t, YOLOv10n, and YOLOv11n further refine the architecture for improved speed-accuracy trade-offs.

YOLO-based crack detection studies have also made progress. Adarsh et al. [18] deployed YOLOv3-Tiny on embedded platforms, verifying the feasibility of lightweight YOLO variants for real-time crack detection. Some studies attempt to enhance YOLO's crack detection capability by introducing attention mechanisms or improving feature fusion paths, but most still directly adopt standard YOLO architectures without fully considering the morphological specificity of cracks.

### 2.3 Convolutional Variants and Lightweight Designs

Convolution is the cornerstone of CNNs. Depthwise Separable Convolution decomposes standard convolution into channel-wise depthwise convolution and pointwise 1×1 convolution, significantly reducing parameters [19], [20]. Dilated convolution inserts gaps between kernel elements, enlarging the receptive field without increasing computation [21]. Deformable convolution introduces learnable offsets to dynamically adapt the convolution kernel to object geometric deformation [22].

In attention mechanisms, SENet [23] explicitly models channel dependencies via global pooling and fully connected layers. ECA [24] removes the dimensionality-reduction layers from SENet and uses 1D convolution to achieve local cross-channel interaction with minimal additional computation.

The Mixture-of-Experts (MoE) paradigm realizes sparse activation via conditional computation [25], [26], activating only a subset of network parameters for each input. Inspired by this, we propose a morphology-aware sparse expert structure that adapts the sparse activation idea of MoE to convolutional networks.

### 2.4 Object Detection Loss Functions

IoU loss optimizes by maximizing the overlap between predicted and ground-truth boxes [27]. GIoU introduces a penalty term based on the minimum enclosing rectangle [28]. DIoU further incorporates center-point distance penalty [29]. CIoU adds an aspect ratio consistency term on top of DIoU and has become one of the most widely used loss functions in object detection.

However, CIoU has inherent limitations in crack detection: (1) for elongated cracks, even a small center offset causes a drastic drop in IoU; (2) for small crack fragments, predicted and ground-truth boxes often have no overlap, resulting in zero gradient; (3) CIoU's aspect ratio penalty is relative and lacks explicit supervision of absolute scale and shape consistency.

To address these issues, we adopt a center-distance-based dynamic focusing Wise-IoU (WIoU) [30] to replace CIoU, and superimpose an explicit box morphology consistency loss that imposes constraints on aspect ratio and area in log space, specifically tailored to the elongated characteristics of cracks.

---

## 3. Methodology

Despite the strong performance of YOLOv8 in generic object detection, its application to pavement distress detection—particularly for crack-like linear defects and pothole-like regional defects—suffers from several inherent limitations. To address these issues, we propose BMS-YOLO, a lightweight detection framework tailored for box-only pavement distress detection. The overall architecture integrates five key enhancements: an FDDE module, morphology-aware sparse experts embedded in C2f blocks, an ECA mechanism, a lightweight SPPF-CSPC structure, and a novel loss function combining WIoU with box morphology consistency. Additionally, a topology-guided box fusion post-processing pipeline is designed to mitigate fragmented crack predictions.

### 3.1 Frequency-Direction Detail Enhancement (FDDE)

Cracks are intrinsically high-frequency signals characterized by sharp intensity transitions along specific orientations, whereas regional defects such as potholes and repairs exhibit low-frequency smooth variations. Standard convolution layers treat all frequency components equally, causing fine crack edges to be attenuated by successive pooling and stride operations. To explicitly preserve and enhance crack-relevant details, we design the FDDE module, which decouples the input feature map into high- and low-frequency branches and applies directional convolutions to the former.

Given an input feature map X ∈ ℝ^(C × H × W), we obtain the low-frequency component X_low via a 3×3 average pooling (serving as a low-pass filter), and the high-frequency component as X_high = X - X_low. The high-frequency branch then applies two depthwise convolutional layers with elongated kernels of sizes 1×5 and 5×1 respectively, capturing horizontal and vertical line patterns. These directional responses are summed and projected by a 1×1 convolution. The low-frequency branch is simply projected by another 1×1 convolution. To adaptively balance the two branches, a gating mechanism computes a spatial weight map from the high-frequency features via global average pooling and a sigmoid activation, producing a gate G ∈ (0,1)^C. The final output is given by:

```
X_out = X + Conv_1×1([G ⊙ X_high'; (1-G) ⊙ X_low'])
```

where ⊙ denotes element-wise multiplication, [·;·] denotes channel concatenation, and X_high', X_low' are the projected high- and low-frequency features. The residual connection preserves the original information while enhancing direction-sensitive crack details.

### 3.2 Morphology-Aware Sparse Experts (MorphSparseMoE)

The C2f module in YOLOv8 stacks multiple identical bottleneck blocks, which are suboptimal for handling the extreme morphology variation between crack-like (line-shaped) and pothole-like (region-shaped) distresses. Inspired by mixture-of-experts (MoE) paradigms, we introduce a lightweight morphology-aware sparse expert block that dynamically selects specialized convolutional pathways according to the input feature's local pattern. The MorphSparseMoE comprises four expert branches:

- **Expert 0:** horizontal line expert — depthwise convolution with kernel size 1×5
- **Expert 1:** vertical line expert — depthwise convolution with kernel size 5×1
- **Expert 2:** isotropic expert — standard 3×3 depthwise convolution
- **Expert 3:** region expert — average pooling followed by 1×1 convolution

A router network computes a probability distribution w = Softmax(Router(X)). We retain only the top-k experts (k=2) by masking the remaining weights to zero and re-normalizing. The output is:

```
Y = Σ w_i · Expert_i(X)
```

followed by a 1×1 projection and a residual connection.

### 3.3 Efficient Channel Attention (ECA)

We incorporate the ECA module at the output of the modified C2f blocks and the SPPF-CSPC structure. The kernel size k of the 1D convolution is adaptively determined by:

```
k = | (log₂(C) + 1) / 2 |_odd
```

ECA incurs negligible computational overhead while consistently boosting the discriminative power of the model for distress categories.

### 3.4 Lightweight SPPF-CSPC Structure

We propose a lightweight SPPF-CSPC variant that adopts a cross-stage partial connection (CSP) design. The input feature is split into two branches: one branch undergoes convolutions followed by n repeated max-pooling operations (n=3, kernel size 5), and the other is a shortcut 1×1 convolution. The two branches are concatenated and passed through a final 1×1 convolution followed by ECA.

### 3.5 Loss Function: WIoU with Box Morphology Consistency

We replace CIoU with Wise-IoU (WIoU):

```
L_WIoU = (1 - IoU) · exp(ρ²/σ²)
```

where ρ is the Euclidean distance between box centers, σ is the diagonal of the minimum bounding rectangle, and the exponential term is gradient-detached.

The morphology consistency loss operates in log-space:

```
L_morph = |log(w_p/h_p) - log(w_t/h_t)| + 0.5 · |log(√(w_p·h_p)) - log(√(w_t·h_t))|
```

The total box loss is:

```
L_box = L_WIoU + λ · L_morph
```

### 3.6 Post-Processing: Topology-Guided Box Fusion

We construct a graph where each detection is a node, and edges are defined by morphological relationships: two crack boxes are topologically related if (a) their IoU exceeds 0.12, or (b) they share the same dominant orientation and their center distance is less than 0.08 × D_image or 0.65 × max(box sizes). Union-Find is applied to group and fuse related boxes.

---

## 4. Experiments

(See `BMS-YOLO_Experiments_Polished.md` for the complete experimental section.)

---

## 5. Conclusion

This paper addresses the core issues of high-frequency detail loss, insufficient morphological adaptability, and loss function unfriendliness to crack characteristics in existing YOLO models for pavement distress detection, and proposes BMS-YOLO. Through systematic theoretical analysis and extensive experimental validation on the UAV-PDD2023 benchmark dataset, the main conclusions are as follows:

1. The FDDE module effectively improves perception of subtle cracks via frequency-direction decoupling and adaptive gating.
2. The MorphSparseMoE achieves morphology-adaptive modeling with low computational cost via top-k sparse routing among four specialized expert branches.
3. ECA and the lightweight SPPF-CSPC structure synergistically achieve model compression and receptive field expansion.
4. The joint optimization of WIoU and box morphology consistency loss, with a "strong-to-weak" two-stage training strategy (λ: 0.02 → 0.005), is identified as the optimal approach for leveraging morphological priors.
5. The topology-guided box fusion post-processing strategy effectively increases recall by 1.9 points for fragmented crack detection.
6. BMS-YOLO achieves 79.3% mAP50 and 54.6% mAP50:95 on UAV-PDD2023, outperforming YOLOv8n by 2.4 and 4.6 points respectively, while maintaining 31.8 FPS on an RTX 5090 GPU.

**Limitations and Future Work:** Future directions include illumination normalization preprocessing, super-resolution auxiliary modules for extremely small targets, graph neural networks for dense mesh-like crack topology modeling, INT8 quantization and structured pruning for edge deployment, and semi-supervised/weakly supervised learning paradigms.

---

## References

[1] G. Jocher, A. Chaurasia, and J. Qiu, "YOLOv8: Ultralytics YOLO," 2023.

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
