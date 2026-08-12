# BMS\-YOLO IEEE Access 论文全维度修改意见（Markdown 文档）

# BMS\-YOLO IEEE Access 论文全维度修改意见（Markdown 文档）

> 适用工具：Claude Code 全文润色、结构重排、图表补充、语法修正、格式标准化
> 
> 

## 文档基础信息

- 论文标题：BMS\-YOLO: A Lightweight Box\-Supervised Morphology\-Aware Pavement Distress Detection Model

- 期刊要求：IEEE Access 标准格式、学术表达、图表规范、实验论证完整性

- 文档用途：提交给 Claude Code 自动化改写、分段优化、生成图表描述、修正英文语法、重构章节逻辑

---

# 1 IEEE Access 硬性格式合规整改（最高优先级，必须先处理）

## 1\.1 标题、作者、摘要、索引词规范

### 1\.1\.1 标题规范

现有标题：`BMS-YOLO: A Lightweight Box-Supervised Morphology-Aware Pavement Distress Detection Model`

1. 缺陷：缩写 BMS 仅标题出现，摘要首次出现未补全全称，违反 IEEE 缩写规则

2. 修改要求：

    - 标题保留不变；

    - 摘要第一句完整书写全称 `Box-supervised Morphology-aware Sparse YOLO (BMS-YOLO)`；

    - 全文所有自定义模块缩写（FDDE / MorphSparseMoE / SPPF\-CSPC / WIoU）**首次出现必须附带完整英文全称**。

### 1\.1\.2 作者、通讯作者、基金、个人简介规范

原文缺失 IEEE 强制内容，要求补充：

1. 全部作者完整英文单位（学院、学校、城市、邮编、国家）；

2. 项目资助、基金编号、资助机构声明；

3. 文末 Biography 板块：所有作者学历、研究方向、代表性成果，期刊出版需配套证件照说明；

4. 通讯作者邮箱保留，补充完整作者排序说明。

### 1\.1\.3 ABSTRACT 摘要规范

IEEE Access 硬性标准：词数 150–250，无引用、无未定义缩写、逻辑闭环（痛点→方案→创新模块→实验指标→工程价值）
现有缺陷：

1. 超长复合句堆砌，工程论文可读性差；

2. 仅罗列指标，缺少无人机机载轻量化落地应用价值；

3. FDDE、MorphSparseMoE 首次出现无全称；
修改指令（发给 Claude Code）：

> 拆分长难句，控制总词数 220 左右；所有自定义模块首次出现补全全称；结尾增加 1 句说明 UAV 道路巡检边缘部署工程意义；删除冗余指标描述，强化对比增益。
> 
> 

### 1\.1\.4 INDEX TERMS 索引关键词

现有关键词数量过多、层级混乱、术语冗余：
`Pavement distress detection, object detection, YOLOv8, morphology-aware sparse experts, frequency-direction detail enhancement, Wise-IoU, topology-guided fusion, UAV imagery`
IEEE 规范：3–5 个名词短语，首字母大写，精简去重
标准优化版本（直接替换）：
`Pavement Distress Detection, YOLOv8, Sparse Mixture of Experts, Wise-IoU, UAV Remote Sensing`

## 1\.2 章节、公式、图表、表格 IEEE 排版规范

### 1\.2\.1 章节标题大小写规范

- 一级章节（I\. INTRODUCTION）：全大写，保留；

- 二级子小节（A\. FREQUENCY\-DIRECTION DETAIL ENHANCEMENT）：**改为仅首字母大写**
示例：`A. Frequency-Direction Detail Enhancement (FDDE)`

### 1\.2\.2 公式规范

1. 所有公式居中、编号右对齐，正文引用统一写 `Equation (X)`，禁止简写 Eq\.\(X\)；

2. 公式内全部变量必须在上下文文字完整解释：$\sigma$, GAP, $\lambda$, $D_{image}$, $s_i$, $s_j$ 等；

3. 张量 / 矩阵符号统一：特征图 $X \in \mathbb{R}^{C×H×W}$ 格式保持统一；损失函数花体 $\mathcal{L}$ 全文格式统一；

4. 补充公式变量符号说明段落，Claude Code 自动补全变量释义。

### 1\.2\.3 表格规范（核心整改项）

IEEE Access 表格强制规则：

1. 表标题置于表格上方：`TABLE X. XXXXX`；

2. 统一三线表，仅保留顶线、表头线、底线，删除所有竖线、多余横线；

3. 数值精度全局统一，mAP、FPS、参数量统一保留 1 位小数；

