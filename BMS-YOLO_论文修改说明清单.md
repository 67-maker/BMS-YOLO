# BMS-YOLO 论文修改说明清单

**修改日期：** 2026-07-20
**修改依据：** 《BMS-YOLO IEEE Access 论文全维度修改意见》
**目标期刊：** IEEE Access

---

## 一、作者信息修改

| 修改项 | 修改前 | 修改后 |
|---|---|---|
| 作者姓名 | Qi Liu | Qi Liu |
| 作者单位 | College of Big Data and Intelligent Engineering, Changjiang Normal University | College of Big Data and Intelligent Engineering, **Yangtze Normal University** |
| 城市/邮编 | Chongqing 408000, China | Chongqing 408000, China |
| 作者邮箱 | liuqi@cjcnu.edu.cn | **liuqi@cynu.edu.cn** |
| 基金信息 | 占位符文字 | **已删除（无基金支持）** |

---

## 二、摘要（Abstract）重写

### 2.1 修改原因
- 原摘要为超长复合句堆砌，可读性差
- 缺少自定义模块缩写全称
- 未说明 UAV 边缘部署工程意义
- 词数超出 IEEE Access 标准

### 2.2 修改内容
- 拆分长难句，控制总词数约 220 词
- 所有自定义模块首次出现补全全称：
  - **frequency-direction detail enhancement (FDDE)**
  - **morphology-aware sparse mixture of experts (MorphSparseMoE)**
  - **efficient channel attention (ECA)**
  - **spatial pyramid pooling--cross-stage partial connection (SPPF-CSPC)**
  - **wise intersection-over-union (WIoU)**
- 增加结尾句说明 UAV 道路巡检边缘部署工程意义
- 逻辑结构调整为：痛点 → 方案 → 创新模块 → 实验指标 → 工程价值

---

## 三、关键词（Index Terms）精简

| 修改前 | 修改后 |
|---|---|
| Pavement distress detection, object detection, YOLOv8, morphology-aware sparse experts, frequency-direction detail enhancement, Wise-IoU, topology-guided fusion, UAV imagery（8个，冗余混乱） | **Pavement Distress Detection, YOLOv8, Sparse Mixture of Experts, Wise-IoU, UAV Remote Sensing**（5个，首字母大写） |

---

## 四、表格全部转换为 IEEE 三线表

### 4.1 转换说明
- 删除所有竖线 `|`
- 使用 `\toprule`、`\midrule`、`\bottomrule`
- 数值精度全局统一（mAP、FPS、参数量均保留 1 位小数）
- 近似值 `$\sim$` 在表格中保留

### 4.2 表格转换清单

| 表号 | 表名 | 修改内容 |
|---|---|---|
| Table 1 | Category Distribution | 竖线表 → 三线表 |
| Table 2 | Overall Performance Comparison | 竖线表 → 三线表，`table*` 跨栏 |
| Table 3 | Progressive Architecture and Loss Ablation | 竖线表 → 三线表，`table*` 跨栏 |
| Table 4 | Sensitivity Analysis of $\lambda$ | 竖线表 → 三线表 |
| Table 5 | Topology-guided Box Fusion | 竖线表 → 三线表，`table*` 跨栏 |
| Table 6 | Model Complexity and Efficiency | 竖线表 → 三线表 |
| Table 7 | Per-category mAP50 Comparison | 竖线表 → 三线表 |

---

## 五、章节结构重构

### 5.1 Related Work 子小节重组

| 修改前 | 修改后 |
|---|---|
| (A) Crack and Pavement Distress Detection Methods | (A) Pavement Distress Detection Methods |
| (B) YOLO-Series Object Detection Models | **(B) Lightweight YOLO Architectures and Vision Mixture-of-Experts** |
| (C) Convolutional Variants and Lightweight Architectural Designs | **(C) Feature Enhancement and Channel Attention Mechanisms** |
| (D) Object Detection Loss Functions | **(D) Bounding Box Regression Loss Functions** |

每小节末尾增加总结句，点出现有方法局限性，引出本文改进思路。

### 5.2 Methodology 子小节重组

