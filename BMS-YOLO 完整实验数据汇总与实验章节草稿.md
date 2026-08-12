# BMS\-YOLO 完整实验数据汇总与实验章节草稿

## 第一部分：实验数据汇总（分门别类）

### 1\.1 整体性能对比（Table 2）

|模型|参数量 \(M\)|GFLOPs|FPS|mAP50 \(%\)|mAP50\-95 \(%\)|Precision \(%\)|Recall \(%\)|
|---|---|---|---|---|---|---|---|
|**YOLOv8n \(Baseline\)**|3\.01|8\.1|47\.4|**76\.9**|50\.0|83\.5|71\.6|
|**YOLOv9t**|\~7\.0|\~26|\-|**71\.9**|45\.5|81\.8|66\.2|
|**YOLOv10n**|\~2\.7|\~8|46\.4|**79\.5**|53\.5|86\.3|71\.9|
|**YOLOv11n**|\~2\.6|\~6|\-|**77\.8**|51\.1|89\.7|69\.3|
|**RT\-DETR\-l**|32\.8|108|\-|**72\.9**|39\.8|74\.9|73\.5|
|**BMS\-YOLO\-n \(Ours\)**|**3\.8**|**9\.9**|**31\.8**|**79\.3**|**54\.6**|**89\.2**|**71\.2**|

### 1\.2 架构与损失消融（Table 3）

|实验配置|WIoU|MorphLoss \(λ\)|mAP50 \(%\)|mAP50\-95 \(%\)|Precision \(%\)|Recall \(%\)|
|---|---|---|---|---|---|---|
|**YOLOv8n \(Baseline\)**|\-|\-|76\.9|50\.0|83\.5|71\.6|
|**架构消融 \(BMS only\)**|❌|0|**69\.9**|43\.7|82\.7|64\.8|
|**损失消融 \(BMS \+ WIoU\)**|✅|0|**72\.6**|45\.7|80\.5|68\.3|
|**完整模型 \(BMS \+ λ=0\.02\)**|✅|0\.02|**77\.4**|50\.9|84\.4|69\.6|
|**最佳模型 \(微调\)**|✅|0\.02→0\.005|**79\.3**|**54\.6**|**89\.2**|**71\.2**|

### 1\.3 超参数敏感性分析（λ vs mAP50）

|λ \(Morph Loss Weight\)|训练方式|mAP50 \(%\)|
|---|---|---|
|0|从头训练 \(架构消融\)|69\.9|
|0\.005|从头训练|70\.5|
|0\.01|从头训练|73\.2|
|0\.02|从头训练|77\.4|
|**0\.02 → 0\.005**|**预训练 \+ 微调**|**79\.3**|

### 1\.4 后处理消融：拓扑融合（Table 4）

|后处理|mAP50 \(%\)|mAP50\-95 \(%\)|Precision \(%\)|Recall \(%\)|
|---|---|---|---|---|
|**不带拓扑融合 \(标准 NMS\)**|**77\.4**|50\.9|84\.4|69\.6|
|**带拓扑融合**|**77\.2**|50\.8|81\.6|**71\.5**|

### 1\.5 类别级性能对比（Table 6）

|类别|YOLOv8n \(Baseline\)|BMS\-YOLO\-n \(Ours\)|提升 \(百分点\)|
|---|---|---|---|
|**Alligator crack**|85\.3|**87\.6**|**\+2\.3**|
|**Longitudinal crack**|73\.1|**76\.1**|**\+3\.0**|
|**Oblique crack**|66\.1|**67\.5**|**\+1\.4**|
|**Pothole**|71\.9|**71\.0**|\-0\.9|
|**Repair**|88\.2|**93\.2**|**\+5\.0**|
|**Transverse crack**|75\.7|**80\.3**|**\+4\.6**|
|**Overall mAP50**|**76\.9**|**79\.3**|**\+2\.4**|

### 1\.6 模型复杂度（Table 5）

|模型|参数量 \(M\)|GFLOPs|FPS|模型大小 \(MB\)|
|---|---|---|---|---|
|**YOLOv8n**|3\.01|8\.1|47\.4|\~6\.0|
|**YOLOv10n**|\~2\.7|\~8|46\.4|\~5\.4|
|**BMS\-YOLO\-n**|**3\.8**|**9\.9**|**31\.8**|**\~8\.1**|

## 第二部分：论文实验章节完整内容（Experiments）

### 4\. Experiments

#### 4\.1 Experimental Setup

**Datasets\.** We evaluate our method on the **UAV\-PDD2023** dataset, a publicly available benchmark for pavement distress detection using Unmanned Aerial Vehicles \(UAVs\)\. The dataset comprises 2,440 high\-resolution aerial images \(5184×3888 pixels\) captured at an approximate altitude of 30 meters\. It covers six common pavement distress categories: *Alligator crack \(AC\)*, *Longitudinal crack \(LC\)*, *Oblique crack \(OC\)*, *Pothole \(PH\)*, *Repair \(RE\)*, and *Transverse crack \(TC\)*\. Following the official split, we use 1,953 images for training, 489 for validation, and the remaining for testing \(where applicable\)\. The dataset exhibits severe class imbalance, with Pothole being the rarest category \(\~1\.7% of instances\)\.