4. 近似值 `∼` 增加表格注释：`∼ denotes approximate statistical results`；

5. 注释统一放在表格底部，使用 `*` 标记；
现有表格问题：Markdown 竖线表格杂乱、表头拥挤、缺少注释、精度不统一。
Claude Code 指令：

> 将全文所有表格转换为 IEEE 标准三线表，统一数值精度，补充表格注释，优化表头文字可读性。
> 
> 

### 1\.2\.4 图片规范（论文严重缺失核心图表）

IEEE 图片硬性要求：

1. 图标题置于图片下方：`FIGURE X. XXXXX`；

2. 多子图标注 \(a\)\(b\)\(c\)，图内文字字号统一、清晰；

3. 对比图统一置信阈值、统一图像标尺；

4. 必须补充架构总图、模块结构图、定量可视化图表；
现有缺陷：仅文字描述效果图，无网络总图、无模块拆解图、无消融柱状图、无超参折线图。
需新增图表清单（交给 Claude Code 生成绘图描述文字）：

5. Fig\.1 BMS\-YOLO 完整网络架构总图（标注 Backbone/Neck/Head/FDDE/MorphSparseMoE 位置）

6. Fig\.2 三大核心模块子图：\(a\) FDDE \(b\) MorphSparseMoE 专家路由 \(c\) SPPF\-CSPC

7. Fig\.3 消融实验 mAP50/mAP50:95 柱状对比图

8. Fig\.4 λ 超参灵敏度折线图（单阶段 vs 两阶段训练）

9. Fig\.5 各类别 mAP50 对比柱状图（YOLOv8n vs BMS\-YOLO）

10. Fig\.6 FPS \- 参数量权衡散点图（轻量化模型横向对比）

11. 原有定性对比图 Fig1/2/3 优化：增加局部放大框、差异化类别检测框颜色、标注单图碎片框数量。

### 1\.2\.5 参考文献 References

1. 格式：数字顺序编码，IEEE 标准引用格式；

2. 缺陷：arXiv 预印本文献过多，期刊偏好正式会议 / 期刊文章；

3. 优化要求：替换部分 arXiv 文献为正式出版版本；补充 2024–2025 路面病害轻量化 YOLO 最新文献；统一作者排序、卷期页码完整信息；
Claude Code 指令：

> 标准化全部参考文献为 IEEE 数字引用格式，补充缺失卷期、DOI，替换冗余预印本文献，补充近 2 年相关前沿论文。
> 
> 

### 1\.2\.6 作者简介 Biography

原文仅第一作者简介，要求补充全部作者完整简介，包含研究方向、学历、成果，增加配图说明文字。

---

# 2 论文章节结构逻辑重构（Claude Code 分段重排优化）

原始章节顺序：
I\. INTRODUCTION → II\. RELATED WORK → III\. METHODOLOGY → IV\. EXPERIMENTS → V\. CONCLUSION

## 2\.1 Section I INTRODUCTION 引言重构

现有缺陷：背景冗长、痛点分散、创新点平铺直叙、缺少行业落地刚需描述
重构分段逻辑（指令给 Claude）：

1. 段落 1：道路病害运维行业背景，人工巡检缺陷，无人机遥感检测优势；

2. 段落 2：深度学习检测方案对比（分割 / 两阶段检测器 / YOLO 单阶段优缺点）；

3. 段落 3：标准 YOLOv8 用于路面病害三大核心痛点（高频细节丢失、形态建模单一、损失函数不匹配裂纹几何、裂纹检测碎片化）；

4. 段落 4：本文核心思想：**架构与损失协同形态感知联合设计**；

5. 段落 5：分层罗列 5 项创新点，区分核心算法创新与工程优化；

6. 段落 6：全文章节组织安排。

## 2\.2 Section II RELATED WORK 相关工作优化

原始 4 小节内容重叠，缺少每小节收尾差异化总结，无法凸显本文创新优势
优化子小节划分：
A\. Pavement Distress Detection Methods
B\. Lightweight YOLO \& Vision Mixture of Experts
C\. Feature Enhancement \& Channel Attention Mechanism
D\. Bounding Box Regression Loss Functions
统一要求：每小节末尾增加总结句，点明现有方法局限性，引出本文改进思路。

## 2\.3 Section III METHODOLOGY 方法（核心章节，逻辑割裂严重）

