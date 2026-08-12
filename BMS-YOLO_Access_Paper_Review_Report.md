# BMS-YOLO IEEE Access 投稿稿 —— 多视角审阅报告

> **审阅框架**：`academic-research-skills/academic-paper-reviewer` v1.10.0（EIC + 3 位同行审稿人 + Devil's Advocate）。  
> **审阅对象**：`IEEE ACCESS_latex/access_final.pdf`（13 页，约 85 MB）。  
> **审阅日期**：2026-08-01。  
> **说明**：本报告为只读审阅产出，未修改原稿。

---

## 一、执行摘要（Executive Summary）

- **图状态**：Fig 1–8 全部正常嵌入 PDF，清晰度可接受；Fig 1 架构图布局合理。
- **最严重问题**：Fig 2 的 caption 写 “only **2.3M** parameters”，与全文其它所有地方（Abstract、Table 2、Table 6）的 **3.8M parameters** 严重矛盾。**必须在投稿前修正**。
- **建议编辑决定**：Major Revision（修正关键数据矛盾后可达 Minor Revision / Accept）。

---

## 二、图审阅（Figure Quality Review）

| 图 | 状态 | 备注 |
|---|---|---|
| **Fig 1** | ✅ OK | 架构图完整、模块清晰、无文字重叠；caption 与正文一致。 |
| **Fig 2** | ⚠️ **有问题** | 散点图本身清晰，但 **caption 参数量错误**（2.3M vs 3.8M）；RT-DETR-l 标 “FPS N/A” 略显冗余。 |
| **Fig 3** | ✅ OK | 消融柱状图，数据与 Table 3 一致。 |
| **Fig 4** | ✅ OK | λ 敏感性折线图，趋势与 Table 4 一致。 |
| **Fig 5** | ✅ OK | 每类 mAP50 柱状图，数据与 Table 7 一致。 |
| **Fig 6–8** | ✅ OK | 定性可视化正常嵌入，YOLOv8n vs BMS-YOLO 对比清晰。 |

**结论**：论文所有图片均已正确嵌入，无图缺失或严重分辨率问题；唯一必须处理的是 Fig 2 caption 的数值错误。

---

## 三、内容问题清单（按严重度）

### 🔴 Critical（必须修正）

**1. Fig 2 caption 参数量与全文严重矛盾**
- **位置**：PDF 第 8 页，Fig 2 caption；LaTeX 源文件 `access_final.tex` 第 292 行。
- **错误原文**：`BMS-YOLO-n achieves the best balance, delivering 79.3% mAP50 with only 2.3M parameters.`
- **正确表述**：`...delivering 79.3% mAP50 with only 3.8M parameters.`
- **依据**：
  - Abstract："with only 3.8M parameters"
  - Table 2：BMS-YOLO-n Params = 3.8 M
  - Table 6：BMS-YOLO-n Params = 3.8 M
  - Introduction 第 116 行同样使用 3.8M / 31.8 FPS
- **影响**：核心主张（轻量化）出现内部数据矛盾，审稿人会质疑论文数据可信度。

---

### 🟠 Major（强烈建议修正）

**2. Fig 2 中 RT-DETR-l 的 “FPS N/A” 标签冗余**
- **位置**：PDF 第 8 页，Fig 2 散点图右侧。
- **问题**：Table 2 中 RT-DETR-l 的 FPS 列为 “–”，图里却以独立标签 “FPS N/A” 呈现，使散点图右侧显得拥挤且缺乏坐标意义（y 轴为 FPS，该模型无 FPS 数据）。
- **建议**：
  - 方案 A：将 RT-DETR-l 从该 FPS-Params 散点图中移除，改为在 caption 中用文字说明对比；
  - 方案 B：保留该点但仅用小注释，避免 “Lower Params → Lighter RT-DETR-l FPS N/A” 这种长标签。

**3. Batch size 不一致削弱 “identical conditions” 声明**
- **位置**：PDF 第 7 页，Implementation Details。
- **问题**：
  - 原文："The batch size is set to 16 for the baseline and 48 for the proposed model on the 5090 server."
  - 后文："All comparison models are trained under identical conditions: the same 300 epochs, SGD optimizer, data augmentation strategy, and input resolution of 640×640."
- **影响**：batch size 会显著影响 batch normalization 统计和训练动态，称其 “identical” 不够严谨。
- **建议**：说明 batch size 差异（如显存限制），或改用 “comparable/controlled conditions”。

**4. 部分超参数/阈值缺少敏感性分析或说明**
- **MorphSparseMoE top-k = 2**：未解释选择 k=2 的原因，也未做 k 值 ablation。
- **Topology Fusion 阈值**：IoU 0.12、中心距离 0.08×D_image、0.65×max(s_i,s_j) 的物理意义与选择依据未说明；Table 5 仅展示有无 fusion，未做阈值 ablation。
- **两阶段训练 epoch 划分**：Table 3 提到 “Fine-tune”，但未说明 pre-train 和 fine-tune 各多少 epochs。
- **建议**：至少补充选择依据；如空间允许，增加敏感性分析。

---

### 🟡 Minor（可选优化）

**5. 模板占位符保留**
- PDF 首页 “Date of publication xxxx 00, 0000” 和每页底部 “VOLUME 11, 2023” 是 IEEE Access 模板默认占位，编辑部会替换；投稿前可接受。

