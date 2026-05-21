---
layout: paper
paper_order: 4
title: "WHOLE: World-Grounded Hand-Object Lifted from Egocentric Videos"
zhname: "WHOLE：用扩散先验把第一视角里的手和物体一起 lift 到世界坐标"
category: "人体动作生成"
---

# WHOLE: World-Grounded Hand-Object Lifted from Egocentric Videos
**用扩散先验把第一视角里的手和物体一起 lift 到世界坐标**

> 📅 阅读日期: 2026-05-21
>
> 🏷️ 板块: 14 Human Motion · 手-物联合重建 / 第一视角视频 / 生成式先验引导
>
> 🔁 推进轨: 模块轮转（13_Physics-Based_Animation → **14_Human_Motion**）

---

## 📋 基本信息

| 项目 | 链接 |
|---|---|
| 时间 | 2026 年 2 月 |
| arXiv | [2602.22209](https://arxiv.org/abs/2602.22209) |
| HTML | [arxiv.org/html/2602.22209v1](https://arxiv.org/html/2602.22209v1) |
| PDF | [arxiv.org/pdf/2602.22209](https://arxiv.org/pdf/2602.22209) |
| 项目主页 | [judyye.github.io/whole-www](https://judyye.github.io/whole-www/) |
| 代码 | 暂未公开（作者主页 [JudyYe](https://github.com/JudyYe) 历史项目多在论文后开源，可持续关注） |
| 作者 | Yufei (Judy) Ye, Jiaman Li, Ryan Rong, C. Karen Liu |
| 机构 | Stanford University · Amazon FAR (Frontier AI & Robotics) |

> 来源：YanjieZe/awesome-humanoid-robot-learning · 14 Human Motion Analysis and Synthesis 第 478 项。

---

## 🎯 一句话总结

> 第一视角视频里手和物体动不动就互相遮挡、还会出画——WHOLE 训练一个**手-物联合扩散先验**，再用 VLM 抠出来的**接触线索 + 物体/手分割掩膜**做**测试时引导**，一次性给出世界坐标系下的 **MANO 手姿 + 6D 物体轨迹**，比"分头估 + 后处理"显著更稳。

---

## 📌 英文缩写速查

| 缩写 | 含义 |
|---|---|
| HOI | Hand-Object Interaction，手-物交互 |
| MANO | A Skinned Multi-Person Linear Model for Hands，常用的可微分手模型 |
| 6D Pose | 3D 平移 + 3D 旋转，即物体在世界坐标下的位姿 |
| VLM | Vision-Language Model，本文用于提取"哪只手是否与物体接触" |
| HOT3D | Meta 发布的第一视角手-物 3D 跟踪数据集，本文训练 / 评测基准 |
| SDF | Signed Distance Field，作者历史工作（G-HOP）里用过的几何表征，本文沿用相关思路 |

---

## ❓ 论文要解决什么问题？

**第一视角（egocentric）视频**里同时恢复"手 + 被操作物体"的世界坐标轨迹，至少踩三个坑：

1. **互相遮挡**：手抓物体时，手把物体挡住一半、物体也把手挡住一半，单目模型对任何一边都吃力；
2. **频繁出画**：人头一转，物体瞬间出画、过几秒再回来，传统单帧估计器直接失锁；
3. **米尺度世界系不一致**：常见做法是「手用一个模型估、物体用另一个模型估、再后处理拉齐」，结果是接触点漂移、轨迹卡顿、米尺度不对齐。

传统流派要么只做**手**（FrankMocap、HaMeR），要么只做**物体**（FoundationPose、MegaPose），凑在一起常常违反物理接触。WHOLE 的目标是把「手 + 物体 + 接触」一次性 lift 到统一世界坐标系，给下游单目重建 / 物理动画 / **人形机器人模仿** 提供干净的轨迹。

---

## 🔧 方法详解 —— 扩散先验 + 测试时引导

### 核心想法

**先在干净数据上学一个 "手 + 物体" 的联合运动先验，再在测试时用视频观测把先验"掰"到符合视频的轨迹上。**

这其实是 image-to-3D 中很流行的「learned prior + classifier guidance」范式被搬到了 4D 手-物重建里——只不过这里的先验不是 image 先验，而是**hand-object motion prior**。

### 三个关键组件

| 组件 | 作用 | 关键设计 |
|---|---|---|
| ① 手-物联合扩散先验 | 学到「手 MANO 参数 + 6D 物体轨迹 + 接触」的联合分布 | 在 HOT3D 上训练，输入是手参数序列 + 物体位姿序列，扩散在它们的联合空间里 |
| ② VLM 增强的接触检测 | 给"哪只手 / 何时 / 是否接触物体"提供可靠信号 | 用空间提示（spatially grounded visual prompts）+ 5 张 in-context 校准样本，把接触 F1 从 **57% → 81%** |
| ③ 测试时引导（test-time guidance） | 把先验生成的轨迹"对齐"到视频观测 | 引导信号：**2D 物体/手分割掩膜投影一致性** + **VLM 给出的接触一致性** + 物体模板匹配 |

### 训练 vs 测试两条流水线

- **训练阶段**：完全在干净数据（HOT3D 等）上学扩散去噪，**不**看视频特征，只学 motion prior 本身。这一步类似 PhysDiff / MDM 在动作生成里的做法。
- **测试阶段**：给定一段第一视角视频 + 物体模板（已知 mesh），先跑现成模型抠出每帧的手/物体 2D mask 与候选 6D 位姿，然后用扩散反向过程，每一步去噪都额外加入 guidance gradient 拉齐到观测（mask 重投影 + 接触掩膜）。

### 为什么"联合先验"比"分头估 + 后处理"强

- **遮挡互补**：手被挡时，物体姿态 + 接触提示反推手大致在哪；物体被挡时，手姿反推物体被握成什么样；
- **出画兜底**：当物体短暂离开视野，先验仍可"想象出"合理的物体轨迹，等下次入画时再被观测拉回；
- **接触一致**：联合分布里"手指与物体表面零距离"是被显式建模的，分头估几乎不可能保证这一点。

---

### 🧭 整体流程（mermaid）

<div class="mermaid">
flowchart LR
    subgraph IN["🎥 输入"]
        V["第一视角视频<br/>(Egocentric RGB)"]
        T["物体模板<br/>(已知 mesh)"]
    end

    subgraph OBS["👁 视频观测提取"]
        M1["2D 分割掩膜<br/>(SAM / Lang-SAM)"]
        M2["接触线索<br/>(VLM + 空间提示 + 5-shot 校准<br/>F1: 57% → 81%)"]
        M3["候选 6D 物体位姿<br/>(FoundationPose 等)"]
    end

    subgraph PRIOR["🧠 手-物联合扩散先验"]
        P1["HOT3D 上预训练<br/>(MANO 手 + 6D 物体)"]
        P2["联合分布<br/>p(手序列, 物体序列, 接触)"]
        P1 --> P2
    end

    subgraph GUIDE["🎯 测试时引导生成"]
        G1["扩散反向去噪"]
        G2["Mask 重投影一致性<br/>+ 接触一致性<br/>+ 模板匹配"]
        G1 <--> G2
    end

    V --> M1
    V --> M2
    V --> M3
    T --> M3
    T --> G2

    M1 --> G2
    M2 --> G2
    M3 --> G2

    P2 --> G1
    G1 --> OUT["📦 世界坐标下<br/>手 MANO 轨迹 + 物体 6D 轨迹<br/>(接触一致 / 出画鲁棒)"]

    OUT --> DS1["🖼 单目 HOI 重建训练数据"]
    OUT --> DS2["🤖 人形机器人手部模仿"]
    OUT --> DS3["🎮 物理动画 / 接触感知"]

    style IN fill:#fff4e6,stroke:#e67e22,color:#7d3c08
    style OBS fill:#e8f4fd,stroke:#1f78b4,color:#0b3954
    style PRIOR fill:#eef7ee,stroke:#27ae60,color:#0f3d1e
    style GUIDE fill:#f4eafd,stroke:#7e57c2,color:#311b6c
    style OUT fill:#fff8dc,stroke:#b8860b,color:#5b3a00
</div>

---

## 💡 核心贡献

1. **首个把"手 + 物体"作为联合分布学先验**的第一视角视频 4D lift 方法，跳出"分别估 + 后处理"路线；
2. **VLM + 空间提示 + 5-shot 校准** 的接触检测方案，F1 从 57% 跳到 81%，把过去最难提的接触信号变成可用引导；
3. 在 **HOT3D** 上拿到手姿、6D 物体位姿、以及二者相对关系三个指标的 **SOTA**；
4. 输出是干净的「世界坐标 + 接触一致」轨迹，可直接喂给后续的物理仿真 / 人形机器人手部模仿。

---

## 📊 与相关工作的关系

| 路线 | 代表方法 | 是否联合建模 | 接触一致性 | 世界坐标 |
|---|---|---|---|---|
| 单目手姿 | FrankMocap / HaMeR | ❌（只手） | ⚠️ 后处理 | ⚠️ 相机系 |
| 单目物体 6D | FoundationPose / MegaPose | ❌（只物体） | ❌ | ⚠️ |
| 单视频 HOI 重建 | HOLD / DiffHOI（作者历史工作） | ⚠️ 部分 | ⚠️ | ⚠️ |
| 4D 手轨迹 | HaPTIC（作者同期） | ❌（只手） | — | ✅ |
| **WHOLE（本文）** | **手 + 物体联合扩散先验** | **✅** | **✅** | **✅** |

> 作者 Yufei Ye 一脉的工作（iHOI → Affordance Diffusion → DiffHOI → G-HOP → HaPTIC → WHOLE）是一条非常清晰的「生成式先验 × HOI 重建」研究主线，WHOLE 是把 G-HOP（generative HOI prior）从静态扩展到 4D 时序、并且首次能直接吃第一视角视频的版本。

---

## 🤖 对人形机器人学习的启发

- **干净的手部参考动作**：人形机器人灵巧操作的最大痛点是「人手怎么抓的、给机器人手 retarget 的时候要不要保接触」。WHOLE 把接触一致性写进先验，输出的 MANO 序列直接是"贴住物体"的，retarget 到 Inspire Hand / Shadow Hand 时少很多接触穿模；
- **物体世界轨迹一并到位**：与 ASAP / SONIC / RGMT 这种「人体动作 → 人形机器人」工作互补——后者主要管 root + 全身，WHOLE 补上"被操作物体在世界系里怎么走"，对**双手操作 + 物体跟踪**类任务（如 HOMIE、Dex Teleop）非常关键；
- **数据扩展**：第一视角视频在网上几乎无限，WHOLE 提供了一条**把这些视频变成 4D HOI 训练数据**的可行路径，下游 Diffusion Policy / 模仿学习类工作能直接用；
- **Real2Sim 物体**：物体 6D 轨迹 + mesh 模板就可以直接塞进 Isaac Lab / MuJoCo 重放，方便做接触感知的 sim-to-real 训练。

---

## 📁 资源对照

| 资源 | 内容 |
|---|---|
| [arXiv 2602.22209](https://arxiv.org/abs/2602.22209) | 论文正文 |
| [HTML 版本](https://arxiv.org/html/2602.22209v1) | 在线阅读，含图表 |
| [项目主页](https://judyye.github.io/whole-www/) | 视频 demo + 论文 PDF 入口 |
| [作者历史代码合集](https://github.com/JudyYe) | iHOI / DiffHOI / HaPTIC 等可作为本文实现参考 |
| 训练评测数据 | [HOT3D](https://facebookresearch.github.io/hot3d/)（Meta） |

---

## 🎤 面试参考

**Q：为什么非要"联合建模"手和物体？**
A：因为单独估的时候，遮挡和出画导致的失锁是不可避免的——而"手贴住物体" / "手离开物体"这种事件本身就是手-物的联合事件。把它们放进同一个先验分布里训练，遮挡那侧可以靠未被遮挡的那侧 + 接触状态来反推，物理一致性也内生地被先验所偏好。

**Q：测试时引导和端到端预测相比，优势是什么？**
A：端到端预测一旦遇到分布外（罕见物体、奇怪握法），会"硬猜"出离谱姿态；而先验 + 引导的好处是：**先验保证生成的轨迹是合理的手-物运动**，引导只负责把它对齐到当前视频。换句话说，**生成质量由先验保底**，**视频忠实度由引导调节**，两者解耦，更鲁棒。

**Q：F1 从 57% → 81% 这么大的提升是怎么来的？**
A：本质是把"接触判定"做成一个 VLM 任务，但加了三件套：① **空间提示**（把候选物体和手在图上用框标出来再问 VLM）；② **JSON 输出 + 校验规则**约束格式；③ **5 张 in-context 校准样本**消除 VLM 的系统性偏置（容易判正）。这条思路其实对 humanoid 仓库里"用 VLM 抽接触/抓取信号"的工作（如 VIGOR、视觉 loco-mani）非常有借鉴价值。

**Q：和 EmbodMocap、HUMOTO 这些数据/重建工作怎么比？**
A：颗粒度不同。EmbodMocap 偏「全身 + 场景」的米尺度对齐，HUMOTO 偏棚内多视图人-物数据集，WHOLE 专注「手 + 被操作物体」这个最难、最缺数据的尺度。三者其实是互补关系：人形机器人 motion tracking 需要全身（EmbodMocap），但末端灵巧操作必须要 WHOLE 这一层。

---

## 🔗 相关阅读

- **作者前作（同一研究线）**：
  - [iHOI](https://judyye.github.io/ihoi/)：单图重建手中物体；
  - [DiffHOI](https://judyye.github.io/diffhoi-www/)：扩散引导的日常 HOI 视频重建；
  - [G-HOP](https://judyye.github.io/ghop-www/)：静态手-物联合生成先验，WHOLE 的"先验基石"；
  - [HaPTIC](https://judyye.github.io/haptic-www/)：4D 手轨迹预测，与 WHOLE 同期。
- **同期数据/重建**：EmbodMocap（[arXiv 2602.23205](https://arxiv.org/abs/2602.23205)）、HUMOTO（[arXiv 2504.10414](https://arxiv.org/abs/2504.10414)）、ForeHOI（[arXiv 2602.06226](https://arxiv.org/abs/2602.06226)）；
- **基准数据集**：[HOT3D](https://facebookresearch.github.io/hot3d/)（Meta 多视 + Aria）；
- **人形机器人下游**：HOMIE（灵巧操作遥操作）、iDP3（3D 扩散策略），都可以以 WHOLE 输出为参考动作来源。