原始顺序：FDDE → MorphSparseMoE → ECA → SPPF\-CSPC → Loss → Post\-processing
**推荐重构顺序（强制调整）**
3\.1 Overall Architecture of BMS\-YOLO（先放网络总图概述）
3\.2 Frequency\-Direction Detail Enhancement \(FDDE\)
3\.3 Morphology\-Aware Sparse MoE \(MorphSparseMoE\) \& BMSC2f Block
3\.4 Lightweight Multi\-Scale Fusion: SPPF\-CSPC \+ ECA Attention
3\.5 Joint Loss: WIoU \+ Box Morphology Consistency Loss \(Two\-stage Training\)
3\.6 Inference Post\-processing: Topology\-Guided Box Fusion
整改说明：原 FDDE 与 MoE 分散，BMSC2f 融合模块逻辑断裂；先总览网络再分模块讲解，符合审稿人阅读习惯。

## 2\.4 Section IV EXPERIMENTS 实验论证强化

现有缺陷：消融仅逐步叠加、缺少单一模块消融、无边缘设备测速、长尾类别分析单薄
要求补充实验内容：

1. 单一组件消融实验（单独添加 FDDE / 单独添加 MoE，量化独立增益）；

2. Jetson 嵌入式 GPU 边缘推理 FPS 测试，贴合无人机机载部署场景；

3. 裂纹碎片框数量定量统计（NMS vs 拓扑融合）；

4. MorphSparseMoE top\-k 超参消融（k=1/2/3 性能对比）；

5. 不同 λ 衰减策略对比实验。

## 2\.5 Section V CONCLUSION \& Limitation 结论优化

现有缺陷：重复摘要、局限性描述简略、未来工作无分层优先级
修改要求：

1. 升华「架构 \- 损失协同设计」核心主线，不重复摘要文字；

2. 分点客观阐述模型短板：低对比度裂纹、密集网状裂缝、推理速度衰减、长尾坑槽精度小幅下降；

3. 分层规划未来工作：短期部署优化、中期算法改进、长期弱监督学习研究。

---

# 3 英文学术表达润色规范（Claude Code 全文语法修正指令）

## 3\.1 句式整改要求

1. 拆分全部超长复合句（单句超过 3 行必须拆分）；

2. 减少过度被动语态，工程论文优先使用主动语态 `we propose / we design / we conduct`；

3. 删除口语化模糊词汇，统一严谨学术书面用词；

4. 段落间补充过渡连接词：However, Furthermore, In contrast, Specifically, To further validate, As shown in。

## 3\.2 全文术语统一（强制全局替换）

1. bounding box /box：首次全称，后文简写统一；

2. UAV imagery：全文统一，禁止混用 UAV aerial images；

3. mAP50:95：固定格式，禁止 mAP@0\.5:0\.95；

4. distress（总称）/distresses（多病害实例）单复数严格区分；

5. feature map /feature representation 全文统一。

## 3\.3 时态、语法统一规则

1. 已有文献研究：过去时 \(proposed, designed\)；

2. 本文模型、模块定义：一般现在时；

3. 实验结果描述：过去时；

4. 补充缺失冠词、修正名词单复数、消除介词错误。

---

# 4 图表专项优化指令（直接复制给 Claude 生成图文描述）

## 4\.1 新增定量图表文字描述模板

1. 网络架构总图：标注输入 640×640，Stem 层 FDDE、Backbone 堆叠 BMSC2f、Neck SPPF\-CSPC\+ECA、解耦检测头、后处理拓扑融合输出，标注下采样倍数、通道维度。

2. FDDE 模块图：高低频分支分离、1×5/5×1 方向卷积、自适应门控融合、残差连接完整流程。

3. MorphSparseMoE 图：4 类专家分支、轻量路由网络、Top\-k=2 稀疏激活、加权输出流程。

4. 消融柱状图：X 轴：基线、仅架构、\+WIoU、\+MorphLoss、完整 BMS\-YOLO；Y 轴 mAP50/mAP50:95，两组并列柱状。

5. λ 折线图：横轴 λ 取值 0\~0\.02，纵轴 mAP50，两条曲线区分单阶段训练、两阶段预训练微调。

6. 类别对比柱状图：6 类病害，并列 YOLOv8n 与 BMS\-YOLO mAP50 数值，标注长尾样本数量注释。

7. 轻量化权衡散点图：横轴参数量 M，纵轴 FPS，标注 YOLOv8n、YOLOv10n、BMS\-YOLO、RT\-DETR\-l 数据点。

## 4\.2 原有定性检测效果图优化

1. 每张子图增加局部放大框，圈出细微裂纹、碎片化检测区域；

