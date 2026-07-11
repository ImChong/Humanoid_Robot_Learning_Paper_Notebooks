---
layout: paper
paper_order: 1
title: "TACT-ful: Multi-Channel Terrain Affordance and Compliance Training for Payload-Robust Perceptive Humanoid Locomotion"
zhname: "TACT-ful：多通道地形可供性 + 负载柔顺训练的感知型人形行走"
category: "Locomotion"
---

# TACT-ful: Multi-Channel Terrain Affordance and Compliance Training for Payload-Robust Perceptive Humanoid Locomotion
**TACT-ful：用「多通道地形代价（平整/陡峭/速度可行性/前进爬升）」驱动落脚规划与密集奖励，再用「虚拟力矩柔顺训练」让下肢无需力传感器就能扛住负载扰动，端到端 PPO 一次训成、零样本上真机的感知型人形行走**

> 📅 阅读日期: 2026-07-11
>
> 🏷️ 板块: 05 Locomotion · 感知行走 · 地形可供性 · 负载鲁棒 · 落脚规划 · 端到端 PPO
>
> 🔁 推进轨: 模块轮转（04_Loco-Manipulation_and_WBC → **05_Locomotion**）

---

## 📋 基本信息

| 项目 | 链接 |
|---|---|
| 时间 | 2026 年 6 月 |
| arXiv | [2606.20645](https://arxiv.org/abs/2606.20645) · [PDF](https://arxiv.org/pdf/2606.20645) · [HTML](https://arxiv.org/html/2606.20645) |
| 项目页 | [fai-rl-tech.github.io/tact-locomotion](https://fai-rl-tech.github.io/tact-locomotion.github.io/) |
| 代码 | 见项目页（截至 2026-07-11 以项目页为准） |
| 作者 | Thanh Ly、Truong-Duy Dang、Chien Le、Tan-Dzung Do、Phuong Tuan Dat、Cuc T. Trinh、Vien Anh Ngo、An T. Le |
| 机构 | VinRobotics · VinUniversity（AI 研究中心）· TU Darmstadt |
| 实验平台 | 服务型人形（H1-2 级）· Unitree G1 跨形态验证 · VinFast 人形真机演示 |
| 主题 | cs.RO · 感知型人形行走 / 负载鲁棒 / 地形落脚 |

---

## 🎯 一句话总结

> 让人形机器人「背着东西上台阶」很难：既要看懂地形挑对落脚点，又要在负载扰动下不摔。TACT-ful 把这两件事拆开攻：**感知端**用四条互补的地形代价通道（平整 Q、陡峭 E、速度感知高度可行性 M、前进爬升奖励 b）同时驱动 GPU 并行的 **DCM 落脚规划器**和塑形每步的密集 **可供性奖励**，再配合「二次贝塞尔摆动 + 切线导向的落脚朝向」跨越台阶；**负载端**在训练里对身上采样点注入**虚拟力矩（virtual wrench）**造出物理一致的力与力矩，逼下肢学会「隐式阻抗」去吸收负载扰动——**全程不用力传感器**。整套用**标准 PPO 一次端到端训完**（无师生蒸馏），靠域随机化**零样本迁移到真机**。

---

## 📌 英文缩写速查

| 缩写 | 含义 |
|---|---|
| DCM | Divergent Component of Motion，发散运动分量（步态/落脚规划常用的稳定性量） |
| PPO | Proximal Policy Optimization，近端策略优化 |
| Wrench | 力旋量：力 + 力矩的六维统一表示 |
| Affordance | 可供性：地形「能不能踩、好不好踩」的可操作性度量 |
| Riser | 台阶竖板高度（阶高） |
| OOD | Out-of-Distribution，分布外（此处指训练未覆盖的更高阶高） |

---

## ❓ 论文要解决什么问题？

服务型人形常需**边走边搬运**，这对行走策略提出两个叠加难题：

1. **感知落脚**：在台阶、斜坡等结构化地形上，要从高度图里挑出**既平整又可达**的落脚点，纯「位置跟踪」不够——还要控制**脚的朝向**才能干净地跨过竖板、稳稳落在踏面。
2. **负载鲁棒**：背上 10–15 kg 负载（尤其**手臂外伸的力矩主导负载**）会显著改变动力学，若靠力/力矩传感器闭环则成本高、易噪声。

作者主张**不必分成「先规划再跟踪」的两段式**，而是把地形可供性与负载柔顺**一起塞进一个端到端 RL 策略**里协同学习。

---

## 🔧 方法详解

### 1. 多通道地形可供性（Multi-Channel Terrain Affordance）
构造四条互补代价 / 奖励通道：

- **平整 Q**：落脚区域越平越好；
- **陡峭 E**：惩罚坡度过大的落点；
- **速度感知高度可行性 M**：结合当前速度判断该高度差是否「够得着」；
- **前进爬升奖励 b**：鼓励向上跨越、避免原地踏步。

这四通道**同时**做两件事：驱动一个 **GPU 并行的 DCM 落脚规划器**给出目标落点，并塑形**每步的密集可供性奖励**指导策略。

### 2. 摆动轨迹与落脚朝向
用**二次贝塞尔曲线**生成摆动腿轨迹，带**自适应顶点偏置**；再用**切线导向的落脚朝向控制**，让脚在跨竖板、踩踏面时朝向正确——超越了只跟踪落脚「位置」的做法。

### 3. 负载柔顺训练（Virtual Wrench Injection）
训练时在身上**采样负载挂载点**（躯干、手臂外伸处），注入**物理一致的虚拟力与力矩**，让下肢在没有力传感器的情况下学会**隐式阻抗**去匹配、吸收负载引起的扰动。

### 4. 端到端 RL 与部署
- **非对称 actor-critic + PPO**：actor 只吃**深度图**；critic 在训练期额外拿到**特权观测**（高程图、规划器目标）；
- **单次训练**，无师生蒸馏；
- 靠**域随机化零样本 sim-to-real**，在真机上直接跑。

### 5. 关键结果
- **行走**：台阶阶高至 0.20 m 时可达 **1.0 m/s**；标准地形成功率 **70%**（比「仅自适应步态」基线高 17 个百分点），高难地形（0.22–0.28 m，OOD）约 30%；
- **负载**：约 **15 kg** 中心负载仍稳；+15 kg 骨盆负载成功率 **50%**（基线 38%）且功耗低 27 W；+10 kg 腕部（力矩主导）负载成功率 **65%**（基线 50%）；
- **效率**：高难地形上速度跟踪误差与机械功率均优于「仅地形代价」变体（0.22 vs 0.23 m/s；229 vs 241 W）。

---

### 🧭 整体流程（mermaid）

<div class="mermaid">
flowchart TD
    DEPTH["📷 深度图观测<br/>(actor 输入)"] --> POLICY
    HMAP["🗺️ 高程图 / 规划器目标<br/>(critic 特权观测·仅训练)"] -.-> CRITIC

    subgraph TERRAIN["🌄 多通道地形可供性"]
      Q["平整 Q"] --> COST
      E["陡峭 E"] --> COST
      M["速度感知高度可行性 M"] --> COST
      B["前进爬升 b"] --> COST["🧮 融合地形代价"]
    end

    COST --> DCM["⚙️ GPU 并行 DCM<br/>落脚规划器 → 目标落点"]
    COST --> REW["🎯 密集可供性奖励"]

    DCM --> SWING["🦿 二次贝塞尔摆动<br/>+ 切线导向落脚朝向"]
    WRENCH["🏋️ 虚拟力矩注入<br/>(采样负载点·物理一致)"] --> POLICY["🧠 非对称 PPO 策略"]
    SWING --> POLICY
    REW --> POLICY
    CRITIC["📈 特权 critic"] --> POLICY

    POLICY --> DR["🎲 域随机化"]
    DR --> REAL["🤖 零样本上真机<br/>台阶 1.0 m/s · ~15 kg 负载 · 无力传感器"]

    style TERRAIN fill:#e8f4fd,stroke:#1f78b4,color:#0b3954
    style COST fill:#e8f4fd,stroke:#1f78b4,color:#0b3954
    style WRENCH fill:#f7e8fd,stroke:#9b59b6,color:#4a1c5d
    style POLICY fill:#fff4e6,stroke:#e67e22,color:#7d3c08
    style REAL fill:#fde8e8,stroke:#c0392b,color:#641e16
</div>

---

## 💡 核心贡献

1. **多通道地形可供性**：平整/陡峭/速度可行性/爬升四代价，联动 DCM 规划与 RL 奖励；贝塞尔摆动 + 切线导向朝向，超越「仅落脚位置」的跟踪；
2. **负载感知柔顺**：虚拟力矩注入训练出下肢隐式阻抗，**无需力传感器**即可扛住至 ~15 kg 中心负载与力矩主导的腕部负载，无需重训；
3. **端到端一体化**：单次 PPO（无师生蒸馏）、域随机化零样本 sim-to-real，在结构化地形背负载真机演示。

---

## 🤖 对人形机器人学习的启发

- **「规划 + 奖励」共用一套地形代价**是省事又协同的设计：同一份可供性既产生落脚目标、又塑形密集奖励，避免规划器与策略「各说各话」；
- **控制落脚朝向、而非仅位置**，是跨越台阶竖板这类接触敏感场景里被低估的一环；
- **虚拟力矩注入**把「负载鲁棒」变成训练时的分布覆盖问题，用隐式阻抗替代力传感器闭环，工程上省成本、抗噪声，可迁移到搬运/协作类任务；
- **端到端单次训练 + 域随机化**再次印证：在明确的感知/奖励结构下，不一定要师生蒸馏也能拿到可部署策略。

---

## 📁 资源对照

| 资源 | 内容 |
|---|---|
| [arXiv 2606.20645](https://arxiv.org/abs/2606.20645) | 论文正文（方法、消融与数值结果） |
| [PDF](https://arxiv.org/pdf/2606.20645) · [HTML](https://arxiv.org/html/2606.20645) | 在线阅读 |
| [项目页](https://fai-rl-tech.github.io/tact-locomotion.github.io/) | 视频演示 / 代码入口 |

> ℹ️ 备注：本环境网络出口对 arXiv 有限制，本笔记依据可获取的 Abstract 与 HTML 正文整理，方法机制与实验数值均取自官方描述；若后续项目页补充代码可再补链接。

---

## 🔗 相关阅读

- **感知行走 · 同模块**：[RPL：挑战地形上的鲁棒感知行走](../RPL__Learning_Robust_Humanoid_Perceptive_Locomotion_on_Challenging_Terrains/RPL__Learning_Robust_Humanoid_Perceptive_Locomotion_on_Challenging_Terrains.md) · [CMR：非结构地形收缩映射嵌入](../CMR__Contractive_Mapping_Embeddings_for_Robust_Humanoid_Locomotion/CMR__Contractive_Mapping_Embeddings_for_Robust_Humanoid_Locomotion.md)；
- **台阶 / 落脚**：[FastStair：学习跑上楼梯](../FastStair__Learning_to_Run_Up_Stairs_with_Humanoid_Robots/FastStair__Learning_to_Run_Up_Stairs_with_Humanoid_Robots.md) · [Walk the PLANC：受限落脚点的敏捷行走](../Walk_the_PLANC__Physics-Guided_RL_for_Agile_Humanoid_Locomotion_on_Constrained_Footholds/Walk_the_PLANC__Physics-Guided_RL_for_Agile_Humanoid_Locomotion_on_Constrained_Footholds.md)；
- **像素端到端**：[Now You See That：从原始像素学人形行走](../Now_You_See_That_Learning_End-to-End_Humanoid_Locomotion_from_Raw_Pixels/Now_You_See_That_Learning_End-to-End_Humanoid_Locomotion_from_Raw_Pixels.md)。
