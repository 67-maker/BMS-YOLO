# `access_final.pdf` 同行评审报告

- 评审日期：2026-08-04
- 评审模式：Academic Research Suite — `academic-paper-reviewer/full`
- 稿件：*BMS-YOLO: A Lightweight Box-Supervised Morphology-Aware Pavement Distress Detection Model*
- 拟投期刊：版式与页首页尾显示为 *IEEE Access*
- 评审范围：全文 13 页、约 8,096 个英文词、42 笔参考文献；核查正文、公式、表格、图件及部分引用的一手来源
- 限制：作者未提供代码、模型权重、数据切分清单或训练日志，因此本评审不能重跑实验；引用核查属高风险抽查，不等同 42 笔完整书目核验

## 一、编辑结论

**决定：Reject — Premature / Resubmit Encouraged（拒稿；完成数据与实验重建后可重投）**

稿件提出 FDDE、MorphSparseMoE、ECA/SPPF-CSPC、WIoU + morphology loss，以及 topology-guided box fusion 的组合框架。问题重要，稿件组织清楚，且尝试同时处理裂缝的频率、方向、形态与碎片化问题。但目前核心实证链条不能可靠支撑 79.3% mAP50、54.6% mAP50:95 及「可部署」结论：官方数据规模与稿件数据规模严重不符而未说明转换；最终模型比基线多 100 epochs 且 batch size 不同；部分消融并未在最终模型口径上完成；公式、实现叙述与归因互相矛盾；图表中存在直接相反的数值；引用抽查发现多笔作者、年份、卷期或原始来源错误。

这些不是文字润色即可修正。作者需要重建数据来源与切分、统一训练预算、重新执行关键实验、公开足够的可重现材料，并全面审核书目。若作者能完成上述工作，方法概念仍有形成可发表研究的潜力。

### 综合分数

| 维度 | 分数（0–100） | 判定 |
|---|---:|---|
| 原创性 | 60 | 概念组合有潜力，但「首创」未被可信文献定位支撑 |
| 方法严谨性 | 30 | 数据、比较公平性、公式与实现定义存在核心缺口 |
| 证据充分性 | 32 | 单次主结果、有限重复、无显着性/不确定性报告，且消融口径不一致 |
| 论证连贯性 | 47 | 结构清楚，但多处由相关结果直接推定模块机制 |
| 写作品质 | 70 | 英文整体可读、版式成熟，但数值与术语错误严重 |
| **加权平均** | **44.0** | **Reject** |

## 二、领域分析与评审配置

| 维度 | 判定 |
|---|---|
| 主要领域 | Computer Vision / Object Detection |
| 次要领域 | Civil Infrastructure Inspection、UAV Remote Sensing、Edge AI |
| 研究范式 | 定量实验研究 |
| 方法类型 | 深度学习模型设计、基准比较、消融研究 |
| 目标层级 | 稿件以 *IEEE Access* 为目标；现稿未达可送审的数据与可重现性门槛 |
| 稿件成熟度 | 版式接近投稿稿，但研究纪录与书目仍属未完成稿 |

评审角色如下，后续五份意见彼此独立形成，再由编辑综合：

1. **EIC**：*IEEE Access* 电脑视觉与智慧基础设施方向副编辑；关注期刊契合度、原创性、整体可信度与读者价值。
2. **Reviewer 1（方法）**：目标检测、benchmark protocol、ablation design 与可重现性专家；关注数据切分、比较公平性、统计不确定性、公式—实现一致性。
3. **Reviewer 2（领域）**：UAV pavement distress detection 与 civil infrastructure computer vision 研究者；关注文献来源、形态假设、数据集事实及增量贡献。
4. **Reviewer 3（实务/跨领域）**：UAV edge deployment 与道路资产管理工程师；关注整幅图像吞吐、端侧硬件、检出单位与运维价值。
5. **Devil’s Advocate**：专门压力测试「架构—损失共同设计」的核心因果叙事及最强替代解释。

## 三、EIC 评审

**建议：Reject；信心：4/5。**

### 优点