2. 类别差异化配色：裂纹红色、坑槽黄色、修补区域绿色；

3. 检测框上方标注类别 \+ 置信度；

4. 每张图底部标注统计量：总检测框数量、漏检目标数量；

5. 补充低光照、阴影、密集网状裂纹极端场景可视化对比。

---

# 5 学术创新论证深度提升（Claude Code 重点扩写段落）

1. 强化全文主线「架构与损失协同设计」：引言、方法、消融实验、结论四段反复呼应，作为核心理论贡献；

2. 突出 MorphSparseMoE 差异化创新：现有视觉 MoE 基于全局特征路由，本文首次面向病害几何形态设计四类专用专家分支，对比现有 MoE 工作明确区分；

3. 深挖形态一致性损失理论价值：log 空间长宽比约束解决细长裂纹 IoU 敏感缺陷，对比 CIoU 静态长宽正则，突出病害专属几何先验；

4. 放大拓扑并查集后处理工程价值：现有裂纹检测仅依赖 NMS，本文拓扑连通融合大幅降低漏检，贴合道路巡检实际需求；

5. 客观扩充局限性分析，体现研究完整性，提升审稿人好感。

---

# 6 实验补充完善指令（Claude Code 新增实验段落）

1. 公平性声明：所有对比模型训练轮次、优化器、数据增强、输入分辨率完全统一，单独分段写在实验设置；

2. 复杂度理论分析：定量计算 FDDE、MorphSparseMoE 带来的参数量、FLOPs 增量，解释 FPS 下降内在原因；

3. 可选加分项：补充额外公开路面病害数据集泛化实验，证明模型泛化能力；

4. 消融实验补充 top\-k 路由超参对比，论证 k=2 为精度与速度最优平衡点。

---

# 7 投稿前自查清单（Claude Code 自动校验）

## 7\.1 格式校验

* [ ] 标题、作者单位、基金、通讯作者完整；

* [ ] 摘要 150–250 词，索引词 3–5 个；

* [ ] 全部表格为 IEEE 三线表，图题位于图片下方；

* [ ] 公式居中右编号，变量全部释义；

* [ ] 参考文献数字顺序编码，正式期刊文献占比≥70%。

## 7\.2 内容校验

* [ ] 全文自定义缩写首次出现附带完整全称；

* [ ] 网络架构总图 \+ 三大模块子图齐全；

* [ ] 消融实验包含单一模块消融 \+ 逐步叠加消融；

* [ ] 定量柱状 / 折线可视化图表完整；

* [ ] 局限性、未来工作客观分层阐述。

## 7\.3 语言校验

* [ ] 无超长复合句，术语全文统一；

* [ ] 时态、单复数、冠词无语法错误；

* [ ] 段落过渡逻辑词完善，行文流畅。

## 7\.4 创新校验

* [ ] 5 项创新分层清晰，每项均有实验数据支撑；

* [ ] 「架构 \- 损失协同设计」主线贯穿全文；

* [ ] 与现有相关工作差异化描述明确。

---

# 8 交付给 Claude Code 的统一执行指令（可直接复制粘贴）

```Plain Text
你现在是IEEE Access专业英文论文编辑，按照下方完整Markdown修改意见对BMS-YOLO论文全文执行以下操作：
1. 格式标准化：统一IEEE期刊排版规范，修正标题大小写、表格转为三线表、规范公式与图表标注、标准化参考文献；
2. 英文润色：拆分长难句、统一术语、修正时态语法、补充段落过渡词、控制摘要词数150-250；
3. 章节重构：按照指定顺序重排Methodology小节，优化引言、相关工作、实验、结论逻辑递进关系；
4. 内容补充：补全缺失的变量释义、公平性实验说明、消融实验描述、局限性与分层未来工作；
5. 图文配套：生成所有新增图表的标准化文字描述，优化现有定性效果图说明；
6. 创新强化：全文重点突出「架构+损失协同形态感知」核心主线，放大MorphSparseMoE、形态损失、拓扑融合差异化创新；
7. 输出完整修订后论文正文，同时附一份分点修改说明清单，标注每一处关键改动位置与修改理由。
```

## 使用说明

1. 复制全部上述 Markdown 内容，保存为 `.md` 文件；

2. 将 md 文件 \+ 原始论文 PDF 文本一起上传至 Claude Code；

3. 粘贴文末统一执行指令，一键完成全文自动优化、重写、格式修正。

> （注：部分内容可能由 AI 生成）
