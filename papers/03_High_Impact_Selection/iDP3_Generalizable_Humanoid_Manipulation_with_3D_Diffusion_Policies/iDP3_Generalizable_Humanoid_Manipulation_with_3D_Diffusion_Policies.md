---
layout: paper
title: "iDP3: Generalizable Humanoid Manipulation with Improved 3D Diffusion Policies"
category: "高影响力精选 High Impact Selection"
subcategory: "Teleoperation & Imitation Learning"
zhname: "iDP3：基于改进版 3D 扩散策略的可泛化人形操作"
---

# iDP3: Generalizable Humanoid Manipulation with Improved 3D Diffusion Policies
**iDP3：基于改进版 3D 扩散策略的可泛化人形操作**

> 📅 阅读日期: 2026-05-18  
> 🏷️ 板块: 03_High_Impact_Selection / Teleoperation & Imitation Learning（H11）  
> 🧭 状态: 首版基础摘要（含 mermaid 流程图）；后续可结合 IROS 2025 版补充更多新场景实验细节。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2410.10803](https://arxiv.org/abs/2410.10803) |
| **HTML** | [arxiv.org/html/2410.10803v3](https://arxiv.org/html/2410.10803v3) |
| **PDF** | [arxiv.org/pdf/2410.10803](https://arxiv.org/pdf/2410.10803) |
| **项目主页** | [humanoid-manipulation.github.io](https://humanoid-manipulation.github.io/) |
| **源码（策略）** | [YanjieZe/Improved-3D-Diffusion-Policy](https://github.com/YanjieZe/Improved-3D-Diffusion-Policy) |
| **源码（遥操作）** | [YanjieZe/humanoid_teleoperation](https://github.com/YanjieZe/humanoid_teleoperation) |
| **作者** | Yanjie Ze, Zixuan Chen, Wenhao Wang, Tianyi Chen, Xialin He, Ying Yuan, Xue Bin Peng, Jiajun Wu |
| **机构** | Stanford / SFU / UPenn / UIUC / CMU |
| **会议** | IROS 2025 |
| **机器人** | Fourier GR-1（25-DoF 上半身 + 可升降推车 + 头戴 L515 LiDAR） |
| **训练规模** | 单一场景采集，>2000 次真机评估 trial |

---

## 🎯 一句话总结

iDP3 把 DP3 从「世界坐标系 + 标定 + 分割」搬到了「相机自帧 + 大点云 + 卷积金字塔编码器 + 长预测视界」，配上 Apple Vision Pro 25-DoF 全上半身遥操作 + Fourier GR-1 + 升降推车的硬件方案，让人形机器人只用**一个场景**的人工示范数据，就能在厨房、会议室、办公室等**未见场景**里零样本完成 Pick & Place / Pour / Wipe 等技能。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| **iDP3** | Improved 3D Diffusion Policy | 本文方法，DP3 的人形 / 移动机器人改造版 |
| **DP3** | 3D Diffusion Policy | Ze 等 2024 的原始 3D 扩散策略（依赖标定+分割） |
| **DP** | Diffusion Policy | Chi 等的 2D 扩散策略基线 |
| **DoF** | Degrees of Freedom | 自由度，iDP3 启用了 25 DoF 上半身 |
| **AVP** | Apple Vision Pro | 数据采集所用的头显，提供头/手/腕 6-DoF |
| **IK** | Inverse Kinematics | 逆运动学；用 Relaxed IK 跟手腕 |
| **LiDAR** | Light Detection And Ranging | 用 RealSense L515 固态 LiDAR 取深度点云 |
| **FPS** | Farthest Point Sampling | DP3 原版点云采样；iDP3 改 voxel + uniform |
| **DDIM** | Denoising Diffusion Implicit Models | 扩散策略推理用的少步采样器 |

---

## ❓ 论文要解决什么问题？

当前人形操作系统普遍局限在**单一训练场景**：

1. 大多数遥操作系统（OpenTeleVision / HumanPlus / OmniH2O / DexCap / ACE …）只演示了原场景的 picking / pouring，**离开训练桌一换场景就崩**；
2. DP3 本身依赖**精准相机外参 + 点云前景分割**，相机一旦换装（如挂在人形头上随头转）就失效；
3. 收集人形多场景示范数据**极其昂贵**——人形又重、又脆、又需要操作员训练。

iDP3 的目标就是：**只用 1 个场景的人形示范数据**，在未见场景里 zero-shot 完成日常操作。其核心信念是「点云本身就有强 view / scene 不变性，只要别把它强制对齐到世界系」。

---

## 🔧 方法详解

### 1. 硬件平台（25-DoF 上半身 + 升降推车 + 头戴 LiDAR）

- **机器人**：Fourier GR-1，启用 head + waist + arms + Inspire 灵巧手 = 25 DoF，**主动放弃下肢**（用推车解决移动 / 高度）；
- **升降推车**：把桌面差异（不同房间的桌子高度）从「需要 WBC 蹲下」简化为「转动升降柱」，作者明言这是过渡方案；
- **头戴 RealSense L515 固态 LiDAR**：作者多次尝试 D435 / Livox Mid-360 都不行——D435 深度噪声大、Mid-360 帧率不足；L515 是当前能跑 contact-rich 操作的甜点。

### 2. 数据采集：AVP 驱动的全上半身遥操作

- **AVP** 取人体头/手/腕 6-DoF；
- **手臂**：Relaxed IK 跟手腕位姿；
- **腰 + 头**：直接用人头朝向驱动（首次把腰部纳入遥操，工作空间显著扩展）；
- **vision feedback**：把 L515 实时画面 stream 回 AVP，实现沉浸式遥操；
- **延迟**：因 LiDAR 占带宽 / CPU，约 0.5 s；
- **动作空间**：直接用关节目标位（试过末端位姿，发现噪声更大）。

### 3. iDP3 = DP3 的四件套改造

| # | 改动 | 动机 |
|---|------|------|
| **A** | **Egocentric 3D 表征**（相机坐标系） | 摆脱标定 + 分割，让头戴 LiDAR 即插即用 |
| **B** | **放大点云输入**（1k → 4k） | 缺了分割后必须靠"看完全场景"补偿；ablation 表明 4k 最甜点 |
| **C** | **卷积 + 金字塔编码器** | 替换 DP3 原 MLP；卷积让输出更平滑、金字塔特征提精度 |
| **D** | **更长预测视界**（4 → 16） | 人体示范本身抖动 + 传感噪声大，短视界根本学不出来 |

附加工程优化：FPS 换 **voxel + uniform** 采样（更快且覆盖均匀）；50 步训练 / 10 步 DDIM 推理；onboard CPU 15 Hz 实时部署。

### 4. 与 DP3 / DP 的核心区别

```text
DP3:  world-frame 点云  + 物体分割 + 1024 点 + MLP + 4-step horizon
DP :  RGB(+R3M) + ResNet/MLP（强基线但靠 finetune，泛化差）
iDP3: camera-frame 点云 + 不分割 + 4096 点 + Conv+Pyramid + 16-step horizon
```

---

## 🧭 整体流程（mermaid）

<div class="mermaid">
flowchart LR
    subgraph DATA["🧑‍💻 数据采集（单场景）"]
        D1["Apple Vision Pro<br/>头/手/腕 6-DoF"]
        D2["Relaxed IK<br/>映射臂关节"]
        D3["腰 + 头跟人头朝向<br/>(扩工作空间)"]
        D4["LiDAR 画面回传 AVP<br/>沉浸反馈"]
    end

    subgraph ROBOT["🤖 GR-1 + 推车 + L515"]
        R1["25-DoF 上半身<br/>head/waist/arms/hands"]
        R2["可升降推车<br/>(替代下肢 WBC)"]
        R3["头戴 RealSense L515<br/>egocentric 点云"]
    end

    subgraph IDP3["🧠 iDP3 学习"]
        I1["A. Camera-frame 表征<br/>免标定 / 免分割"]
        I2["B. 4096 点大点云<br/>覆盖全场景"]
        I3["C. Conv + Pyramid 编码器<br/>平滑 + 多尺度"]
        I4["D. 16 步预测视界<br/>抗人手抖动"]
        I1 --> I5["Diffusion Policy 主干<br/>DDIM 10 步推理"]
        I2 --> I5
        I3 --> I5
        I4 --> I5
    end

    subgraph DEPLOY["🌍 未见场景 zero-shot"]
        E1["厨房 / 会议室 / 办公室"]
        E2["Pick & Place"]
        E3["Pour"]
        E4["Wipe"]
        E1 --- E2
        E1 --- E3
        E1 --- E4
    end

    DATA --> ROBOT
    ROBOT --> IDP3
    IDP3 -->|15 Hz onboard CPU| DEPLOY

    style DATA fill:#e8f4fd,stroke:#1f78b4,color:#0b3d5c
    style ROBOT fill:#e8f8e8,stroke:#27ae60,color:#0b3d1a
    style IDP3 fill:#fdebd0,stroke:#e67e22,color:#7a3e00
    style DEPLOY fill:#fce4ec,stroke:#c2185b,color:#5c0b2b
</div>

---

## 📊 实验亮点（节选）

- **>2000 次** 真机 trial 评估，避免 humanoid 论文常见的「3 次试验定胜负」。
- **核心对比**（Pick & Place，每方法 ~130 trial）：
  - 原版 **DP3 失败率 100%**（直接学不出来）；
  - **DP + finetune R3M** 训练场景下抓取最准（99/147），但**换场景 / 换物体即崩**；
  - **iDP3 训练场景** 75/139，略低于 DP+R3M，但**新物体 / 新视角 / 新场景全部 9/10**（DP 同设置常 1–3/10）。
- **消融**：
  - 编码器：Linear → Conv+Pyramid 显著提升平滑度与准确率；
  - 点数：1024 → 4096 提升明显，8192 收益饱和；
  - 预测视界：4 步全 0%，16 步是甜点，32 步反而下降。
- **效率**：iDP3 训练 wall-time **比 DP 还短**（即便点云大了 4×），onboard CPU 实时 15 Hz。

---

## 🤖 对人形机器人领域的意义

| 方向 | 含义 |
|------|------|
| **3D 视觉运动策略** | 把"3D 必依赖标定 + 分割"这条思维定势打破，让 DP3 系真正能上人形 / 移动平台 |
| **数据效率** | 用 **1 个场景** 的数据做到了 RUM、ManiWhere 用 20+ 场景才能做的泛化 |
| **遥操作** | 首个把 **waist** 纳入 AVP 遥操闭环的工作，工作空间显著扩展 |
| **硬件取舍** | 用"升降推车"过渡式替代下肢 WBC，是一种工程上诚实可复现的方案 |
| **泛化叙事** | 把"3D representation 自带 view / scene invariance"从 simulation claim 推到了真实人形场景 |

---

## 🎤 面试参考

**Q：iDP3 相比原版 DP3 最关键的改动是什么？**  
A：四件套改造（相机自帧表征 / 4096 点放大 / 卷积金字塔编码器 / 16 步预测视界），但要选一个最本质的，是**抛弃世界坐标 + 抛弃分割**——这一步让 3D 策略首次能装到头戴 LiDAR + 移动平台上，是泛化能力的根因。点数 / 编码器 / 视界都是把"丢掉分割"造成的精度损失补回来的工程手段。

**Q：为什么不用 RGB + R3M？DP + finetune R3M 在训练场景里也很强。**  
A：训练场景内 DP+R3M 是最强基线（99/147 > iDP3 75/139），但作者展示了**换物体 / 换视角 / 换场景**它会从 ~90% 掉到 10–30%。3D 点云天然不携带颜色 / 光照纹理偏置，因此 iDP3 在分布外几乎是平的 9/10。这是「在 distribution 内拼绝对精度 vs. 在 distribution 外保泛化」的经典权衡。

**Q：为什么 16 步预测视界是必要的？**  
A：人通过 AVP 遥操产生的轨迹**本身抖动大**（手抖 + IK 解算抖动 + LiDAR 数据 0.5 s 延迟）。短视界（4 步）相当于让策略每一小段都去拟合抖动，根本学不到平滑的动作流形；16 步让策略学习一个相对长的「动作片段先验」，类似 Diffusion Policy 原论文里的 action chunking，自然平均掉高频噪声。

**Q：和 HumanPlus / OmniH2O 路线最大差异？**  
A：HumanPlus / OmniH2O 关心的是 **whole-body RL + retargeting + sim-to-real**，目标是让人形会"走 + 全身姿态跟随"，但操作泛化仍局限训练场景。iDP3 完全反过来——**砍掉下肢、聚焦上半身 IL + 3D 视觉**，靠点云表征解决了"操作技能的场景泛化"。两条路线某种意义上是互补的：上半身 iDP3 + 下半身 HOMIE / HugWBC 是合理的组合。

**Q：为什么必须 L515 不行换 D435？**  
A：DP3 / iDP3 对 3D 点云的几何细节敏感。D435 是结构光，远距离深度噪声大、孔洞多，会让 4096 点里大半是无效噪声；L515 固态 LiDAR 给得起 contact-rich 操作所需的几何质量。Livox Mid-360 帧率 / 分辨率又对不上实时操作。这是当前硬件下的甜点选择。

---

## 🔗 相关阅读

- [DP3 (2403.03954)](https://arxiv.org/abs/2403.03954)：原始 3D Diffusion Policy，iDP3 直接基线
- [Diffusion Policy (2303.04137)](https://arxiv.org/abs/2303.04137)：扩散策略 2D 起点
- [OpenTeleVision (2407.01512)](https://arxiv.org/abs/2407.01512)：AVP 视觉回传方案
- [HumanPlus (2406.10454)](https://arxiv.org/abs/2406.10454) / [OmniH2O (2406.08858)](https://arxiv.org/abs/2406.08858)：whole-body 遥操作路线对照
- [Robot Utility Model (2409.05865)](https://arxiv.org/abs/2409.05865)：另一条「跨场景泛化」路线（用 20+ 场景数据）
- [YanjieZe/Improved-3D-Diffusion-Policy](https://github.com/YanjieZe/Improved-3D-Diffusion-Policy)：策略训练 / 部署官方实现（IROS 2025 已收录）
- [YanjieZe/humanoid_teleoperation](https://github.com/YanjieZe/humanoid_teleoperation)：AVP 全上半身遥操作配套仓库

---

## 📎 附录：与该笔记并行的"高影响力精选"笔记

| 类别 | 已完成 | 待补 |
|------|------|------|
| 全身控制核心 | ExBody1 / ExBody2 / HOVER / HugWBC | SONIC / UH-1 |
| 遥操作与模仿学习 | OmniH2O / HOMIE / HumanPlus（07_Teleoperation）/ EgoMimic（06_Manipulation）/ **iDP3（本文）** | （本分类已全部覆盖） |
| 仿真平台与工具 | ProtoMotions3 / Isaac Lab / Humanoid-Gym / HumanoidBench / BEHAVIOR Robot Suite | （本分类已全部覆盖） |

> 截至本笔记，「遥操作与模仿学习」与「仿真平台与工具」两类高影响力精选论文均已落笔；后续轨 A 推进重点回到 **全身控制核心**（SONIC、UH-1）。