| 修改前 | 修改后 |
|---|---|
| 无 3.1（直接跳到 3.2） | **3.1 Overall Architecture of BMS-YOLO**（新增网络总览段落 + Fig.1 占位） |
| 3.2 Frequency-Direction Detail Enhancement | 3.2 Frequency-Direction Detail Enhancement (FDDE) |
| 3.3 Morphology-Aware Sparse Experts | 3.3 Morphology-Aware Sparse MoE (MorphSparseMoE) & BMSC2f Block |
| 3.4 Efficient Channel Attention | **3.4 Lightweight Multi-scale Fusion: SPPF-CSPC and ECA Attention**（合并） |
| 3.5 Loss Function: WIoU with Box Morphology Consistency | **3.5 Joint Loss: WIoU and Box Morphology Consistency with Two-stage Training** |
| 3.6 Post-Processing: Topology-Guided Box Fusion | **3.6 Inference Post-processing: Topology-Guided Box Fusion** |

### 5.3 Introduction 六段重构

| 段落 | 内容 |
|---|---|
| 段落 1 | 道路病害运维行业背景，人工巡检缺陷，**无人机遥感检测优势** |
| 段落 2 | 传统图像处理方法的局限性 |
| 段落 3 | 深度学习检测方案对比（分类/分割/两阶段/YOLO 优缺点） |
| 段落 4 | **四大核心痛点（i-iv）**：高频细节丢失、形态建模单一、损失函数不匹配、裂纹碎片化 |
| 段落 5 | **五+项创新点**，区分核心算法创新与工程优化，MorphSparseMoE 增加差异化创新说明 |
| 段落 6 | 全文章节组织安排 |

### 5.4 Conclusion 重写

| 修改前 | 修改后 |
|---|---|
| 枚举式总结（First, Second, Third...） | **叙述式升华**"架构-损失协同设计"核心主线 |
| 局限性一段带过 | **分点客观阐述**四大模型短板 |
| 未来工作五项并列 | **分层规划**：短期部署优化、中期算法改进、长期弱监督学习研究 |

---

## 六、公式变量解释补全

| 公式 | 补充的变量解释 |
|---|---|
| FDDE 门控公式 $G = \sigma(\text{GAP}(X_{\text{high}}))$ | GAP 全局平均池化、$\sigma$ sigmoid 激活函数、$C$ 通道数 |
| FDDE 输出公式 $X_{\text{out}} = X + \text{Conv}_{1\times1}(\dots)$ | $\odot$ 逐元素乘法、$[\cdot;\cdot]$ 通道拼接、$X_{\text{high}}'$/$X_{\text{low}}'$ 投影特征 |
| MoE 路由公式 $\mathbf{w} = \text{Softmax}(\text{Router}(X))$ | Router 具体结构（GAP + 两层 MLP + SiLU + 线性层）、$\Delta^4$ 4-单纯形含义 |
| ECA 核大小公式 $k = |\log_2(C) + 1|/2|_{\text{odd}}$ | $C$ 通道数、$|\cdot|_{\text{odd}}$ 取最近奇数含义 |
| WIoU 公式 $\mathcal{L}_{\text{WIoU}} = (1-\text{IoU})\exp(\rho^2/\sigma^2)$ | IoU 交并比、$\rho$ 中心点欧氏距离、$\sigma$ 最小外接矩形对角线 |
| 形貌损失 $\mathcal{L}_{\text{morph}}$ | $w_p$/$h_p$/$w_t$/$h_t$ 预测框/真实框宽高、log 空间含义 |
| 总框损失 $\mathcal{L}_{\text{box}}$ | $\lambda$ 平衡超参数、两阶段策略说明 |
| 拓扑融合条件 $d < 0.08 \times D_{\text{image}}$ | $D_{\text{image}}$ 图像对角线长度、$s_i$/$s_j$ 最大边长 |

---

## 七、实验部分增强

