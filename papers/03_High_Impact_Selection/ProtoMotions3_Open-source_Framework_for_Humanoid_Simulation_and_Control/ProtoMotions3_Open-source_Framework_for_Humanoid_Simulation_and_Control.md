---
layout: paper
paper_order: 24
title: "ProtoMotions3: An Open-source Framework for Humanoid Simulation and Control"
category: "高影响力精选"
subcategory: "Simulation Platform & Tools"
zhname: "ProtoMotions3：面向人形仿真与控制的开源框架"
---

# ProtoMotions3: An Open-source Framework for Humanoid Simulation and Control
**ProtoMotions3：面向人形仿真与控制的开源框架**

> 📅 阅读日期: 2026-04-24
> 🏷️ 板块: 仿真平台 / 运动模仿 / Sim-to-Real / NVIDIA

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **项目主页 / 文档** | [nvlabs.github.io/ProtoMotions](https://nvlabs.github.io/ProtoMotions/) |
| **代码** | [GitHub - NVlabs/ProtoMotions](https://github.com/NVlabs/ProtoMotions) |
| **引用标题** | ProtoMotions3: An Open-source Framework for Humanoid Simulation and Control |
| **作者** | Chen Tessler, Yifeng Jiang, Xue Bin Peng, Erwin Coumans, Yi Shi, Haotian Zhang, Davis Rempe, Gal Chechik, Sanja Fidler |
| **发布时间** | 2025 |
| **许可证** | Apache-2.0 |
| **相关论文** | [MaskedMimic](https://arxiv.org/abs/2409.14393), [AMP](https://arxiv.org/abs/2104.02180), [ASE](https://arxiv.org/abs/2205.01906), [DeepMimic](https://xbpeng.github.io/projects/DeepMimic/index.html) |

> 注：截至本笔记整理时，ProtoMotions3 更像一个带推荐引用的开源框架/技术栈发布，未找到独立 arXiv 论文页；官方 README 给出的引用类型是 GitHub repository。

---

## 🎯 一句话总结

> ProtoMotions3 是 NVIDIA 发布的 GPU 加速人形仿真与控制框架，把大规模运动学习、多后端仿真、motion retargeting、MaskedMimic/AMP/ASE/PPO 算法、Unitree G1/H1 等机器人形态和 sim-to-real 部署链路整合到一套开源工程中。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| GTP | General Tracking Policy | 覆盖大量动作数据的通用跟踪策略 |
| AMASS | Archive of Motion Capture as Surface Shapes | 常用大规模人体动作捕捉数据集 |
| SEED | BONES-SEED motion data | ProtoMotions 文档中用于 G1 部署链路的数据来源 |
| Sim2Sim | Simulation-to-Simulation | 同一策略在不同物理引擎间测试 |
| Sim2Real | Simulation-to-Real | 从仿真策略迁移到真实机器人 |
| ONNX | Open Neural Network Exchange | 模型部署交换格式 |

---

## ❓ ProtoMotions 要解决什么问题？

人形运动控制的难点已经不只是“训一个 PPO 走路”。

真实工程里会同时遇到：

1. **数据规模问题**：AMASS、BONES、PHUMA、Kimodo motion 等来源格式不同，重定向到不同 robot morphology 很麻烦。
2. **仿真后端问题**：IsaacGym、IsaacLab、Newton、Genesis、MuJoCo 各有速度、稳定性和部署验证优势。
3. **算法复用问题**：AMP、ASE、MaskedMimic、PPO 都需要环境、motion dataset、reward、模型和训练脚本配合。
4. **机器人落地问题**：从训练环境导出到 Unitree G1 这类真实机器人时，observation 计算、模型格式、部署接口都容易错位。

ProtoMotions 的定位是把这些部分串成一个更完整的人形控制研发栈。

---

## 🔧 方法详解

### 1. 多后端仿真抽象

官方文档列出的后端包括：

| 后端 | 作用 |
|------|------|
| NVIDIA Newton | 面向 GPU 加速物理仿真的新后端 |
| IsaacGym | 经典 GPU 并行 RL 训练后端 |
| IsaacLab | NVIDIA 机器人学习平台 |
| Genesis | GPU 仿真后端 |
| MuJoCo | CPU 后端，常用于可解释测试和交叉验证 |

这种设计的工程价值是 Sim2Sim：同一个策略可以从 IsaacGym 切到 Newton 或 MuJoCo，检查它是否只是在某个物理引擎里“过拟合”。

### 2. 统一 motion learning 管线

ProtoMotions 重点支持大规模 motion learning：

- 用 AMASS 的公开人体动作数据训练物理仿真人形。
- 用 PyRoki 做全量 motion retargeting，把 SMPL/SMPL-X 或其他骨架动作转到目标机器人。
- 支持 SMPL、SMPL-X、Unitree G1、H1 和自定义 morphology。
- 文档中强调可在多 GPU 上把大动作库分片训练。

这里的核心不是单个 reward，而是数据、重定向、仿真、训练和评估的端到端吞吐。

### 3. 内置算法族

官方文档列出的实现包括：

| 算法 | 作用 |
|------|------|
| PPO | 通用强化学习优化器 |
| AMP | 通过 motion prior 学自然动作 |
| ASE | 学习可复用技能 latent |
| MaskedMimic | 将多模态控制统一成 masked motion inpainting |

这说明 ProtoMotions 更接近一个“研究栈”：既能跑经典 imitation baseline，也能承接 NVIDIA 自己的 MaskedMimic 路线。

### 4. 从仿真到真实机器人

官方 README 强调了 Unitree G1 部署链路：

- 训练一个覆盖 BONES-SEED 大规模动作的 General Tracking Policy。
- 导出单个 ONNX 模型。
- 将 observation computation 一并封装，部署侧只需要提供原始传感器信号。
- 在 RoboJuDo 框架上进行 G1 实机测试。

这点很关键：很多论文只给训练代码，但真实部署时 observation 对齐会变成主要风险。ProtoMotions 把这部分纳入框架目标。

---

## 🚶 具体实例

一个典型 ProtoMotions 工作流可以这样理解：

1. 从 AMASS 或 SEED 准备动作数据。
2. 用 PyRoki 将人体动作重定向到 Unitree G1。
3. 在 IsaacGym 或 Newton 后端训练 G1 motion tracking policy。
4. 用 MuJoCo 或另一个后端做 Sim2Sim 检查。
5. 将策略导出为 ONNX。
6. 通过 G1 deployment tutorial 接入真实机器人控制栈。

如果使用 Kimodo 生成文本动作，则可以先把 text-to-motion 结果转换到 ProtoMotions 格式，再训练一个物理可执行策略。这把“运动生成模型”和“物理控制器”接了起来。

---

## 🤖 工程价值

- **比单篇论文更像平台**：它把 motion retargeting、仿真后端、训练算法、部署导出放在同一 repo。
- **适合复现实验链路**：从 AMASS/SEED 到 G1 的流程有文档和 tutorial。
- **适合做算法基线**：AMP、ASE、MaskedMimic、PPO 都在同一框架中，有利于横向比较。
- **对 sim-to-real 有直接意义**：ONNX 导出和 G1 部署说明降低了从 paper policy 到 real robot 的工程断层。

---

## 📁 源码与论文对照

| 方向 | 链接 | 对应意义 |
|------|------|----------|
| ProtoMotions 主仓库 | [NVlabs/ProtoMotions](https://github.com/NVlabs/ProtoMotions) | 框架主体、训练脚本、文档、部署入口 |
| ProtoMotions 文档 | [Documentation](https://nvlabs.github.io/ProtoMotions/) | 安装、数据准备、训练、G1 部署 |
| MaskedMimic | [arXiv:2409.14393](https://arxiv.org/abs/2409.14393) / [Project](https://research.nvidia.com/labs/par/maskedmimic/) | ProtoMotions 中最重要的统一控制算法之一 |
| MimicKit | [xbpeng/MimicKit](https://github.com/xbpeng/MimicKit) | sibling repository，偏轻量 motion imitation 方法套件 |
| PyRoki | [arXiv:2505.03728](https://arxiv.org/abs/2505.03728) | ProtoMotions v3 motion retargeting 的关键工具 |

---

## 🎤 面试高频问题 & 参考回答

1. **ProtoMotions 和 MimicKit 的区别？**
   - MimicKit 更轻量，聚焦 motion imitation 算法实现；ProtoMotions 更大，覆盖仿真后端、数据处理、retargeting、算法、部署和真实机器人链路。

2. **为什么 ProtoMotions 要支持多个物理后端？**
   - 单后端训练可能过拟合引擎细节。Sim2Sim 可以检查策略是否对不同动力学实现保持稳定，是 sim-to-real 前的重要压力测试。

3. **MaskedMimic 在 ProtoMotions 中为什么重要？**
   - MaskedMimic 把全身追踪、局部目标、路径、文本、物体交互等控制形式统一成 masked motion inpainting，是通用人形控制方向的重要算法。

4. **ProtoMotions 对真实机器人部署最值得关注的点是什么？**
   - ONNX 导出时把 observation computation 一并处理，减少训练侧和部署侧观测定义不一致的问题。

---

## 📎 附录

### A. 与路线图其他论文的关联

| 论文 / 框架 | 关系 |
|-------------|------|
| DeepMimic | motion tracking 的基础范式 |
| AMP | ProtoMotions 支持的对抗运动先验 |
| ASE | ProtoMotions 支持的技能 latent 学习 |
| MaskedMimic | ProtoMotions 的核心统一控制算法之一 |
| Retargeting Matters | 与 ProtoMotions/GMR/PHC 等 tracking baseline 有直接比较关系 |
| MimicKit | 同作者/同谱系的轻量 sibling framework |

### B. 参考来源

- [ProtoMotions Documentation](https://nvlabs.github.io/ProtoMotions/)
- [NVlabs/ProtoMotions GitHub](https://github.com/NVlabs/ProtoMotions)
- [MaskedMimic arXiv](https://arxiv.org/abs/2409.14393)
- [MaskedMimic Project](https://research.nvidia.com/labs/par/maskedmimic/)