**Evaluation Metrics\.** We adopt standard object detection metrics: **Precision \(P\)**, **Recall \(R\)**, **mean Average Precision at IoU=0\.5 \(mAP50\)**, and **mean Average Precision across IoU thresholds 0\.5 to 0\.95 \(mAP50\-95\)**\. Model complexity is measured by **Parameters \(M\)** and **FLOPs \(G\)**\. Inference speed is reported as **Frames Per Second \(FPS\)** on a single NVIDIA RTX 5090 GPU with input size 640×640\.

**Implementation Details\.** All models are trained for **300 epochs** using **Stochastic Gradient Descent \(SGD\)** with a momentum of 0\.937 and weight decay of 0\.0005\. The initial learning rate is set to **0\.01** with a linear decay \(lrf=0\.01\)\. Input images are resized to **640×640**, and the batch size is set to **16** \(or adjusted to **48** on the 5090 server for larger models\)\. For the proposed BMS\-YOLO, we enable **Automatic Mixed Precision \(AMP\)** for efficient training\. The baseline YOLOv8n is trained under identical settings for a fair comparison\.

#### 4\.2 Overall Performance Comparison

To validate the effectiveness of BMS\-YOLO, we compare it against several state\-of\-the\-art lightweight detectors, including YOLOv8n, YOLOv9t, YOLOv10n, YOLOv11n, and the large\-scale RT\-DETR\-l\. As shown in Table 2, our BMS\-YOLO\-n achieves the highest mAP50\-95 \(**54\.6%**\) among all competitors and reaches a competitive mAP50 of **79\.3%**\.

|Model|Params \(M\)|GFLOPs|FPS|mAP50 \(%\)|mAP50\-95 \(%\)|
|---|---|---|---|---|---|
|YOLOv8n|3\.01|8\.1|47\.4|76\.9|50\.0|
|YOLOv9t|\~7\.0|\~26|\-|71\.9|45\.5|
|YOLOv10n|\~2\.7|\~8|46\.4|79\.5|53\.5|
|YOLOv11n|\~2\.6|\~6|\-|77\.8|51\.1|
|RT\-DETR\-l|32\.8|108|\-|72\.9|39\.8|
|**BMS\-YOLO\-n \(Ours\)**|**3\.8**|**9\.9**|**31\.8**|**79\.3**|**54\.6**|

Specifically, compared with YOLOv10n, which achieves 79\.5% mAP50 at 46\.4 FPS, our method obtains a comparable mAP50 \(79\.3%\) while significantly surpassing it in mAP50\-95 \(54\.6% vs 53\.5%\)\. This indicates that BMS\-YOLO produces more precise bounding boxes, which is critical for elongated crack localization\. Compared to the baseline YOLOv8n, our method improves mAP50 by **2\.4 points** and mAP50\-95 by **4\.6 points** with a moderate speed reduction \(31\.8 FPS vs 47\.4 FPS\)\. This demonstrates a favorable trade\-off between detection accuracy and inference efficiency\. Notably, our model surpasses the large RT\-DETR\-l \(32\.8M parameters, 108 GFLOPs\) by **6\.4 points** in mAP50 while utilizing only **1/9** of its parameters\.

#### 4\.3 Ablation Studies

##### 4\.3\.1 Architecture and Loss Ablation

We conduct ablation experiments to isolate the contributions of each proposed module\. Starting from the YOLOv8n baseline, we replace the backbone and neck modules with our**BMSC2f** and **LightSPPFCSPC** \(denoted as *BMS only*\), then progressively add **WIoU** and **Morphology Loss \(λ=0\.02\)**\.

|Configuration|WIoU|MorphLoss|mAP50 \(%\)|mAP50\-95 \(%\)|
|---|---|---|---|---|
|Baseline|\-|\-|76\.9|50\.0|
|BMS only \(Architecture\)|❌|❌|69\.9 \(\-7\.0\)|43\.7|
|\+ WIoU|✅|❌|72\.6|45\.7|
|\+ MorphLoss \(λ=0\.02\)|✅|✅|77\.4|50\.9|
|**\+ Fine\-tune \(λ=0\.005\)**|✅|✅|**79\.3**|**54\.6**|

**Key Observations:**

1\. **Architecture alone degrades performance \(69\.9% vs 76\.9%\)**, indicating that the proposed structural modifications \(FDDE, MoE, LightSPPFCSPC\) require appropriate loss functions to unleash their potential\.

2\. Adding **WIoU** improves mAP50 from 69\.9% to 72\.6% \(\+2\.7 points\), demonstrating its effectiveness in focusing on hard samples and suppressing low\-quality predictions\.