**6. Fig 1 箭头视觉拥挤**
- Neck 到 Detection Head 的箭头以及 Head 到 Post-processing 的箭头穿越 Backbone/Neck 区域，略显拥挤但不影响理解。

**7. Fig 3 数据标签对齐可优化**
- 柱状图顶部数值标签位置与柱子的对应关系可以更紧凑，避免读者误读。

---

## 四、五位审稿人视角总结

### 1. EIC（主编）
- **期刊匹配度**：IEEE Access 接收工程与计算机科学应用类论文，路面病害检测 + UAV + 轻量 YOLO 属于合适范围。
- **创新性**：FDDE、MorphSparseMoE、SPPF-CSPC+ECA、WIoU+MorphLoss、Topology Fusion 的组合具有一定新意。
- **主要扣分点**：Fig 2 caption 的 2.3M/3.8M 矛盾是低级错误，会直接影响编辑对稿件严谨性的判断。
- **初步决定**：Major Revision。

### 2. Methodology Reviewer（方法审稿人）
- **优点**：方法栈完整，loss 设计（WIoU + log-space morphology loss）有理论动机；随机种子固定（seed=42）提升可复现性。
- **不足**：
  - top-k、topology fusion 阈值、两阶段 epoch 划分等关键实现细节缺少 ablation。
  - batch size 不同可能影响 baseline 与 proposed 的公平比较。
  - 未提供标准差（Table 2 未报告多次运行的方差），仅 ablation 实验提到 3 次运行。

### 3. Domain Reviewer（领域审稿人）
- **优点**：文献较新，覆盖 YOLOv8–11、RT-DETR、MoE、注意力机制等前沿方向。
- **不足**：
  - Table 2 的比较对象是通用检测器，缺少在 UAV-PDD2023 数据集上专门发表的最新 SOTA 方法对比。
  - 对 Pothole 类别 mAP50 下降 0.9 的解释（仅归因于类别不平衡）可能不足；需讨论形态感知设计对区域型/圆形目标的潜在偏见。

### 4. Perspective Reviewer（跨学科审稿人）
- **优点**：讨论了实时性（31.8 FPS）、桌面 GPU 部署、 offline UAV inspection 等实际应用场景。
- **可加强**：
  - 边缘设备（如 NVIDIA Jetson）部署潜力。
  - 模型量化/INT8 压缩对 FDDE/MoE 路径的影响。
  - 高分辨率图像 tiling 策略与推理延时的权衡。

### 5. Devil's Advocate（魔鬼代言人）
- **核心论点挑战**：
  - 论文主张 “architecture–loss co-design”，但 Table 3 显示单独替换为 BMS 架构使 mAP50 从 76.9 降至 69.9。这说明 **architecture 单独并不带来提升**，必须与 WIoU/MorphLoss 配合才能超过 baseline。论文应更谨慎表述二者的贡献权重，避免过度声称 architecture 本身的优越性。
- **其它质疑**：
  - **33% FPS 下降**（47.4 → 31.8）与 “lightweight” 定位存在张力，需更明确说明部署场景为何仍接受该速度。
  - **Pothole 性能下降** 可能不仅是类别不平衡，而是形态感知设计对短/圆目标有系统偏见。
  - **2.3M vs 3.8M** 的矛盾若被审稿人发现，会严重削弱核心主张的可信度。

---

## 五、编辑决定与修改路线图

### 推荐决定：Major Revision

> 理由：存在一处明确的 CRITICAL 数据矛盾（Fig 2 caption 参数量错误），以及若干影响方法严谨性的 Major 问题。修正后可达 Minor Revision 或 Accept。

### 必须修改（Revision Required）
1. **修正 Fig 2 caption**：`2.3M parameters` → `3.8M parameters`（`access_final.tex` 第 292 行）。
2. **复核 Fig 2 源图**：确认散点图上的 BMS-YOLO-n 点或标签没有同样的 2.3M 错误。
3. **统一比较条件描述**：明确 batch size 差异，或调整 “identical conditions” 措辞。

### 强烈建议修改（Strongly Recommended）
4. 移除/重述 Fig 2 中 RT-DETR-l 的 “FPS N/A” 标签。
5. 补充 MorphSparseMoE top-k、Topology Fusion 阈值、两阶段 epoch 划分的说明或 ablation。
6. 更谨慎地表述 architecture-loss co-design 的贡献比例，承认单独 architecture 替换会暂时降低性能。
7. 深入讨论 Pothole 类别性能下降的原因（不仅是类别不平衡）。

### 可选优化（Optional Polish）
8. 调整 Fig 1 箭头布局，减少模块间穿越。
9. 对齐 Fig 3 柱状图数据标签。
10. 补充 UAV-PDD2023 数据集专门 SOTA 方法的比较。

---

## 六、附录：PDF 技术核查结果

| 项目 | 结果 |
|---|---|
| 文件 | `IEEE ACCESS_latex/access_final.pdf` |
| 页数 | 13 |
| 文件大小 | 约 85 MB |
| 编译状态 | 成功（TeX Live 2026） |
| 图片嵌入 | Fig 1–8 全部正常嵌入，无图片缺失/未找到错误 |
| 参考文献 | BibTeX 处理成功 |
| 编译警告 | 仅有非致命字体/书签警告，不影响内容 |