| 修改项 | 说明 |
|---|---|
| 公平性声明 | 增加所有对比模型统一训练条件的详细说明（300 epoch、SGD、数据增强、输入分辨率） |
| 理论复杂度分析 | 定量分析 FDDE（约 +0.15M 参数、+0.3 GFLOPs）和 MorphSparseMoE（约 +0.3M 参数、+0.8 GFLOPs/块）的参数/FLOPs 增量 |
| 定性结果图片编号 | 从 fig:qual-a/b/c 改为 fig:qual1/2/3 |

---

## 八、图表占位注释（待插入）

| 图号 | 内容 | LaTeX 位置 |
|---|---|---|
| **Fig. 1** | BMS-YOLO 完整网络架构总图（标注 Backbone/Neck/Head、下采样倍数、通道维度） | Methodology 3.1 节 |
| **Fig. 2** | 三大模块子图：(a) FDDE (b) MorphSparseMoE (c) SPPF-CSPC | Methodology 3.3 节后 |
| **Fig. 3** | 消融实验 mAP50/mAP50:95 柱状对比图 | 实验消融实验段 |
| **Fig. 4** | $\lambda$ 超参灵敏度折线图（单阶段 vs 两阶段） | 超参分析段 |
| **Fig. 5** | 各类别 mAP50 对比柱状图（YOLOv8n vs BMS-YOLO-n） | 类别分析段 |
| **Fig. 6** | FPS-参数量权衡散点图 | 整体对比段 |
| **Fig. 7a/b/c** | 优化定性检测效果图（增加局部放大、差异化配色、标注置信度） | 定性结果段 |

---

## 九、英文学术表达润色

| 润色项 | 具体修改 |
|---|---|
| 拆分长难句 | 摘要、Introduction 多处拆分超过 3 行的复合句 |
| 主动语态 | 统一使用 "we propose/we design/we conduct" |
| 段落过渡词 | 增加 However、Furthermore、In contrast、Specifically 等连接词 |
| 术语统一 | bounding box 首次全称、UAV imagery 统一、mAP50:95 固定格式 |
| 时态统一 | 已有文献用过去时、本文模型用一般现在时、实验结果用过去时 |

---

## 十、未完成的修改项（需你配合）

| 未完成项 | 原因 | 后续处理 |
|---|---|---|
| 6 张新图绘制 | 无法自动生成 | 待你绘制后发给我插入 |
| 3 张定性效果图优化 | 需要图片处理 | 待你优化后替换 |
| 单一组件消融实验数据 | 暂无新数据 | 暂不补充 |
| top-k 路由超参对比 | 暂无新数据 | 暂不补充 |
| 边缘设备 FPS 测试 | 暂无新数据 | 暂不补充 |
| 参考文献格式标准化 | 时间/工作量较大 | 待后续处理 |

---

## 十一、文件清单

| 文件 | 路径 | 说明 |
|---|---|---|
| LaTeX 主文件（最终版） | `IEEE ACCESS_latex/access_final.tex` | 包含全部修改 |
| 实验部分 | `IEEE ACCESS_latex/experiments.tex` | 已内联到主文件，可保留备份 |
| PDF 输出 | `IEEE ACCESS_latex/access_final.pdf` | 编译成功，11 页 |
| 完整英文 Markdown | `BMS-YOLO_Full_Paper_Complete.md` | 所有部分整合 |
| 中文版 Markdown | `BMS-YOLO_Full_Paper_中文版.md` | 供阅读参考 |

---

## 十二、修改前后对比摘要

| 维度 | 修改前 | 修改后 |
|---|---|---|
| 摘要词数 | 约 280 词（超限） | 约 220 词（合规） |
| 关键词数量 | 8 个（冗余） | 5 个（精简） |
| 表格格式 | 竖线表格 | IEEE 三线表 |
| 宽表布局 | 单栏（溢出/重叠） | 跨栏 `table*` |
| 章节结构 | 原始 5 段 | 6 段逻辑递进 |
| 公式变量 | 未解释 | 全部补全 |
| 结论段落 | 枚举式 | 叙述式升华 + 分层未来工作 |
| 作者信息 | 占位符 | 真实姓名+单位+邮箱 |
| PDF 页数 | 10 页 | 11 页 |