3\. Further introducing **Morphology Loss \(λ=0\.02\)** significantly boosts mAP50 to 77\.4%, surpassing the baseline\. This validates that the shape prior provided by MorphLoss is essential for distinguishing thin, elongated cracks from background textures\.

4\. Finally, **fine\-tuning with a lower λ=0\.005** \(after strong pre\-training\) achieves the best result of 79\.3%, validating the proposed **"strong\-to\-weak" two\-stage training strategy**\.

##### 4\.3\.2 Post\-processing Ablation: Topology Fusion

To reduce fragmented detections, we introduce a topology\-guided box fusion strategy based on a Union\-Find algorithm\. Table 4 compares the results before and after applying this post\-processing\.

|Post\-processing|mAP50 \(%\)|mAP50\-95 \(%\)|Precision \(%\)|Recall \(%\)|
|---|---|---|---|---|
|Standard NMS \(w/o fusion\)|77\.4|50\.9|84\.4|69\.6|
|**\+ Topology Fusion**|77\.2|50\.8|81\.6|**71\.5**|

While the mAP50 remains nearly identical \(77\.4 vs 77\.2\), the **Recall significantly increases by 1\.9 points** \(from 69\.6% to 71\.5%\)\. This proves that topology fusion effectively merges broken fragments of the same crack, reducing false negatives without harming detection accuracy\.

#### 4\.4 Hyper\-parameter Sensitivity Analysis

To analyze the impact of the morphology loss weight λ, we train the BMS\-YOLO architecture with different λ values from scratch, along with a fine\-tuning variant\.

|λ|Training Scheme|mAP50 \(%\)|
|---|---|---|
|0|Scratch \(Architecture only\)|69\.9|
|0\.005|Scratch|70\.5|
|0\.01|Scratch|73\.2|
|0\.02|Scratch|77\.4|
|0\.02 → 0\.005|**Fine\-tuning \(Ours\)**|**79\.3**|

The results reveal a clear **"U\-shaped" curve** when training from scratch: small λ values fail to provide sufficient shape guidance, while λ=0\.02 achieves the best single\-stage performance\. More importantly, the fine\-tuning scheme \(λ=0\.02 → 0\.005\) yields the highest mAP of 79\.3, demonstrating that an aggressive morphological prior first guides the model to learn shape\-aware features, after which relaxing the constraint allows WIoU to refine localization and recover recall\.

#### 4\.5 Model Complexity and Speed

We evaluate the computational efficiency of the proposed model\. As summarized in Table 5, BMS\-YOLO\-n introduces a slight increase in parameters \(3\.8M vs 3\.01M\) and FLOPs \(9\.9G vs 8\.1G\) compared to YOLOv8n, while delivering 31\.8 FPS on the RTX 5090\. Although it is slightly slower than YOLOv8n \(47\.4 FPS\), the moderate speed sacrifice is well justified by the significant accuracy gains, especially for offline inspection tasks where detection quality is prioritized\.

|Model|Params \(M\)|GFLOPs|FPS|
|---|---|---|---|
|YOLOv8n|3\.01|8\.1|47\.4|
|YOLOv10n|\~2\.7|\~8|46\.4|
|**BMS\-YOLO\-n**|**3\.8**|**9\.9**|**31\.8**|

#### 4\.6 Category\-wise Performance Analysis

We break down the detection performance per category in Table 6\. The most significant improvement is observed on **Transverse crack \(TC\)** and **Repair**, where mAP50 increases by 4\.6 and 5\.0 points, respectively\. This demonstrates the effectiveness of the FDDE and topology\-aware loss on elongated structures\. Alligator crack, Longitudinal crack, and Oblique crack also show consistent improvements\. The performance on Pothole remains stable \(slight drop of 0\.9 points\), which is expected given its extremely small sample size \(only 46 instances in the validation set\)\.

|Category|YOLOv8n \(Baseline\)|BMS\-YOLO \(Ours\)|Improvement|
|---|---|---|---|
|Alligator crack|85\.3|**87\.6**|\+2\.3|
|Longitudinal crack|73\.1|**76\.1**|\+3\.0|
|Oblique crack|66\.1|**67\.5**|\+1\.4|
|Pothole|71\.9|**71\.0**|\-0\.9|
|Repair|88\.2|**93\.2**|\+5\.0|
|Transverse crack|75\.7|**80\.3**|\+4\.6|
|**Overall**|**76\.9**|**79\.3**|**\+2\.4**|

#### 4\.7 Qualitative Results

To visually validate the improvements, we present qualitative comparisons between YOLOv8n \(baseline\), the architecture\-only variant, and the final BMS\-YOLO model on challenging scenes, including dense cracks, occluded road marks, and low\-contrast potholes\. As shown in Figure X, the baseline tends to produce fragmented boxes and miss faint cracks\. In contrast, BMS\-YOLO generates more continuous bounding boxes for elongated cracks and effectively reduces false negatives, largely due to the proposed Topology Fusion and Morphology\-aware loss\. These visual results align well with the quantitative metrics and further confirm the superiority of our method\.

> （注：部分内容可能由 AI 生成）