1. **问题重要且具应用价值。** 稿件针对 UAV 路面病害检测的形态异质性与裂缝碎片化，对智慧交通与基础设施巡检有明确意义。
2. **稿件结构完整。** Title—Abstract—Method—Experiments—Limitations 的主线清楚，图 1 能快速传达系统构成。
3. **作者承认若干限制。** 第 11–12 页主动讨论速度下降、低对比裂缝、topology fusion 过度合并与 pothole 下降，态度较平衡。

### 主要弱点

1. **核心结果缺乏可审核的数据血缘。** 第 7 页称使用 6,599/489 张 train/val 图像、39,198 个实例；官方论文与数据存储页面则报告约 2,440 张图像、11,158 个标注。若作者做了 tiling、镜像、重标注或版本整合，必须提供转换演算法、原图到 patch 的映射、版本 DOI、去重规则及 split manifest。否则结果无法与「UAV-PDD2023 benchmark」直接比较。官方来源：[Data in Brief 论文](https://www.sciencedirect.com/science/article/pii/S2352340923007710)、[Zenodo 数据页](https://zenodo.org/records/8429208)。
2. **「公平比较」声明不成立。** 第 7 页明确写 final BMS-YOLO 训练 400 epochs、baseline/其他模型 300 epochs，且 batch size 为 48 vs. 16。这两项都会改变优化动力与有效训练预算，故表 2 的 +2.4/+4.6 p.p. 不能完全归因于模型设计。
3. **稿件存在会误导读者的公开数值错误。** 图 5 图注声称 Alligator/Longitudinal/Oblique/Transverse 为 +13.0/+6.5/+5.9/+9.3，Repair 为 ?1.3；表 7 与图柱实际为 +2.3/+3.0/+1.4/+4.6，Repair +5.0。此错误直接影响结果解读。
4. **书目可靠性不足。** 抽查已发现 WIoU、ECA、Flexi-YOLO 等核心来源的作者、年份或出版资讯不符；在文献定位不可信时，首创性与差异化主张不能成立。

### 给作者的关键问题

1. 7,088 张图像与 39,198 个实例如何由官方 2,440 张/约 11,158 个标注产生？是否有原图跨 train/val 泄漏？
2. 表 2 的 BMS-YOLO 是否包含 topology fusion？若包含，为何表 5 仅在 77.4% 的 pre-fine-tune 模型上评估；若不包含，摘要的系统叙述应如何解读？
3. 作者是否能提供代码、配置文件、split manifest、每个 seed 的原始结果与模型权重？*IEEE Access* 的可重现性指引明确鼓励详细方法、数据与代码公开：[IEEE Access Reproducibility](https://ieeeaccess.ieee.org/authors/reproducibility/)。

## 四、Reviewer 1：方法与可重现性

**建议：Reject；信心：5/5。**

### 优点

1. 报告 P、R、mAP50、mAP50:95、Params、GFLOPs 与 FPS，至少涵盖精度与效率的基本面向。
2. 尝试进行 architecture/loss、lambda 与 post-processing 三类消融。
3. 有固定 seed，并宣称部分关键消融使用三个 seed 重复。

### 重大/关键问题

1. **[CRITICAL] 数据来源与切分不可重现。** 官方数据规模与表 1 完全不同，文中也未定义由 5,184×3,888 原图产生 6,599/489 张输入的步骤。必须排除同一原图的相邻 patches 同时出现在 train/val 的 group leakage；split 必须以原始飞行图像/路段为 group，而不是随机 patch。
2. **[CRITICAL] 训练预算混杂。** 最终模型的提升同时包含 architecture、loss schedule、额外 100 epochs、不同 learning-rate schedule 与不同 batch size。表 3 的「+ Fine-tune」不是纯 loss-weight 效应，因为它也增加训练时间。至少需要 2×2 控制：baseline 与 BMS 各自 300/400 epochs，且 batch、optimizer、LR schedule、AMP、augmentation 全部相同。
3. **[MAJOR] MoE 的数学叙述与计算主张不一致。** Router 使用 GAP 后输出每张图像的一组四维权重，因此不是「每个 spatial location」的 local morphology routing（第 5 页）。公式 (4) 又写出所有四个 Expert 的加权总和；若实现先计算全部 expert 再 mask，top-k 不会带来条件式 FLOPs 节省。作者须给出 tensor shape、routing granularity、dispatch/padding 实现、load balancing loss、expert utilization，以及实测 latency。
4. **[MAJOR] WIoU 定义混用了不同版本。** 公式 (6) 只呈现以中心距离作 detached reweighting 的形式，未呈现 WIoU v3 的 dynamic non-monotonic focusing/outlier-degree 部分；正文却反覆宣称 dynamic focusing。原始 WIoU 论文为 Tong et al. (2023)：[arXiv:2301.10051](https://arxiv.org/abs/2301.10051)。作者应明确标出使用版本、完整公式与代码来源，并避免把 detached 权重描述成对中心距离直接提供梯度。
5. **[MAJOR] Morphology loss 公式与文字不一致。** 公式 (7) 是 absolute error，但下一句称两项皆使用 smooth L1；二者梯度不同。需给出真正的 training expression、epsilon/clamping、宽高定义、适用类别 mask，以及是否只对裂缝类启用。若对 pothole/repair 同样启用，可能正是 compact class 下降的原因。
6. **[MAJOR] 消融不能识别各模块贡献。** 「BMS only」同时替换 FDDE、MorphSparseMoE、SPPF-CSPC、ECA，且性能下降 7.0 p.p.；后续只加入 WIoU/MorphLoss。没有 FDDE-only、MoE-only、ECA-only、SPPF-CSPC-only，也没有 architecture × loss 的 factorial ablation。现有结果只能证明整套 pipeline 在某一训练方案下较好，不能支持每个模块的机制性归因。
7. **[MAJOR] 不确定性与模型选择偏差未报告。** 稿件说「key ablations」跑三个 seed，但表 2–5 均无 mean±SD/CI，也未说哪些实验重复。lambda 及 two-stage schedule 在同一 validation set 上选优后又在同一 set 报最终结果，缺独立 test set，存在 validation overfitting。
8. **[MAJOR] Topology fusion 的评估口径含混。** 表 5 的基础值 77.4/50.9 对应 lambda=0.02 的 300-epoch 模型，而非表 2 的 79.3/54.6 final model；因此不能据此声称最终系统 recall +1.9 p.p.。且合并后 mAP 与 precision 均下降，应用价值需使用 crack-level connectivity/length coverage 或 maintenance-event recall 重新定义，而不能只用 COCO box metrics。

### 次要问题

- 第 7 页说 transverse crack 占 training instances 34.2%，实际 13,418/36,944 ≈ 36.3%。
- 同页把 validation 的 Repair=41、Pothole=46 写成 1.1%、1.0%；实际约为 1.8%、2.0%。
- 第 10 页说整幅 5,184×3,888 图像切成 640×640 patches 后约 100 ms。无重叠至少需 `ceil(5184/640) × ceil(3888/640) = 63` patches；以 32.3 FPS 计，纯模型推理约 1.95 s，尚未含 I/O、切片、NMS 与 fusion。
- batch-size-1 FPS 必须报 warm-up、迭代次数、AMP/FP16、同步方式、数据传输是否计入及方差。

## 五、Reviewer 2：领域、文献与贡献

**建议：Reject；信心：4/5。**

### 优点

1. 将线状裂缝与区域型病害的形态差异作为设计起点，方向合理。
2. 尝试把频率、方向卷积、attention、MoE、bounding-box loss 与 topology fusion 放在同一问题框架中。
3. 引入 UAV-PDD2023，题目与近年的道路病害检测研究相符。

### 主要问题

1. **[CRITICAL] 核心书目不能支撑技术谱系。** ECA 的原始来源是 Wang et al., CVPR 2020，而稿件 [27] 列成 2024 年的 pavement-specific Paper，并用同一文献同时支撑 SE 与 ECA。原始 ECA 论文：[CVPR Open Access](https://openaccess.thecvf.com/content_CVPR_2020/html/Wang_ECA-Net_Efficient_Channel_Attention_for_Deep_Convolutional_Neural_Networks_CVPR_2020_paper.html)。WIoU 原始作者亦非稿件 [30] 所列。这是来源归属错误，不只是格式问题。
2. **[MAJOR] 已抽查的近年文献多处 bibliographic mismatch。** 例如稿件 [17] 把 *Flexi-YOLO* 写成 Li & Chen、2026、PLOS ONE 21(4)，实际为 Yang, Tian, Zhou, Tan & He，2025，PLOS ONE 20(6)：[原文](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0325993)。稿件 [5] 只列 Yang & Song，原文有五位作者：[Sensors 原文](https://www.mdpi.com/1424-8220/26/2/609)。作者应逐笔以 DOI/Crossref/出版社页核对 42 笔参考文献，无法核实者删除。
3. **[MAJOR] 新颖性主张过度。** 「first morphology-specific expert branches for pavement distress detection」需要系统性的相近工作比较，而不是仅列举通用 MoE 与方向卷积。应建立 comparison table，比较 routing granularity、expert type、loss、data、params/FLOPs、是否提供代码。
4. **[MAJOR] 方向先验未处理 UAV 姿态与道路坐标系。** Horizontal/vertical expert 被分别对应 transverse/longitudinal crack，但 transverse/longitudinal 是相对道路轴线的语义，不等于图像全域 x/y 轴。若相机航向或 road orientation 改变，这一先验不具旋转等变性。需说明图像是否方向正规化，并加入旋转/跨航向测试或改用 steerable/orientation-equivariant filters。
5. **[MAJOR] 机制归因超出证据。** Repair +5.0 被归因于 FDDE 的「enhanced receptive field」，但 FDDE 主要是高/低频分支，且没有 category × component ablation；pothole ?0.9 又被归因于 class imbalance，却未提供多 seed 方差。这些应改写为假设，而非已证实因果。
6. **[MINOR] YOLOv8 术语自相矛盾。** 第 10 页称 MorphLoss 解决「default square anchors」与裂缝的 mismatch，但稿件第 2 页已正确说 YOLOv8 是 anchor-free；官方文件也确认 YOLOv8 使用 anchor-free split head：[Ultralytics YOLOv8](https://docs.ultralytics.com/models/yolov8)。

## 六、Reviewer 3：部署与跨领域实务

**建议：Major Revision；信心：4/5。**

### 优点

1. 同时报告参数、FLOPs 与 FPS，并讨论 offline UAV inspection，而不是只谈 mAP。
2. 承认 topology fusion 的 recall—precision trade-off，符合道路养护中漏检成本较高的情境。
3. 定性图尝试展示 lane marking、复合病害及稀有类别场景。

### 主要问题

1. **整幅图像吞吐被低估约一个数量级以上。** 32.3 FPS 是单个 640×640 tensor 的吞吐，不是 5,184×3,888 原图的任务吞吐；需报 end-to-end latency、patch overlap、边界去重、显存峰值及每公里道路处理速度。
2. **「UAV deployable」证据不足。** 实验硬件为桌面 RTX 5090，没有 Jetson/嵌入式 GPU、能耗、TensorRT engine、INT8 精度下降或实际飞行数据流。可改称「desktop post-mission processing prototype」，除非补做端侧测试。
3. **Box-level topology 不等于物理裂缝拓扑。** 把多个框合并可能提高 event recall，却也可能把交叉裂缝或相邻不同病害合成一个大框。道路养护更关心 distress event、长度、面积、严重度和地理位置；应增加 crack connectivity、length/area error、over-merge rate 与路段级 maintenance decision 指标。
4. **数据外部效度不足。** 仅在一个中国 UAV 数据集与单一高度附近验证，无跨道路材质、飞行高度、相机、天候、地区或数据集测试。部署声明应降级，或增加 cross-dataset/domain-shift evaluation。
5. **操作风险未量化。** precision 下降 2.8 p.p. 被描述为可接受，但实际养护成本取决于 false alarm 的派工成本与 missed distress 的安全成本。可提供可调 threshold 的 precision–recall/utility curve，而不是替所有场景预设 recall 更重要。

## 七、Devil’s Advocate 压力测试

### 最强反论

稿件目前最简单、也最能解释结果的替代叙事不是「morphology-aware architecture 与 morphology-sensitive loss 互相激活」，而是：作者在一个未被清楚说明、可能经切片或增广而扩大的数据版本上，用不同 batch size 和额外 100 epochs 对提出模型进行更充分的优化，再从同一 validation set 中选出最佳 lambda/schedule。Architecture-only 其实比 baseline 低 7.0 mAP50，加入 WIoU 后仍低 4.3；只有加入 morphology loss 及额外 fine-tuning 才超越 baseline。这同样可以由训练预算、正则化、超参数搜寻或数据泄漏解释，而不需要接受「co-design」机制。由于没有同预算 factorial ablation、独立 test set、router utilization、per-seed uncertainty 或可重跑代码，稿件尚未排除这个更节约的解释。

### CRITICAL

| # | 维度 | 问题 | 位置 |
|---|---|---|---|
| DA-C1 | Foundation collapse | 数据规模与官方版本不符，且缺少转换/切分血缘；若存在原图级泄漏，全部指标失效 | p.7, Table 1 |
| DA-C2 | Logic-chain break | 由不同训练预算下的结果推断 architecture–loss 因果协同；现有设计无法识别该因果 | pp.7–9, Tables 2–4 |
| DA-C3 | Evidence integrity | 核心引用来源错配，使「首次」「来源于」「相较既有方法」等定位无法被信任 | pp.3–4, 12–13 |

### MAJOR

| # | 维度 | 问题 | 位置 |
|---|---|---|---|
| DA-M1 | Internal contradiction | global GAP router 被描述成 local/spatial routing | pp.4–5, Eq. (3) |
| DA-M2 | Definition mismatch | WIoU 版本与公式不符；MorphLoss 的 absolute vs. smooth-L1 不符 | p.6, Eqs. (6)–(8) |
| DA-M3 | Result contradiction | Figure 5 caption 与 Table 7/柱图相反 | pp.10–11 |
| DA-M4 | System boundary | topology fusion 的 77.2/77.4 口径未与 final 79.3 模型接轨 | pp.9–10, Table 5 |
| DA-M5 | Deployment overclaim | tile-level FPS 被当成 full-image latency，且桌面 GPU 被泛化为 UAV deployability | p.10 |

## 八、编辑综合与共识

### 评审摘要

| 评审 | 建议 | 信心 | 核心意见 |
|---|---|---:|---|
| EIC | Reject | 4 | 结果与书目完整性不足，现稿不适合进入正式出版流程 |
| R1 方法 | Reject | 5 | 数据血缘、比较公平性与公式—实现一致性破坏内部效度 |
| R2 领域 | Reject | 4 | 核心引用错配，新颖性与形态先验未被可信定位 |
| R3 实务 | Major Revision | 4 | 概念具实务潜力，但部署与端到端评估明显过度主张 |
| Devil’s Advocate | — | — | 三项 CRITICAL 均直接攻击核心证据链 |

### 原子化子主张与共识

| ID | 子主张 | 同意者 | 处置 |
|---|---|---|---|
| SC-1 | 数据集规模/切分与官方来源不符且缺少血缘 | EIC, R1, R2, R3 | **[CONSENSUS-4] 必须重建** |
| SC-2 | final model 与 baselines 的 epochs/batch 不匹配 | EIC, R1, R2 | **[CONSENSUS-3] 必须重跑**；R3 未提及 |
| SC-3 | 现有消融不能证明 architecture–loss co-design | EIC, R1, R2 | **[CONSENSUS-3] 必须重设**；R3 未提及 |
| SC-4 | 书目存在来源与出版资讯错配 | EIC, R2 | 两位高信心评审相互佐证，列为 P1 |
| SC-5 | 部署/吞吐主张超出证据 | EIC, R1, R3 | **[CONSENSUS-3] 必须降级或补实验**；R2 未提及 |
| SC-6 | 图 5 图注与表 7 数值矛盾 | EIC, R1, R2 | **[CONSENSUS-3] 必须修正**；R3 未提及 |
| SC-7 | Router、WIoU、MorphLoss 的定义与叙述不一致 | R1, R2 | 两位专家相互佐证，列为 P1 |
| SC-8 | topology fusion 与 final model 指标口径不清 | EIC, R1, R3 | **[CONSENSUS-3] 必须重评估**；R2 未提及 |

唯一实质分歧是决定严格度：R3 认为 deployment evidence 可通过大修补强；EIC/R1/R2 认为数据血缘与引用完整性已使现有结果不可审核。编辑裁决采后者，因为这些问题要求重建数据与重跑主要实验，超出一般一次 Major Revision 的范围；但方法概念仍值得作者完成重建后另稿重投。

## 九、重投前修订路线图

### P1：必须完成

| # | 对应 | 任务 | 验收标准 |
|---|---|---|---|
| R1 | SC-1 | 重建数据血缘与 split | 列出官方版本 DOI、原始图像数/标注数、每一步 tiling/augmentation/relabel 规则、原图→patch 映射；发布 train/val/test manifest；证明原图/路段 group 无交叉 |
| R2 | SC-2 | 统一比较预算并重跑 | 所有模型相同 epochs、batch、optimizer、LR schedule、augmentation、seed；另做等 wall-clock/等 FLOPs 训练比较；至少 3–5 seeds，报 mean±SD/95% CI |
| R3 | SC-3, SC-7 | 重做 factorial ablation | FDDE、MoE、ECA、SPPF-CSPC、WIoU、MorphLoss、fine-tune、fusion 分别开关；包含 architecture × loss interaction；报每项 Params/FLOPs/latency |
| R4 | SC-7 | 修正并公开数学/实现定义 | 明确 WIoU 版本及完整公式；MorphLoss 使用 abs 或 smooth-L1 择一；说明 class mask、epsilon；提供 router tensor shape、expert dispatch、utilization 与 load balancing |
| R5 | SC-4 | 全面核对 42 笔书目 | 每笔以 DOI/出版社/会议官方页核对作者、题名、年份、卷期、页码；补 ECA、WIoU、CIoU 等原始来源；删除无法核实文献；重新评估所有「first/novel」主张 |
| R6 | SC-8 | 在 final checkpoint 上重评 topology fusion | 同一 final model、同一 split 比较 NMS vs fusion；除 COCO metrics 外，报 over-merge rate、event recall、connectivity/length metric；公开所有 threshold 选择规则 |
| R7 | SC-5 | 重做端到端部署评估 | 报每张完整原图的切片数、overlap、I/O、pre/post-processing、总 latency、显存与能耗；若仍称 UAV deployable，至少在一种 edge GPU/Jetson 上测试 |

### P2：强烈建议

1. 新增独立 test set 或跨数据集测试，避免在 validation set 同时调 lambda、选 schedule 与报最终结果。
2. 使用 road-axis normalization、rotation augmentation 或 rotation-equivariant/steerable filters，验证 horizontal/vertical expert 对航向变化的稳健性。
3. 报 per-class AP 的多 seed 不确定性；不要用 46/41 个 validation 实例的单次变化直接下机制结论。
4. 增加 calibration、PR curves、confusion matrix、不同 IoU threshold 与不同融合 threshold 的敏感性。
5. 将所有机制性归因改成「由专门消融支持」或「尚待验证的解释」，避免从一组结果直接推导因果。

### P3：文字与版式

1. 修正 Figure 5 caption、Table 1 百分比与 100 ms 叙述。
2. 删除「default square anchors」；YOLOv8 是 anchor-free。
3. 更新首页 publication date、DOI placeholder 与页尾 `VOLUME 11, 2023`，避免把投稿模板当成已出版资讯。
4. 统一 `UAV`、`WIoU`、`MorphLoss`、`SPPF-CSPC`、`top-k` 的拼写与版本标示。
5. Figure 2 应说明点大小如何映射 mAP，并避免用同一 GPU 的 raw FPS 泛化到不同部署平台。

## 十、给作者的最短行动顺序

1. 暂停文字润色，先锁定数据版本与 split。
2. 修正公式与代码，使 paper、config、code 三者一致。
3. 以公平预算重跑 baseline、final 与完整消融。
4. 做 final-model topology/deployment 评估。
5. 全面核对引用，最后再重写 Abstract、Discussion、Conclusion。

完成 P1 后，这项工作才适合重新进入正式同行评审。
