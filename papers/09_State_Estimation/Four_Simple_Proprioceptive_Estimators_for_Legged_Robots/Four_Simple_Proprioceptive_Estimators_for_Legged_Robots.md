---
layout: paper
paper_order: 9
title: "Four Simple Proprioceptive Estimators for Legged Robots"
zhname: "四个由浅入深的本体感知估计器：从 InEKF 到「按接触事件建状态」的固定滞后平滑器，全部开源进 GTSAM"
category: "State Estimation"
---

# Four Simple Proprioceptive Estimators for Legged Robots
**用「接触事件」而非固定高频时钟来建状态：把 IMU 预积分 + 足落点（foothold）地标塞进一个小因子图，从 InEKF 一路升级到带演化偏置的固定滞后平滑器**

> 📅 阅读日期: 2026-06-17
>
> 🏷️ 板块: 09 State Estimation · 本体感知里程计 · 因子图 / 固定滞后平滑 · IMU 预积分 · 接触辅助
>
> 🔁 推进轨: 模块轮转（08_Navigation → **09_State_Estimation**）

---

## 📋 基本信息

| 项目 | 链接 |
|---|---|
| arXiv | [2605.23100](https://arxiv.org/abs/2605.23100) |
| HTML | [在线阅读](https://arxiv.org/html/2605.23100) |
| PDF | [下载](https://arxiv.org/pdf/2605.23100) |
| 源码（GTSAM 示例） | [borglab/gtsam · LeggedEstimatorReplayExample.cpp](https://github.com/borglab/gtsam/blob/develop/examples/LeggedEstimatorReplayExample.cpp) ✅ |
| 源码（ROS2） | [ChiyunNoh/GTSAM-Legged-Estimator-ROS2](https://github.com/ChiyunNoh/GTSAM-Legged-Estimator-ROS2) ✅ |
| **发布时间** | 2026-05-21（arXiv） |
| 作者 / 机构 | Frank Dellaert、Chiyun Noh、Varun Agrawal、Ayoung Kim（GTSAM 作者团队 / Georgia Tech & KAIST 体系） |

**机器人平台**：四足 **Boston Dynamics Spot**，评测用 **GaRLILEO** 数据集（室内外、含上下楼/斜坡序列，LiDAR 轨迹作真值）

**领域归属**：足式机器人**本体感知（IMU + 腿运动学 + 接触）浮动基座状态估计**——滤波 vs. 因子图平滑的统一对比

---

## 🎯 一句话总结

本体里程计的老问题是 **IMU 会漂**，而腿式机器人有个免费的强约束：**脚一旦踩地，落点（foothold）在世界系里就是固定的**。本文不发明新算法，而是把这条思路做成**四个由浅入深、共享同一套「接触事件 + IMU 预积分」骨架**的估计器：① 经典 **接触辅助 InEKF**（Hartley 那套，顺序更新）→ ② 把顺序更新换成**小因子图联合解多脚接触**的图更新滤波 → ③ 把图扩成短时间窗、为每个**接触片段（contact episode）显式建一个落点地标变量**的**固定滞后平滑器（单一持久偏置）** → ④ 同样的平滑器，但**把 IMU 偏置建成随机游走、每次接触都给一个新偏置变量**。关键洞见是**「按接触事件而非固定高频时钟建状态」**：只在触地（或最多隔 100ms）时新建一个基座状态，中间的高频 IMU 用**预积分**压缩成一条因子，既省算力又让滤波器对**低频/延迟/重复接触**信息更鲁棒，比高频接触更新「漂得更少」。四个变体**全部进了 GTSAM 并配 ROS2 实现**，是一份极佳的可复现教学/工程参考。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 解释 |
|---|---|---|
| InEKF / IEKF | (Contact-aided) Invariant EKF | 不变扩展卡尔曼滤波，足式估计的事实标准基线 |
| Foothold | 足落点 | 脚踩地期间在世界系中固定的接触点，本文当作地标变量 |
| Contact Episode | 接触片段 | 一只脚从触地到离地的一段；离地再踩 = 新片段 = 新落点变量 |
| Preintegration | IMU 预积分 | 把两事件间高频 IMU 压成一条相对增量因子（Forster 2017） |
| Fixed-Lag Smoother | 固定滞后平滑器 | 只在短时间窗内联合优化、窗外变量边缘化 |
| Factor Graph | 因子图 | 把测量当因子、状态当节点的概率图，GTSAM 的核心 |
| SE₂(3) / SEₖ₊₂(3) | 矩阵李群 | 同时编码姿态/位置/速度（及多接触）的状态表示 |
| APE / RPE | Absolute / Relative Pose Error | 绝对 / 相对位姿误差，APEz 专指竖直方向漂移 |

---

## ❓ 论文要解决什么问题？

足式本体估计文献里方法五花八门（InEKF、神经测量网络、各种平滑器），但**彼此割裂、难以横向比较**：到底是「滤波 vs. 平滑」、「顺序更新 vs. 联合更新」、「固定偏置 vs. 演化偏置」哪一项真正带来收益？本文的目标不是刷 SOTA，而是：

1. **统一骨架**：用同一套「接触事件 + IMU 预积分 + 落点地标」的因子图语言，把从 InEKF 到固定滞后平滑器的方法装进**一个连续谱**，使各设计选择**可控变量地对比**；
2. **回答几个工程问题**：接触更新该用**高频时钟**还是**按事件触发**？IMU 偏置该当**常量**还是**随机游走**？平滑相比滤波在**带高程变化的地形**上值不值？
3. **可复现**：把四个变体全部落进 GTSAM + ROS2，让读者能直接跑、直接换。

---

## 🔧 方法拆解

### 0. 共享状态：姿态 + 位置 + 速度 + IMU 偏置

浮动基座状态含**姿态、位置、速度、IMU 偏置**；滤波侧用不变误差表示（SEₖ₊₂(3) 半直积），平滑侧把同样的量放进因子图节点。

### 1. 估计器①：接触辅助 InEKF（基线）

照搬 Hartley 等人的不变 EKF：IMU 做预测，**每只接触脚的零速/落点约束**做顺序测量更新。问题：多脚同时接触时是**逐个顺序更新**，且接触按高频时钟刷新。

### 2. 估计器②：图更新滤波——把顺序更新换成小因子图

保持滤波结构，但把「一次更新」替换为**一个小型非线性因子图**，**同时联合求解所有当前接触**，而不是一只脚一只脚地改。对比①几乎等价 → 说明**测量更新方式本身收益有限**，瓶颈不在这。

### 3. 估计器③：固定滞后平滑器（单一持久偏置 FL-Single）

把上面的图**沿短时间窗展开**，核心改动是**为每个接触片段显式引入一个世界系落点地标 fᵢ,ₑᴺ**（i = 脚，e = 第几次接触）。脚抬起再落 = 新 episode = 新落点变量；旧 episode 移出窗口就边缘化。偏置用**一个持久变量 + 先验**。

### 4. 估计器④：演化偏置平滑器（FL-Combined）

结构同③，但**偏置建成随机游走轨迹**，每个接触事件给一个偏置节点、相邻偏置用随机游走因子相连——让偏置随时间慢漂得到更好补偿。

### 5. 贯穿全篇的两个关键设计

- **按接触事件建状态**：只在**触地或最多隔 100ms** 时新建基座状态，中间高频 IMU 用 **预积分（Forster 2017）** 压成一条相对 SE₂(3) 增量因子 → 优化窗口紧凑，且天然容纳延迟/重复接触；
- **落点当地标而非滤波器里的固定脚槽**：用显式 fᵢ,ₑᴺ 变量 +（可选）**高程先验** 约束，比把脚塞进状态向量更灵活。

---

## 🧭 整体流程（mermaid）

<div class="mermaid">
flowchart TB
    subgraph SENS["🦿 本体传感器（无视觉/LiDAR）"]
        IMU["📡 IMU 高频<br/>(陀螺 + 加速度)"]
        ENC["⚙️ 关节编码器<br/>(腿运动学)"]
        CON["🦶 接触检测<br/>(触地 / 离地事件)"]
    end

    subgraph PRE["🟨 事件驱动前处理"]
        EV["⏱️ 接触事件 / 超 100ms<br/>→ 新建基座状态节点"]
        PI["🧮 IMU 预积分<br/>两事件间压成一条因子"]
        FH["📍 落点地标 fᵢ,ₑᴺ<br/>每个接触片段一个"]
    end

    subgraph GRAPH["🟦 因子图 (GTSAM)"]
        IF["IMU 预积分因子"]
        CF["接触因子<br/>zᵢᴮ=(Rᴺᴮ)ᵀ(fᵢᴺ−pᴮᴺ)"]
        HF["高程先验(可选)"]
        BF["偏置因子<br/>常量 / 随机游走"]
    end

    subgraph EST["🟧 四个估计器谱系"]
        E1["① InEKF 顺序更新"]
        E2["② 图更新滤波"]
        E3["③ FL-Single 固定滞后<br/>单一持久偏置"]
        E4["④ FL-Combined<br/>演化偏置"]
        OUT["📈 基座位姿/速度/偏置"]
    end

    IMU --> PI --> IF
    CON --> EV
    ENC --> FH --> CF
    EV --> GRAPH
    IF --> GRAPH
    CF --> GRAPH
    HF --> GRAPH
    BF --> GRAPH
    GRAPH --> E1 --> OUT
    GRAPH --> E2 --> OUT
    GRAPH --> E3 --> OUT
    GRAPH --> E4 --> OUT

    style SENS fill:#fff7e0,stroke:#d4a017
    style PRE fill:#fef5d4,stroke:#caa024
    style GRAPH fill:#e8f4fd,stroke:#1f78b4
    style EST fill:#fde8e8,stroke:#c0392b
</div>

---

## 💡 核心贡献

1. **统一谱系**：用一套「接触事件 + IMU 预积分 + 落点地标」的因子图骨架，把 InEKF → 图更新滤波 → 固定滞后平滑（单一/演化偏置）串成可控变量对比。
2. **事件驱动接触更新**：按触地事件（或 ≤100ms）建状态，比高频接触刷新**漂移更小**。
3. **落点地标化**：把每个接触片段建成显式世界系落点变量（可加高程先验），比固定脚槽更灵活，便于多接触联合求解。
4. **全部开源进 GTSAM + ROS2**：四个变体可直接复现、横评、替换，工程/教学价值高。

---

## 📊 关键发现

| 维度 | 结果 |
|---|---|
| 平移 APE（3D 序列 Overpass） | **FL-Combined 2.604m** ≪ Pronto 4.039m ≪ MUSE 6.507m |
| 旋转 APE（2D 序列 Atrium） | **FL-Combined 1.092°** < Inv. EKF 1.935° |
| 竖直漂移 APEz（CorriLoop） | **FL-Single 0.525m 反优于 FL-Combined 1.776m**——演化偏置在台阶/斜坡上有权衡 |
| ① vs. ②（InEKF vs. 图更新） | 几乎无差 → **测量更新方式本身收益有限** |
| 接触更新调度 | 事件驱动比高频刷新「**明显更少漂移**」 |

> 📌 数据来自论文实验表；平台 Spot，数据集 GaRLILEO（LiDAR 真值）。**结论：FL-Single 是稳健中庸之选**——水平精度优于纯滤波，竖直精度在楼梯/斜坡上又比 FL-Combined 更稳；FL-Combined 水平最准但竖直有起伏。

---

## 🤖 对人形 / 状态估计领域的意义

| 方向 | 含义 |
|---|---|
| **滤波 vs. 平滑有了公平基准** | 同骨架横评，避免「换了算法又换了实现」导致的不可比，人形上选型可直接参考 |
| **事件驱动思想可迁双足** | 人形步态接触事件清晰、相位切换频繁，「按事件建状态 + 预积分」比固定时钟更契合 |
| **落点地标 + 高程先验** | 上下楼梯/斜坡场景对竖直漂移敏感，本文的高程先验与 episode 化落点对人形登楼很有用 |
| **GTSAM 现成可叠后端** | 输出标准因子图，天然可接 SLAM / 多传感器融合后端 |

---

## 🎤 面试参考

**Q：为什么足式机器人能靠「接触」抑制 IMU 漂移？**
A：IMU 双重积分会指数级漂移，而脚一旦踩地，其落点在世界系里是**固定且可由腿运动学观测**的。把这个固定落点当约束（零速/落点因子），就给基座位置/速度一条强校正，相当于不断「锚」回环境。

**Q：本文四个估计器的递进逻辑是什么？**
A：① InEKF 是顺序更新滤波基线；② 把顺序更新换成小因子图联合解多脚——验证「更新方式」本身收益不大；③ 再把图沿时间窗展开成固定滞后平滑、为每个接触片段建显式落点地标，并保留单一持久偏置；④ 进一步把偏置建成随机游走、每次接触给新偏置变量。一步步隔离出「平滑窗口」「落点地标」「偏置演化」各自的贡献。

**Q：为什么「按接触事件建状态」比固定高频更新好？**
A：固定高频会塞入大量冗余且噪声相关的接触更新、还难处理延迟/重复接触；按事件只在触地（或 ≤100ms）建一个状态节点，中间 IMU 用预积分压成一条因子，窗口更紧凑、计算更省，实验上漂移也更小。

**Q：FL-Single 和 FL-Combined 怎么选？**
A：FL-Combined（演化偏置）水平精度通常更高，但在上下楼/斜坡上竖直漂移 APEz 反而可能更差——偏置太灵活会被高程变化误带。FL-Single（单一持久偏置）是稳健折中：水平优于纯滤波，竖直又比 FL-Combined 稳。地形平坦选 Combined，地形起伏大选 Single。

---

## 🔗 相关阅读

- [Contact-Aided Invariant EKF (1904.09251)](https://arxiv.org/abs/1904.09251)：本文估计器①的直接出处，本仓库已有笔记
- [Learning Contact Representation for Leg Odometry (2606.05501)](https://arxiv.org/abs/2606.05501)：自监督学连续接触置信度喂 ESEKF，与本文「接触当因子」对照，本仓库已有笔记
- [InEKFormer (2511.16306)](https://arxiv.org/abs/2511.16306)：InEKF + Transformer 混合估计，本仓库已有笔记
- [Adaptive Invariant EKF (2510.16755)](https://arxiv.org/abs/2510.16755)：在线协方差自适应的接触可信度，本仓库已有笔记
- [Legged Robot State Estimation via Forward Kinematic and Preintegrated Contact Factors (1712.05873)](https://arxiv.org/abs/1712.05873)：预积分接触因子的早期工作，本仓库已有笔记

---

> 备注：本笔记基于 arXiv 摘要 + HTML 全文 + 公开搜索整理；部分数值以官方 PDF 表格为准。
