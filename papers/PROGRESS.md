## 进度

### 基础路线图（当前）

| #   | 论文 | 状态 | 日期 | 路线 |
| --- | ---- | ---- | ---- | ---- |
| 1   | PPO: Proximal Policy Optimization | ✅ 完成 | 2026-03-22 | 基础RL |
| 2   | AWR: Advantage Weighted Regression | ✅ 完成 | 2026-03-22 | 基础RL |
| 3   | AMP: Adversarial Motion Priors for Stylized Physics-Based Character Control | ⏳ 待读 | - | 风格学习 |
| 4   | DeepMimic: Example-Guided Deep RL of Physics-Based Character Skills | 📖 进行中 | - | 精确模仿 |
| 5   | PHC: Perpetual Humanoid Control for Real-time Simulated Avatars | ⏳ 待读 | - | 精确模仿 |
| 6   | ADD: Adversarial Disentanglement and Distillation | ⏳ 待读 | - | 风格学习 |
| 7   | ASE: Adversarial Skill Embeddings for Large-Scale Motion Control | ⏳ 待读 | - | 技能组合 |
| 8   | CALM: Conditional Adversarial Latent Models for Directable Virtual Characters | ⏳ 待读 | - | 技能组合 |
| 9   | PULSE: Physically Plausible Universal Latent Skill Extraction | ⏳ 待读 | - | 技能组合 |
| 10  | Diffusion Policy: Visuomotor Policy Learning via Action Diffusion | ⏳ 待读 | - | 扩散+控制 |
| 11  | BeyondMimic: From Motion Tracking to Versatile Humanoid Control via Guided Diffusion | ⏳ 待读 | - | 扩散+控制 |
| 12  | Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World | ⏳ 待读 | - | Sim-to-Real |
| 13  | LCP: Sim-to-Real Action Smoothing | ⏳ 待读 | - | Sim-to-Real |

### ⭐ 高影响力精选（基础路线图之后优先读）

> 从 445 篇新论文中筛选出的高影响力工作。选择标准：🌟开源、经典/奠基性、与 RL/模仿学习运动控制高度相关、知名实验室代表作。

#### Whole-Body Control 核心

| #   | 论文 | 来源 | 理由 |
| --- | ---- | ---- | ---- |
| H1  | [Expressive Whole-Body Control for Humanoid Robots](https://arxiv.org/abs/2402.16796) 🌟 | WBC | 开源，表达性全身控制的基础工作 |
| H2  | [HOVER: Versatile Neural Whole-Body Controller for Humanoid Robots](https://arxiv.org/abs/2410.21229) | WBC | 通用神经 WBC，影响力极大 |
| H3  | [ExBody2: Advanced Expressive Humanoid Whole-Body Control](https://arxiv.org/abs/2412.13196) | WBC | ExBody 系列进化，实机验证 |
| H4  | [HugWBC: A Unified and General Humanoid Whole-Body Controller](https://arxiv.org/abs/2502.03206) | WBC | 统一框架，工程参考价值高 |
| H5  | [SONIC: Supersizing Motion Tracking for Natural Humanoid Whole-Body Control](https://arxiv.org/abs/2511.07820) | WBC | NVIDIA，大规模 motion tracking |
| H6  | [Learning from Massive Human Videos for Universal Humanoid Pose Control](https://arxiv.org/abs/2412.14172) | WBC | UH-1，海量人类视频学习 |

#### 遥操作与模仿学习

| #   | 论文 | 来源 | 理由 |
| --- | ---- | ---- | ---- |
| H7  | [HumanPlus: Humanoid Shadowing and Imitation from Humans](https://arxiv.org/abs/2406.10454) 🌟 | Teleop | Stanford，人形遥操作开山之作 |
| H8  | [OmniH2O: Universal and Dexterous Human-to-Humanoid Whole-Body Teleoperation](https://arxiv.org/abs/2406.08858) 🌟 | Teleop | LeCAR-Lab，通用 H2H 遥操作 |
| H9  | [HOMIE: Humanoid Loco-Manipulation with Isomorphic Exoskeleton Cockpit](https://arxiv.org/abs/2502.13013) 🌟 | Teleop | OpenRobotLab，外骨骼遥操作 |
| H10 | [EgoMimic: Scaling Imitation Learning via Egocentric Video](https://arxiv.org/abs/2410.24221) 🌟 | Manip | 自我中心视角模仿学习 |
| H11 | [Generalizable Humanoid Manipulation with Improved 3D Diffusion Policies](https://arxiv.org/abs/2410.10803) 🌟 | Manip | 泽洋杰，3D 扩散策略 |

#### Locomotion 经典

| #   | 论文 | 来源 | 理由 |
| --- | ---- | ---- | ---- |
| H12 | [Real-World Humanoid Locomotion with Reinforcement Learning](https://arxiv.org/abs/2303.03381) | Loco | Berkeley，首个真实世界人形 RL 行走 |
| H13 | [Humanoid Locomotion as Next Token Prediction](https://arxiv.org/abs/2402.19469) | Loco | 把运动控制建模为 token 预测，新范式 |
| H14 | [Humanoid Parkour Learning](https://arxiv.org/abs/2406.10759) | Loco | 人形跑酷，高动态控制 |
| H15 | [Learning Sim-to-Real Humanoid Locomotion in 15 Minutes](https://arxiv.org/abs/2512.01996) | Loco | 极快 sim-to-real，工程价值高 |
| H16 | [ECO: Energy-Constrained Optimization with RL for Humanoid Walking](https://arxiv.org/abs/2602.06445) 🌟 | Loco | 能量优化行走，开源 |

#### Sim-to-Real & Foundation Model

| #   | 论文 | 来源 | 理由 |
| --- | ---- | ---- | ---- |
| H17 | [Learning Agile and Dynamic Motor Skills for Legged Robots](https://arxiv.org/abs/1901.08652) | S2R | ANYmal 经典，sim-to-real RL 奠基 |
| H18 | [ASAP: Aligning Simulation and Real-World Physics for Agile Humanoid Skills](https://agile.human2humanoid.com/) | S2R | sim-real 物理对齐 |
| H19 | [GR00T N1: An Open Foundation Model for Generalist Humanoid Robots](https://arxiv.org/abs/2503.14734) | Manip | NVIDIA，人形机器人基础模型 |
| H20 | [Behavior Foundation Model for Humanoid Robots](https://arxiv.org/abs/2509.13780) | WBC | 行为基础模型 |

#### 仿真平台 & 工具

| #   | 论文 | 来源 | 理由 |
| --- | ---- | ---- | ---- |
| H21 | [Humanoid-Gym: RL for Humanoid Robot with Zero-Shot Sim2Real Transfer](https://arxiv.org/abs/2404.05695) | Sim | 人形机器人 RL 训练平台 |
| H22 | [HumanoidBench: Simulated Humanoid Benchmark for Whole-Body Locomotion and Manipulation](https://arxiv.org/abs/2403.10506) | Sim | 标准 benchmark |
| H23 | [BEHAVIOR Robot Suite: Real-World Whole-Body Manipulation for Everyday Tasks](https://arxiv.org/abs/2503.05652) 🌟 | Sim | 真实世界全身操作 benchmark |

### Loco-Manipulation and Whole-Body-Control

| #   | 论文 | 日期 | 🌟 | 状态 |
| --- | ---- | ---- | -- | ---- |
| 14  | LATENT: Learning Athletic Humanoid Tennis Skills from Imperfect Human Motion Data | 2026.03 |  | ⏳ 待读 |
| 15  | Ψ₀: An Open Foundation Model Towards Universal Humanoid Loco-Manipulation | - |  | ⏳ 待读 |
| 16  | SteadyTray: Learning Object Balancing Tasks in Humanoid Tray Transport via Residual RL | - |  | ⏳ 待读 |
| 17  | ZeroWBC: Learning Natural Visuomotor Humanoid Control from Egocentric Video | - |  | ⏳ 待读 |
| 18  | Embedding Classical Balance Control Principles in RL for Humanoid Recovery | - |  | ⏳ 待读 |
| 19  | ULTRA: Unified Multimodal Control for Autonomous Humanoid Whole-Body Loco-Manipulation | 2026-03-07 |  | ✅ 完成 |
| 20  | OmniXtreme: Breaking the Generality Barrier in High-Dynamic Humanoid Control | 2026-03-08 |  | ✅ 完成 |
| 21  | LessMimic: Long-Horizon Humanoid Interaction with Unified Distance Field Representations | - |  | ⏳ 待读 |
| 22  | Learning Humanoid End-Effector Control for Open-Vocabulary Visual Loco-Manipulation | - |  | ⏳ 待读 |
| 23  | VIGOR: Visual Goal-In-Context Inference for Unified Humanoid Fall Safety | - |  | ⏳ 待读 |
| 24  | [Perceptive Humanoid Parkour: Chaining Dynamic Human Skills via Motion Matching](https://arxiv.org/abs/2602.15827) | 2026.02 |  | ⏳ 待读 |
| 25  | [MeshMimic: Geometry-Aware Humanoid Motion Learning through 3D Scene Reconstruction](https://arxiv.org/abs/2602.15733) | 2026.02 |  | ⏳ 待读 |
| 26  | [General Humanoid Whole-Body Control via Pretraining and Fast Adaptation](https://arxiv.org/abs/2602.11929) | 2026.02 |  | ⏳ 待读 |
| 27  | [HAIC: Humanoid Agile Object Interaction Control via Dynamics-Aware World Model](https://arxiv.org/abs/2602.11758) | 2026.02 |  | ⏳ 待读 |
| 28  | [EgoHumanoid: Unlocking In-the-Wild Loco-Manipulation with Robot-Free Egocentric Demonstration](https://arxiv.org/abs/2602.10106) | 2026.02 |  | ⏳ 待读 |
| 29  | [MOSAIC: Bridging the Sim-to-Real Gap in Generalist Humanoid Motion Tracking and Teleoperation with Rapid Residual Adaptation](https://arxiv.org/abs/2602.08594) | 2026.02 |  | ⏳ 待读 |
| 30  | [Learning Human-Like Badminton Skills for Humanoid Robots](https://arxiv.org/abs/2602.08370) | 2026.02 |  | ⏳ 待读 |
| 31  | [TextOp: Real-time Interactive Text-Driven Humanoid Robot Motion Generation and Control](https://arxiv.org/abs/2602.07439) | 2026.02 |  | ⏳ 待读 |
| 32  | [Humanoid Manipulation Interface: Humanoid Whole-Body Manipulation from Robot-Free Demonstrations](https://arxiv.org/abs/2602.06643) | 2026.02 |  | ⏳ 待读 |
| 33  | [HiWET: Hierarchical World-Frame End-Effector Tracking for Long-Horizon Humanoid Loco-Manipulation](https://arxiv.org/abs/2602.06341) | 2026.02 |  | ⏳ 待读 |
| 34  | [Learning Soccer Skills for Humanoid Robots:   A Progressive Perception-Action Framework](https://arxiv.org/abs/2602.05310) | 2026.02 |  | ⏳ 待读 |
| 35  | [PDF-HR: Pose Distance Fields for Humanoid Robots](https://arxiv.org/abs/2602.04851) | 2026.02 |  | ⏳ 待读 |
| 36  | [HUSKY: Humanoid Skateboarding System via Physics-Aware Whole-Body Control](https://arxiv.org/abs/2602.03205) | 2026.02 |  | ⏳ 待读 |
| 37  | [Embodiment-Aware Generalist Specialist Distillation for Unified Humanoid Whole-Body Control](https://arxiv.org/abs/2602.02960) | 2026.02 |  | ⏳ 待读 |
| 38  | [HumanX: Toward Agile and Generalizable Humanoid Interaction Skills from Human Videos](https://arxiv.org/abs/2602.02473) | 2026.02 |  | ⏳ 待读 |
| 39  | [TTT-Parkour: Rapid Test-Time Training for Perceptive Robot Parkour](https://arxiv.org/abs/2602.02331) | 2026.02 |  | ⏳ 待读 |
| 40  | [ZEST: Zero-shot Embodied Skill Transfer for Athletic Robot Control](https://arxiv.org/abs/2602.00401) | 2026.02 |  | ⏳ 待读 |
| 41  | [Robust and Generalized Humanoid Motion Tracking](https://arxiv.org/abs/2601.23080) | 2026.01 |  | ⏳ 待读 |
| 42  | [RoboStriker: Hierarchical Decision-Making for Autonomous Humanoid Boxing](https://arxiv.org/abs/2601.22517) | 2026.01 |  | ⏳ 待读 |
| 43  | [PILOT: A Perceptive Integrated Low-level Controller for Loco-manipulation over Unstructured Scenes](https://arxiv.org/abs/2601.17440) | 2026.01 |  | ⏳ 待读 |
| 44  | [Collision-Free Humanoid Traversal in Cluttered Indoor Scenes](https://arxiv.org/abs/2601.16035) | 2026.01 |  | ⏳ 待读 |
| 45  | [FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions](https://arxiv.org/abs/2601.12799) | 2026.01 |  | ⏳ 待读 |
| 46  | [Learning Whole-Body Human-Humanoid Interaction from Human-Human Demonstrations](https://arxiv.org/abs/2601.09518) | 2026.01 |  | ⏳ 待读 |
| 47  | [Hiking in the Wild: A Scalable Perceptive Parkour Framework for Humanoids](https://arxiv.org/abs/2601.07718) | 2026.01 |  | ⏳ 待读 |
| 48  | [Deep Whole-body Parkour](https://arxiv.org/abs/2601.07701) | 2026.01 |  | ⏳ 待读 |
| 49  | [Coordinated Humanoid Manipulation with Choice Policies](https://arxiv.org/abs/2512.25072) | 2025.12 |  | ⏳ 待读 |
| 50  | [UniAct: Unified Motion Generation and Action Streaming for Humanoid Robots](https://arxiv.org/abs/2512.24321) | 2025.12 |  | ⏳ 待读 |
| 51  | [EGM: Efficiently Learning General Motion Tracking Policy for High Dynamic Humanoid Whole-Body Control](https://arxiv.org/abs/2512.19043) | 2025.12 |  | ⏳ 待读 |
| 52  | [Semantic Co-Speech Gesture Synthesis and Real-Time Control for Humanoid Robots](https://arxiv.org/abs/2512.17183) | 2025.12 |  | ⏳ 待读 |
| 53  | [CHIP: Adaptive Compliance for Humanoid Control through Hindsight Perturbation](https://arxiv.org/abs/2512.14689) | 2025.12 |  | ⏳ 待读 |
| 54  | [PvP: Data-Efficient Humanoid Robot Learning with Proprioceptive-Privileged Contrastive Representations](https://arxiv.org/abs/2512.13093) | 2025.12 |  | ⏳ 待读 |
| 55  | [Learning Agile Striker Skills for Humanoid Soccer Robots from Noisy Sensory Input](https://arxiv.org/abs/2512.06571) | 2025.12 |  | ⏳ 待读 |
| 56  | [Discovering Self-Protective Falling Policy for Humanoid Robot via Deep Reinforcement Learning](https://arxiv.org/abs/2512.01336) | 2025.12 |  | ⏳ 待读 |
| 57  | [Opening the Sim-to-Real Door for Humanoid Pixel-to-Action Policy Transfer](https://arxiv.org/abs/2512.01061) | 2025.12 |  | ⏳ 待读 |
| 58  | [Commanding Humanoid by Free-form Language: A Large Language Action Model with Unified Motion Vocabulary](https://arxiv.org/abs/2511.22963) | 2025.11 |  | ⏳ 待读 |
| 59  | [Kinematics-Aware Multi-Policy Reinforcement Learning for Force-Capable Humanoid Loco-Manipulation](https://arxiv.org/abs/2511.21169) | 2025.11 |  | ⏳ 待读 |
| 60  | [HAFO: A Force-Adaptive Control Framework for Humanoid Robots in Intense Interaction Environments](https://arxiv.org/abs/2511.20275) | 2025.11 |  | ⏳ 待读 |
| 61  | [SENTINEL: A Fully End-to-End Language-Action Model for Humanoid Whole Body Control](https://arxiv.org/abs/2511.19236) | 2025.11 |  | ⏳ 待读 |
| 62  | [SafeFall: Learning Protective Control for Humanoid Robots](https://arxiv.org/abs/2511.18509) | 2025.11 |  | ⏳ 待读 |
| 63  | [Agility Meets Stability: Versatile Humanoid Control with Heterogeneous Data](https://arxiv.org/abs/2511.17373) | 2025.11 |  | ⏳ 待读 |
| 64  | [VIRAL: Visual Sim-to-Real at Scale for Humanoid Loco-Manipulation](https://arxiv.org/abs/2511.15200) | 2025.11 |  | ⏳ 待读 |
| 65  | [HMC: Learning Heterogeneous Meta-Control for Contact-Rich Loco-Manipulation](https://arxiv.org/abs/2511.14756) | 2025.11 |  | ⏳ 待读 |
| 66  | [Humanoid Whole-Body Badminton via Multi-Stage Reinforcement Learning](https://arxiv.org/abs/2511.11218) | 2025.11 |  | ⏳ 待读 |
| 67  | [Robot Crash Course: Learning Soft and Stylized Falling](https://arxiv.org/abs/2511.10635) | 2025.11 |  | ⏳ 待读 |
| 68  | [Unveiling the Impact of Data and Model Scaling on High-Level Control for Humanoid Robots](https://arxiv.org/abs/2511.09241) | 2025.11 |  | ⏳ 待读 |
| 69  | [SONIC: Supersizing Motion Tracking for Natural Humanoid Whole-Body Control](https://arxiv.org/abs/2511.07820) | 2025.11 |  | ⏳ 待读 |
| 70  | [Unified Humanoid Fall-Safety Policy from a Few Demonstrations](https://arxiv.org/abs/2511.07407) | 2025.11 |  | ⏳ 待读 |
| 71  | [Towards Adaptive Humanoid Control via Multi-Behavior Distillation and Reinforced Fine-Tuning](https://arxiv.org/abs/2511.06371) | 2025.11 |  | ⏳ 待读 |
| 72  | [GentleHumanoid: Learning Upper-body Compliance for Contact-rich Human and Object Interaction](https://arxiv.org/abs/2511.04679) | 2025.11 |  | ⏳ 待读 |
| 73  | [BFM-Zero: A Promptable Behavioral Foundation Model for Humanoid Control Using Unsupervised Reinforcement Learning](https://arxiv.org/abs/2511.04131) | 2025.11 |  | ⏳ 待读 |
| 74  | [Learning Vision-Driven Reactive Soccer Skills for Humanoid Robots](https://arxiv.org/abs/2511.03996) | 2025.11 |  | ⏳ 待读 |
| 75  | [TWIST2: Scalable, Portable, and Holistic Humanoid Data Collection System](https://arxiv.org/abs/2511.02832) | 2025.11 |  | ⏳ 待读 |
| 76  | [Thor: Towards Human-Level Whole-Body Reactions for Intense Contact-Rich Environments](https://arxiv.org/abs/2510.26280) | 2025.10 |  | ⏳ 待读 |
| 77  | [One-shot Humanoid Whole-body Motion Learning](https://arxiv.org/abs/2510.25241) | 2025.10 |  | ⏳ 待读 |
| 78  | [Humanoid Goalkeeper: Learning from Position Conditioned Task-Motion Constraints](https://arxiv.org/abs/2510.18002) | 2025.10 |  | ⏳ 待读 |
| 79  | [From Language to Locomotion: Retargeting-free Humanoid Control via Motion Latent Guidance](https://arxiv.org/abs/2510.14952) | 2025.10 |  | ⏳ 待读 |
| 80  | [Towards Adaptable Humanoid Control via Adaptive Motion Tracking](https://arxiv.org/abs/2510.14454) | 2025.10 |  | ⏳ 待读 |
| 81  | [Learning Human-Humanoid Coordination for Collaborative Object Carrying](https://arxiv.org/abs/2510.14293) | 2025.10 |  | ⏳ 待读 |
| 82  | [Ego-Vision World Model for Humanoid Contact Planning](https://arxiv.org/abs/2510.11682) | 2025.10 |  | ⏳ 待读 |
| 83  | [DemoHLM: From One Demonstration to Generalizable Humanoid Loco-Manipulation](https://arxiv.org/abs/2510.11258) | 2025.10 |  | ⏳ 待读 |
| 84  | [PhysHSI: Towards a Real-World Generalizable and Natural Humanoid-Scene Interaction System](https://arxiv.org/abs/2510.11072) | 2025.10 |  | ⏳ 待读 |
| 85  | [It Takes Two: Learning Interactive Whole-Body Control Between Humanoid Robots](https://arxiv.org/abs/2510.10206) | 2025.10 |  | ⏳ 待读 |
| 86  | [ResMimic: From General Motion Tracking to Humanoid Whole-body Loco-Manipulation via Residual Learning](https://arxiv.org/abs/2510.05070) | 2025.10 |  | ⏳ 待读 |
| 87  | [HumanoidExo: Scalable Whole-Body Humanoid Manipulation via Wearable Exoskeleton](https://arxiv.org/abs/2510.03022) | 2025.10 |  | ⏳ 待读 |
| 88  | [Retargeting Matters: General Motion Retargeting for Humanoid Motion Tracking](https://arxiv.org/abs/2510.02252) | 2025.10 |  | ⏳ 待读 |
| 89  | [OmniRetarget: Interaction-Preserving Data Generation for Humanoid Whole-Body Loco-Manipulation and Scene Interaction](https://arxiv.org/abs/2509.26633) | 2025.09 |  | ⏳ 待读 |
| 90  | [Towards Versatile Humanoid Table Tennis: Unified Reinforcement Learning with Prediction Augmentation](https://arxiv.org/abs/2509.21690) | 2025.09 |  | ⏳ 待读 |
| 91  | [SEEC: Stable End-Effector Control with Model-Enhanced Residual Learning for Humanoid Loco-Manipulation](https://arxiv.org/abs/2509.21231) | 2025.09 |  | ⏳ 待读 |
| 92  | [VisualMimic: Visual Humanoid Loco-Manipulation via Motion Tracking and Generation](https://arxiv.org/abs/2509.20322) | 2025.10 |  | ⏳ 待读 |
| 93  | [HDMI: Learning Interactive Humanoid Whole-Body Control from Human Videos](https://arxiv.org/abs/2509.16757) | 2025.09 |  | ⏳ 待读 |
| 94  | [KungfuBot 2: Learning Versatile Motion Skills for Humanoid Whole-Body Control](https://arxiv.org/abs/2509.16638) | 2025.09 |  | ⏳ 待读 |
| 95  | [Implicit Kinodynamic Motion Retargeting for Human-to-humanoid Imitation Learning](https://arxiv.org/abs/2509.15443) | 2025.09 |  | ⏳ 待读 |
| 96  | [DreamControl: Human-Inspired Whole-Body Humanoid Control for Scene Interaction via Guided Diffusion](https://arxiv.org/abs/2509.14353) | 2025.09 |  | ⏳ 待读 |
| 97  | [Track Any Motions under Any Disturbances](https://arxiv.org/abs/2509.13833) | 2025.09 |  | ⏳ 待读 |
| 98   | [Behavior Foundation Model for Humanoid Robots](https://arxiv.org/abs/2509.13780) | 2025.09 |  | ⏳ 待读 |
| 99   | [Embracing Bulky Objects with Humanoid Robots: Whole-Body Manipulation with Reinforcement Learning](https://arxiv.org/abs/2509.13534) | 2025.09 |  | ⏳ 待读 |
| 100  | [StageACT: Stage-Conditioned Imitation for Robust Humanoid Door Opening](https://arxiv.org/abs/2509.13200) | 2025.09 |  | ⏳ 待读 |
| 101  | [TrajBooster: Boosting Humanoid Whole-Body Manipulation via Trajectory-Centric Learning](https://arxiv.org/abs/2509.11839) | 2025.09 |  | ⏳ 待读 |
| 102  | [HITTER: A HumanoId Table TEnnis Robot via Hierarchical Planning and Learning](https://arxiv.org/abs/2508.21043) | 2025.08 |  | ⏳ 待读 |
| 103  | [HuBE: Cross-Embodiment Human-like Behavior Execution for Humanoid Robots](https://arxiv.org/abs/2508.19002) | 2025.08 |  | ⏳ 待读 |
| 104  | [HumanoidVerse: A Versatile Humanoid for Vision-Language Guided Multi-Object Rearrangement](https://arxiv.org/abs/2508.16943) | 2025.08 |  | ⏳ 待读 |
| 105  | [Task and Motion Planning for Humanoid Loco-manipulation](https://arxiv.org/abs/2508.14099) | 2025.08 |  | ⏳ 待读 |
| 106  | [GBC: Generalized Behavior-Cloning Framework for Whole-Body Humanoid Imitation](https://arxiv.org/abs/2508.09960) | 2025.08 |  | ⏳ 待读 |
| 107  | [A Whole-Body Motion Imitation Framework from Human Data for Full-Size Humanoid Robot](https://arxiv.org/abs/2508.00362) | 2025.08 |  | ⏳ 待读 |
| 108  | [EMP: Executable Motion Prior for Humanoid Robot Standing Upper-body Motion Imitation](https://arxiv.org/abs/2507.15649) | 2025.07 |  | ⏳ 待读 |
| 109  | [Keep on Going: Learning Robust Humanoid Motion Skills via Selective Adversarial Training](https://arxiv.org/abs/2507.08303) | 2025.07 |  | ⏳ 待读 |
| 110  | [UniTracker: Learning Universal Whole-Body Motion Tracker for Humanoid Robots](https://arxiv.org/abs/2507.07356) | 2025.07 |  | ⏳ 待读 |
| 111  | [ULC: A Unified and Fine-Grained Controller for Humanoid Loco-Manipulation](https://arxiv.org/abs/2507.06905) | 2025.07 |  | ⏳ 待读 |
| 112  | [Learning Motion Skills with Adaptive Assistive Curriculum Force in Humanoid Robots](https://arxiv.org/abs/2506.23125) | 2025.06 |  | ⏳ 待读 |
| 113  | [A Survey of Behavior Foundation Model: Next-Generation Whole-Body Control System of Humanoid Robots](https://arxiv.org/abs/2506.20487) | 2025.06 |  | ⏳ 待读 |
| 114  | [TACT: Humanoid Whole-body Contact Manipulation through Deep Imitation Learning with Tactile Modality](https://arxiv.org/abs/2506.15146) | 2025.06 |  | ⏳ 待读 |
| 115  | [GMT: General Motion Tracking for Humanoid Whole-Body Control](https://arxiv.org/abs/2506.14770) | 2025.06 |  | ⏳ 待读 |
| 116  | [LeVERB: Humanoid Whole-Body Control with Latent Vision-Language Instruction](https://arxiv.org/abs/2506.13751) | 2025.06 |  | ⏳ 待读 |
| 117  | [From Experts to a Generalist: Toward General Whole-Body Control for Humanoid Robots](https://arxiv.org/abs/2506.12779) | 2025.06 |  | ⏳ 待读 |
| 118  | [SkillBlender: Towards Versatile Humanoid Whole-Body Loco-Manipulation via Skill Blending](https://arxiv.org/abs/2506.09366) | 2025.06 |  | ⏳ 待读 |
| 119  | [SLAC: Simulation-Pretrained Latent Action Space for Whole-Body Real-World Reinforcement Learning](https://arxiv.org/abs/2506.04147) | 2025.06 |  | ⏳ 待读 |
| 120  | [Hierarchical Intention-Aware Expressive Motion Generation for Humanoid Robots](https://arxiv.org/abs/2506.01563) | 2025.06 |  | ⏳ 待读 |
| 121  | [From Motion to Behavior: Hierarchical Modeling of Humanoid Generative Behavior Control](https://arxiv.org/abs/2506.00043) | 2025.06 |  | ⏳ 待读 |
| 122  | [SignBot: Learning Human-to-Humanoid Sign Language Interaction](https://arxiv.org/abs/2505.24266) | 2025.05 |  | ⏳ 待读 |
| 123  | [Learning Gentle Humanoid Locomotion and End-Effector Stabilization Control](https://arxiv.org/abs/2505.24198) | 2025.05 |  | ⏳ 待读 |
| 124  | [Mobi-π: Mobilizing Your Robot Learning Policy](https://arxiv.org/abs/2505.23692) | 2025.05 |  | ⏳ 待读 |
| 125  | [SMAP: Self-supervised Motion Adaptation for Physically Plausible Humanoid Whole-body Control](https://arxiv.org/abs/2505.19463) | 2025.05 |  | ⏳ 待读 |
| 126  | H2-COMPACT: Human-Humanoid Co-Manipulation via Adaptive Contact Trajectory Policies | 2025.05 |  | ⏳ 待读 |
| 127  | [Unleashing Humanoid Reaching Potential via Real-world-Ready Skill Space](https://arxiv.org/abs/2505.10918) | 2025.05 |  | ⏳ 待读 |
| 128  | [HuB: Learning Extreme Humanoid Balance](https://arxiv.org/abs/2505.07294) | 2025.05 |  | ⏳ 待读 |
| 129  | [FALCON: Learning Force-Adaptive Humanoid Loco-Manipulation](https://arxiv.org/abs/2505.06776) | 2025.05 |  | ⏳ 待读 |
| 130  | FAME: Force-Adaptive RL for Expanding the Manipulation Envelope of a Full-Scale Humanoid | - |  | ⏳ 待读 |
| 131  | [JAEGER: Dual-Level Humanoid Whole-Body Controller](https://arxiv.org/abs/2505.06584) | 2025.05 |  | ⏳ 待读 |
| 132  | [AMO: Adaptive Motion Optimization for Hyper-Dexterous Humanoid Whole-Body Control](https://arxiv.org/abs/2505.03738) | 2025.05 |  | ⏳ 待读 |
| 133  | [PyRoki: A Modular Toolkit for Robot Kinematic Optimization](https://arxiv.org/abs/2505.03728) | 2025.05 |  | ⏳ 待读 |
| 134  | [TWIST: Teleoperated Whole-Body Imitation System](https://arxiv.org/abs/2505.02833) | 2025.05 |  | ⏳ 待读 |
| 135  | [LangWBC: Language-directed Humanoid Whole-Body Control via End-to-end Learning](https://arxiv.org/abs/2504.21738) | 2025.04 |  | ⏳ 待读 |
| 136  | [Physically Consistent Humanoid Loco-Manipulation using Latent Diffusion Models](https://arxiv.org/abs/2504.16843v1) | 2025.04 |  | ⏳ 待读 |
| 137  | [Adversarial Locomotion and Motion Imitation for Humanoid Policy Learning](https://arxiv.org/abs/2504.14305) | 2025.04 |  | ⏳ 待读 |
| 138  | [Being-0: A Humanoid Robotic Agent with Vision-Language Models and Modular Skills](https://arxiv.org/abs/2503.12533) | 2025.03 |  | ⏳ 待读 |
| 139  | [Trinity: A Modular Humanoid Robot AI System](https://arxiv.org/abs/2503.08338) | 2025.03 |  | ⏳ 待读 |
| 140  | [BEHAVIOR Robot Suite: Streamlining Real-World Whole-Body Manipulation for Everyday Household Activities](https://arxiv.org/abs/2503.05652) | 2025.03 |  | ⏳ 待读 |
| 141  | [Whole-Body Model-Predictive Control of Legged Robots with MuJoCo](https://arxiv.org/abs/2503.04613) | 2025.03 |  | ⏳ 待读 |
| 142  | [HiFAR: Multi-Stage Curriculum Learning for High-Dynamics Humanoid Fall Recovery](https://arxiv.org/abs/2502.20061) | 2025.02 |  | ⏳ 待读 |
| 143  | [HOMIE: Humanoid Loco-Manipulation with Isomorphic Exoskeleton Cockpit](https://arxiv.org/abs/2502.13013) | 2025.02 |  | ⏳ 待读 |
| 144  | [Learning Getting-Up Policies for Real-World Humanoid Robots](https://arxiv.org/abs/2502.12152) | 2025.02 |  | ⏳ 待读 |
| 145  | [Learning Humanoid Standing-up Control across Diverse Postures](https://arxiv.org/abs/2502.08378) | 2025.02 |  | ⏳ 待读 |
| 146  | [HugWBC: A Unified and General Humanoid Whole-Body Controller](https://arxiv.org/abs/2502.03206) | 2025.02 |  | ⏳ 待读 |
| 147  | [SPARK: A Toolbox for Safe Humanoid Autonomy and Teleoperation](https://arxiv.org/abs/2502.03132) | 2025.02 |  | ⏳ 待读 |
| 148  | [Embrace Collisions: Humanoid Shadowing for Deployable Contact-Agnostics Motions](https://arxiv.org/abs/2502.01465) | 2025.02 |  | ⏳ 待读 |
| 149  | [Human-Humanoid Robots Cross-Embodiment Behavior-Skill Transfer Using Decomposed Adversarial Learning from Demonstration](https://arxiv.org/abs/2412.15166) | 2024.12 |  | ⏳ 待读 |
| 150  | [Learning from Massive Human Videos for Universal Humanoid Pose Control](https://arxiv.org/abs/2412.14172) | 2024.12 |  | ⏳ 待读 |
| 151  | [ExBody2: Advanced Expressive Humanoid Whole-Body Control](https://arxiv.org/abs/2412.13196) | 2024.12 |  | ⏳ 待读 |
| 152  | [Mobile-TeleVision: Predictive Motion Priors for Humanoid Whole-Body Control](https://arxiv.org/abs/2412.07773) | 2024.12 |  | ⏳ 待读 |
| 153  | [A Behavior Architecture for Fast Humanoid Robot Door Traversals](https://arxiv.org/abs/2411.03532) | 2024.11 |  | ⏳ 待读 |
| 154  | [EMOTION: Expressive Motion Sequence Generation for Humanoid Robots with In-Context Learning](https://arxiv.org/abs/2410.23234) | 2024.10 |  | ⏳ 待读 |
| 155  | [HOVER: Versatile Neural Whole-Body Controller for Humanoid Robots](https://arxiv.org/abs/2410.21229) | 2024.10 |  | ⏳ 待读 |
| 156  | [Harmon: Whole-Body Motion Generation of Humanoid Robots from Language Descriptions](https://arxiv.org/abs/2410.12773) | 2024.10 |  | ⏳ 待读 |
| 157  | [Whole-Body Dynamic Throwing with Legged Manipulators](https://arxiv.org/abs/2410.05681) | 2024.10 |  | ⏳ 待读 |
| 158  | [Opt2Skill: Imitating Dynamically-feasible Whole-Body Trajectories for Versatile Humanoid Loco-Manipulation](https://arxiv.org/abs/2409.20514) | 2024.09 |  | ⏳ 待读 |
| 159  | [HYPERmotion: Learning Hybrid Behavior Planning for Autonomous Loco-manipulation](https://arxiv.org/abs/2406.14655v1) | 2024.06 |  | ⏳ 待读 |
| 160  | [HumanPlus: Humanoid Shadowing and Imitation from Humans](https://arxiv.org/abs/2406.10454) | 2024.06 |  | ⏳ 待读 |
| 161  | [OmniH2O: Universal and Dexterous Human-to-Humanoid Whole-Body Teleoperation and Learning](https://arxiv.org/abs/2406.08858) | 2024.06 |  | ⏳ 待读 |
| 162  | [WoCoCo: Learning Whole-Body Humanoid Control with Sequential Contacts](https://arxiv.org/abs/2406.06005) | 2024.06 |  | ⏳ 待读 |
| 163  | [Learning Human-to-Humanoid Real-Time Whole-Body Teleoperation](https://arxiv.org/abs/2403.04436) | 2024.03 |  | ⏳ 待读 |
| 164  | [Expressive Whole-Body Control for Humanoid Robots](https://arxiv.org/abs/2402.16796) | 2024.02 |  | ⏳ 待读 |
| 165  | [Sim-to-Real Learning for Humanoid Box Loco-Manipulation](https://arxiv.org/abs/2310.03191) | 2023.10 |  | ⏳ 待读 |
| 166  | WholeBodyVLA: Towards Unified Latent VLA for Whole-body Loco-manipulation Control | 2025.12 |  | ⏳ 待读 |
| 167  | SPIDER: Scalable Physics-Informed DExterous Retargeting | 2025.11 |  | ⏳ 待读 |
| 168  | AdaMimic: Towards Adaptable Humanoid Control via Adaptive Motion Tracking | 2025.10 |  | ⏳ 待读 |
| 169  | General Motion Tracking for Humanoid Whole-Body Control | 2025.06 |  | ⏳ 待读 |
| 170  | CLONE: Holistic Closed-Loop Whole-Body Teleoperation for Long-Horizon Humanoid Control | 2025.06 |  | ⏳ 待读 |
| 171  | ASAP: Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills | 2025.02 |  | ⏳ 待读 |
| 172  | VMP: Versatile Motion Priors for Robustly Tracking Motion on Physical Characters | 2024.08 |  | ⏳ 待读 |
| 173  | Robot Motion Diffusion Model: Motion Generation for Robotic Characters | 2024.07 |  | ⏳ 待读 |
| 174  | [website],Embodied Chain of Action Reasoning with Multi-Modal Foundation Model for Humanoid Loco-manipulation | 2025.04 |  | ⏳ 待读 |
### Locomotion（84篇）

| #   | 论文 | 日期 | 🌟 | 状态 |
| --- | ---- | ---- | -- | ---- |
| 175  | [Biomechanical Comparisons Reveal Divergence of Human and Humanoid Gaits](https://arxiv.org/abs/2602.21666) | 2026.02 |  | ⏳ 待读 |
| 176  | [APEX: Learning Adaptive High-Platform Traversal for Humanoid Robots](https://arxiv.org/abs/2602.11143) | 2026.02 |  | ⏳ 待读 |
| 177  | [ECO: Energy-Constrained Optimization with Reinforcement Learning for Humanoid Walking](https://arxiv.org/abs/2602.06445) | 2026.02 |  | ⏳ 待读 |
| 178  | [Now You See That: Learning End-to-End Humanoid Locomotion from Raw Pixels](https://arxiv.org/abs/2602.06382) | 2026.02 |  | ⏳ 待读 |
| 179  | [A Hybrid Autoencoder for Robust Heightmap Generation from Fused Lidar and Depth Data for Humanoid Robot Locomotion](https://arxiv.org/abs/2602.05855) | 2026.02 |  | ⏳ 待读 |
| 180  | [Scalable and General Whole-Body Control for Cross-Humanoid Locomotion](https://arxiv.org/abs/2602.05791) | 2026.02 |  | ⏳ 待读 |
| 181  | [HoRD: Robust Humanoid Control via History-Conditioned Reinforcement Learning and Online Distillation](https://arxiv.org/abs/2602.04412) | 2026.02 |  | ⏳ 待读 |
| 182  | [CMR: Contractive Mapping Embeddings for Robust Humanoid Locomotion on Unstructured Terrains](https://arxiv.org/abs/2602.03511) | 2026.02 |  | ⏳ 待读 |
| 183  | [RPL: Learning Robust Humanoid Perceptive Locomotion on Challenging Terrains](https://arxiv.org/abs/2602.03002) | 2026.02 |  | ⏳ 待读 |
| 184  | [FastStair: Learning to Run Up Stairs with Humanoid Robots](https://arxiv.org/abs/2601.10365) | 2026.01 |  | ⏳ 待读 |
| 185  | [Walk the PLANC: Physics-Guided RL for Agile Humanoid Locomotion on Constrained Footholds](https://arxiv.org/abs/2601.06286) | 2026.01 |  | ⏳ 待读 |
| 186  | [SKATER: Synthesized Kinematics for Advanced Traversing Efficiency on a Humanoid Robot via Roller Skate Swizzles](https://arxiv.org/abs/2601.04948) | 2026.01 |  | ⏳ 待读 |
| 187  | Walk the PLANC: Physics‑Guided RL for Agile Humanoid LocomotioN on Constrained Footholds | 2026.01 |  | ⏳ 待读 |
| 188  | [Do You Have Freestyle? Expressive Humanoid Locomotion via Audio Control](https://arxiv.org/abs/2512.23650) | 2025.12 |  | ⏳ 待读 |
| 189  | [RoboMirror: Understand Before You Imitate for Video to Humanoid Locomotion](https://arxiv.org/abs/2512.23649) | 2025.12 |  | ⏳ 待读 |
| 190  | [E-SDS: Environment-aware See it, Do it, Sorted - Automated Environment-Aware Reinforcement Learning for Humanoid Locomotion](https://arxiv.org/abs/2512.16446) | 2025.12 |  | ⏳ 待读 |
| 191  | [Learning to Get Up Across Morphologies: Zero-Shot Recovery with a Unified Humanoid Policy](https://arxiv.org/abs/2512.12230) | 2025.12 |  | ⏳ 待读 |
| 192  | [Symphony: A Heuristic Normalized Calibrated Advantage Actor and Critic Algorithm in application for Humanoid Robots](https://arxiv.org/abs/2512.10477) | 2025.12 |  | ⏳ 待读 |
| 193  | [Learning Sim-to-Real Humanoid Locomotion in 15 Minutes](https://arxiv.org/abs/2512.01996) | 2025.12 |  | ⏳ 待读 |
| 194  | [H-Zero: Cross-Humanoid Locomotion Pretraining Enables Few-shot Novel Embodiment Transfer](https://arxiv.org/abs/2512.00971) | 2025.12 |  | ⏳ 待读 |
| 195  | [A Hierarchical Framework for Humanoid Locomotion with Supernumerary Limbs](https://arxiv.org/abs/2512.00077) | 2025.12 |  | ⏳ 待读 |
| 196  | [GaussGym: An open-source real-to-sim framework for learning locomotion from pixels](https://arxiv.org/abs/2510.15352) | 2025.10 |  | ⏳ 待读 |
| 197  | [Architecture Is All You Need: Diversity-Enabled Sweet Spots for Robust Humanoid Locomotion](https://arxiv.org/abs/2510.14947) | 2025.10 |  | ⏳ 待读 |
| 198  | [PolygMap: A Perceptive Locomotion Framework for Humanoid Robot Stair Climbing](https://arxiv.org/abs/2510.12346) | 2025.10 |  | ⏳ 待读 |
| 199  | [Preference-Conditioned Multi-Objective RL for Integrated Command Tracking and Force Compliance in Humanoid Locomotion](https://arxiv.org/abs/2510.10851) | 2025.10 |  | ⏳ 待读 |
| 200  | [DPL: Depth-only Perceptive Humanoid Locomotion via Realistic Depth Synthesis and Cross-Attention Terrain Reconstruction](https://arxiv.org/abs/2510.07152) | 2025.10 |  | ⏳ 待读 |
| 201  | [Stabilizing Humanoid Robot Trajectory Generation via Physics-Informed Learning](https://arxiv.org/abs/2509.24697) | 2025.09 |  | ⏳ 待读 |
| 202  | [RuN: Residual Policy for Natural Humanoid Locomotion](https://arxiv.org/abs/2509.20696) | 2025.09 |  | ⏳ 待读 |
| 203  | [Chasing Stability: Humanoid Running via Control Lyapunov Function Guided RL](https://arxiv.org/abs/2509.19573) | 2025.09 |  | ⏳ 待读 |
| 204  | [Reduced-Order Model-Guided RL for Demonstration-Free Humanoid Locomotion](https://arxiv.org/abs/2509.19023) | 2025.09 |  | ⏳ 待读 |
| 205  | [HuMam: Humanoid Motion Control via End-to-End Deep RL with Mamba](https://arxiv.org/abs/2509.18046) | 2025.09 |  | ⏳ 待读 |
| 206  | [Learning to Walk in Costume: Adversarial Motion Priors for Aesthetically Constrained Humanoids](https://arxiv.org/abs/2509.05581) | 2025.09 |  | ⏳ 待读 |
| 207  | LocoFormer: Generalist Locomotion via Long-Context Adaptation | 2025.09 |  | ⏳ 待读 |
| 208  | [Traversing Narrow Paths: A Two-Stage RL Framework for Robust and Safe Humanoid Walking](https://arxiv.org/abs/2508.20661) | 2025.08 |  | ⏳ 待读 |
| 209  | [No More Marching: Learning Humanoid Locomotion for Short-Range SE(2) Targets](https://arxiv.org/abs/2508.14098) | 2025.08 |  | ⏳ 待读 |
| 210  | [Geometry-Aware Predictive Safety Filters on Humanoids](https://arxiv.org/abs/2508.11129) | 2025.08 |  | ⏳ 待读 |
| 211  | [MASH: Cooperative-Heterogeneous Multi-Agent RL for Single Humanoid Robot Locomotion](https://arxiv.org/abs/2508.10423) | 2025.08 |  | ⏳ 待读 |
| 212  | [End-to-End Humanoid Robot Safe and Comfortable Locomotion Policy](https://arxiv.org/abs/2508.07611) | 2025.08 |  | ⏳ 待读 |
| 213  | [Optimizing Bipedal Locomotion for The 100m Dash With Comparison to Human Running](https://arxiv.org/abs/2508.03070) | 2025.08 |  | ⏳ 待读 |
| 214  | [Coordinated Humanoid Robot Locomotion with Symmetry Equivariant Reinforcement Learning Policy](https://arxiv.org/abs/2508.01247) | 2025.08 |  | ⏳ 待读 |
| 215  | [Success in Humanoid Reinforcement Learning under Partial Observation](https://arxiv.org/abs/2507.18883) | 2025.07 |  | ⏳ 待读 |
| 216  | Learning Humanoid Arm Motion via Centroidal Momentum Regularized Multi-Agent Reinforcement Learning | 2025.07 |  | ⏳ 待读 |
| 217  | [Mechanical Intelligence-Aware Curriculum RL for Humanoids with Parallel Actuation](https://arxiv.org/abs/2507.00273) | 2025.07 |  | ⏳ 待读 |
| 218  | [Booster Gym: An End-to-End RL Framework for Humanoid Robot Locomotion](https://arxiv.org/abs/2506.15132) | 2025.06 |  | ⏳ 待读 |
| 219  | [DoublyAware: Dual Planning and Policy Awareness for Temporal Difference Learning in Humanoid Locomotion](https://arxiv.org/abs/2506.12095) | 2025.06 |  | ⏳ 待读 |
| 220  | [MoRE: Mixture of Residual Experts for Humanoid Lifelike Gaits Learning on Complex Terrains](https://arxiv.org/abs/2506.08840) | 2025.06 |  | ⏳ 待读 |
| 221  | [A Gait Driven RL Framework for Humanoid Robots](https://arxiv.org/abs/2506.08416) | 2025.06 |  | ⏳ 待读 |
| 222  | [Learning Aerodynamics for the Control of Flying Humanoid Robots](https://arxiv.org/abs/2506.00305) | 2025.06 |  | ⏳ 待读 |
| 223  | [FastTD3: Simple, Fast, and Capable Reinforcement Learning for Humanoid Control](https://arxiv.org/abs/2505.22642) | 2025.05 |  | ⏳ 待读 |
| 224  | [Omni-Perception: Omnidirectional Collision Avoidance for Legged Locomotion in Dynamic Environments](https://arxiv.org/abs/2505.19214) | 2025.05 |  | ⏳ 待读 |
| 225  | [One Policy but Many Worlds: A Scalable Unified Policy for Versatile Humanoid Locomotion](https://arxiv.org/abs/2505.18780) | 2025.05 |  | ⏳ 待读 |
| 226  | [TD-GRPC: Temporal Difference Learning with Group Relative Policy Constraint for Humanoid Locomotion](https://arxiv.org/abs/2505.13549) | 2025.05 |  | ⏳ 待读 |
| 227  | [Dribble Master: Learning Agile Humanoid Dribbling Through Legged Locomotion](https://arxiv.org/abs/2505.12679) | 2025.05 |  | ⏳ 待读 |
| 228  | [SHIELD: Safety on Humanoids via CBFs In Expectation on Learned Dynamics](https://arxiv.org/abs/2505.11494) | 2025.05 |  | ⏳ 待读 |
| 229  | [Let Humanoids Hike! Integrative Skill Development on Complex Trails](https://arxiv.org/abs/2505.06218) | 2025.05 |  | ⏳ 待读 |
| 230  | [VideoMimic: Visual imitation enables contextual humanoid control](https://arxiv.org/abs/2505.03729) | 2025.05 |  | ⏳ 待读 |
| 231  | [SoccerDiffusion: Toward Learning End-to-End Humanoid Robot Soccer from Gameplay Recordings](https://arxiv.org/abs/2504.20808) | 2025.04 |  | ⏳ 待读 |
| 232  | [Robust Humanoid Walking on Compliant and Uneven Terrain with Deep RL](https://arxiv.org/abs/2504.13619) | 2025.04 |  | ⏳ 待读 |
| 233  | [PPF: Pre-training and Preservative Fine-tuning of Humanoid Locomotion](https://arxiv.org/abs/2504.09833) | 2025.04 |  | ⏳ 待读 |
| 234  | [Spectral Normalization for Lipschitz-Constrained Policies on Learning Humanoid Locomotion](https://arxiv.org/abs/2504.08246) | 2025.04 |  | ⏳ 待读 |
| 235  | [Learning Bipedal Locomotion on Gear-Driven Humanoid Robot Using Foot-Mounted IMUs](https://arxiv.org/abs/2504.00614) | 2025.04 |  | ⏳ 待读 |
| 236  | [StyleLoco: Generative Adversarial Distillation for Natural Humanoid Robot Locomotion](https://arxiv.org/abs/2503.15082) | 2025.03 |  | ⏳ 待读 |
| 237  | [Natural Humanoid Robot Locomotion with Generative Motion Prior](https://arxiv.org/abs/2503.09015) | 2025.03 |  | ⏳ 待读 |
| 238  | [LiPS: Large-Scale Humanoid Robot RL with Parallel-Series Structures](https://arxiv.org/abs/2503.08349) | 2025.03 |  | ⏳ 待读 |
| 239  | [HWC-Loco: A Hierarchical Whole-Body Control Approach to Robust Humanoid Locomotion](https://arxiv.org/abs/2503.00923) | 2025.03 |  | ⏳ 待读 |
| 240  | [Learning Perceptive Humanoid Locomotion over Challenging Terrain](https://arxiv.org/abs/2503.00692) | 2025.03 |  | ⏳ 待读 |
| 241  | [Humanoid Whole-Body Locomotion on Narrow Terrain via Dynamic Balance and Reinforcement Learning](https://arxiv.org/abs/2502.17219) | 2025.02 |  | ⏳ 待读 |
| 242  | [Learning Humanoid Locomotion with World Model Reconstruction](https://arxiv.org/abs/2502.16230) | 2025.02 |  | ⏳ 待读 |
| 243  | [VB-Com: Learning Vision-Blind Composite Humanoid Locomotion Against Deficient Perception](https://arxiv.org/abs/2502.14814) | 2025.02 |  | ⏳ 待读 |
| 244  | [BeamDojo: Learning Agile Humanoid Locomotion on Sparse Footholds](https://arxiv.org/abs/2502.10363) | 2025.02 |  | ⏳ 待读 |
| 245  | [Learning Humanoid Locomotion with Perceptive Internal Model](https://arxiv.org/abs/2411.14386) | 2024.11 |  | ⏳ 待读 |
| 246  | [Real-Time Polygonal Semantic Mapping for Humanoid Robot Stair Climbing](https://arxiv.org/abs/2411.01919) | 2024.11 |  | ⏳ 待读 |
| 247  | [Learning Smooth Humanoid Locomotion through Lipschitz-Constrained Policies](https://arxiv.org/abs/2410.11825) | 2024.10 |  | ⏳ 待读 |
| 248  | [Learning Humanoid Locomotion over Challenging Terrain](https://arxiv.org/abs/2410.03654) | 2024.10 |  | ⏳ 待读 |
| 249  | Bi-Level Motion Imitation for Humanoid Robots | 2024.10 |  | ⏳ 待读 |
| 250  | [Advancing Humanoid Locomotion: Mastering Challenging Terrains with Denoising World Model Learning](https://arxiv.org/abs/2408.14472) | 2024.08 |  | ⏳ 待读 |
| 251  | [Humanoid Parkour Learning](https://arxiv.org/abs/2406.10759) | 2024.06 |  | ⏳ 待读 |
| 252  | [Deep Reinforcement Learning for Bipedal Locomotion: A Brief Survey](https://arxiv.org/abs/2404.17070) | 2024.04 |  | ⏳ 待读 |
| 253  | [Humanoid Locomotion as Next Token Prediction](https://arxiv.org/abs/2402.19469) | 2024.02 |  | ⏳ 待读 |
| 254  | [Whole-body Humanoid Robot Locomotion with Human Reference](https://arxiv.org/abs/2402.18294) | 2024.02 |  | ⏳ 待读 |
| 255  | [Reinforcement Learning for Versatile, Dynamic, and Robust Bipedal Locomotion Control](https://arxiv.org/abs/2401.16889) | 2024.01 |  | ⏳ 待读 |
| 256  | [Learning to Walk and Fly with Adversarial Motion Priors](https://arxiv.org/abs/2309.12784) | 2023.09 |  | ⏳ 待读 |
| 257  | [Real-World Humanoid Locomotion with Reinforcement Learning](https://arxiv.org/abs/2303.03381) | 2023.03 |  | ⏳ 待读 |
| 258  | [Robust and Versatile Bipedal Jumping Control through Reinforcement Learning](https://arxiv.org/abs/2302.09450) | 2023.02 |  | ⏳ 待读 |

### Manipulation（54篇）

| #   | 论文 | 日期 | 🌟 | 状态 |
| --- | ---- | ---- | -- | ---- |
| 259  | [HumDex: Humanoid Dexterous Manipulation Made Easy](https://arxiv.org/abs/2603.12260) | 2026.03 |  | ⏳ 待读 |
| 260  | [cuRoboV2: Dynamics-Aware Motion Generation with Depth-Fused Distance Fields for High-DoF Robots](https://arxiv.org/abs/2603.05493) | 2026.03 |  | ⏳ 待读 |
| 261  | [DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos](https://arxiv.org/abs/2602.06949) | 2026.02 |  | ⏳ 待读 |
| 262  | [HumanoidVLM: Vision-Language-Guided Impedance Control for Contact-Rich Humanoid Manipulation](https://arxiv.org/abs/2601.14874) | 2026.01 |  | ⏳ 待读 |
| 263  | [Generalizable Geometric Prior and Recurrent Spiking Feature Learning for Humanoid Robot Manipulation](https://arxiv.org/abs/2601.09031) | 2026.01 |  | ⏳ 待读 |
| 264  | [DexterCap: An Affordable and Automated System for Capturing Dexterous Hand-Object Manipulation](https://arxiv.org/abs/2601.05844) | 2026.01 |  | ⏳ 待读 |
| 265  | [Genie Sim 3.0 : A High-Fidelity Comprehensive Simulation Platform for Humanoid Robot](https://arxiv.org/abs/2601.02078) | 2026.01 |  | ⏳ 待读 |
| 266  | Visual-tactile pretraining and online multitask learning for humanlike manipulation dexterity | 2026.01 |  | ⏳ 待读 |
| 267  | [SafeHumanoid: VLM-RAG-driven Control of Upper Body Impedance for Humanoid Robot](https://arxiv.org/abs/2511.23300) | 2025.11 |  | ⏳ 待读 |
| 268  | [Dexterity from Smart Lenses: Multi-Fingered Robot Manipulation with In-the-Wild Human Demonstrations](https://arxiv.org/abs/2511.16661) | 2025.11 |  | ⏳ 待读 |
| 269  | [In-N-On: Scaling Egocentric Manipulation with in-the-wild and on-task Data](https://arxiv.org/abs/2511.15704) | 2025.11 |  | ⏳ 待读 |
| 270  | [RGMP: Recurrent Geometric-prior Multimodal Policy for Generalizable Humanoid Robot Manipulation](https://arxiv.org/abs/2511.09141) | 2025.11 |  | ⏳ 待读 |
| 271  | [Lightning Grasp: High Performance Procedural Grasp Synthesis with Contact Fields](https://arxiv.org/abs/2511.07418) | 2025.11 |  | ⏳ 待读 |
| 272  | [EgoMI: Learning Active Vision and Whole-Body Manipulation from Egocentric Human Demonstrations](https://arxiv.org/abs/2511.00153) | 2025.11 |  | ⏳ 待读 |
| 273  | [Endowing GPT-4 with a Humanoid Body: Building the Bridge Between Off-the-Shelf VLMs and the Physical World](https://arxiv.org/abs/2511.00041) | 2025.11 |  | ⏳ 待读 |
| 274  | [Towards Proprioception-Aware Embodied Planning for Dual-Arm Humanoid Robots](https://arxiv.org/abs/2510.07882) | 2025.10 |  | ⏳ 待读 |
| 275  | ActiveUMI: Robotic Manipulation with Active Perception from Robot‑Free Human Demonstrations | 2025.10 |  | ⏳ 待读 |
| 276  | [EgoDemoGen: Novel Egocentric Demonstration Generation Enables Viewpoint-Robust Manipulation](https://arxiv.org/abs/2509.22578) | 2025.09 |  | ⏳ 待读 |
| 277  | [Residual Off-Policy RL for Finetuning Behavior Cloning Policies](https://arxiv.org/abs/2509.19301) | 2025.09 |  | ⏳ 待读 |
| 278  | [MimicDroid: In-Context Learning for Humanoid Robot Manipulation from Human Play Videos](https://arxiv.org/abs/2509.09769) | 2025.09 |  | ⏳ 待读 |
| 279  | [Masquerade: Learning from In-the-wild Human Videos using Data-Editing](https://arxiv.org/abs/2508.09976) | 2025.08 |  | ⏳ 待读 |
| 280  | [TOP: Time Optimization Policy for Stable and Accurate Standing Manipulation with Humanoid Robots](https://arxiv.org/abs/2508.00355) | 2025.08 |  | ⏳ 待读 |
| 281  | [H-RDT: Human Manipulation Enhanced Bimanual Robotic Manipulation](https://arxiv.org/abs/2507.23523) | 2025.07 |  | ⏳ 待读 |
| 282  | [Being-H0: Vision-Language-Action Pretraining from Large-Scale Human Videos](https://arxiv.org/abs/2507.15597) | 2025.07 |  | ⏳ 待读 |
| 283  | [EgoVLA: Learning Vision-Language-Action Models from Egocentric Human Videos](https://arxiv.org/abs/2507.12440) | 2025.07 |  | ⏳ 待读 |
| 284  | [Robot Drummer: Learning Rhythmic Skills for Humanoid Drumming](https://arxiv.org/abs/2507.11498) | 2025.07 |  | ⏳ 待读 |
| 285  | [Hierarchical Vision-Language Planning for Multi-Step Humanoid Manipulation](https://arxiv.org/abs/2506.22827) | 2025.06 |  | ⏳ 待读 |
| 286  | [Vision in Action: Learning Active Perception from Human Demonstrations](https://arxiv.org/abs/2506.15666) | 2025.06 |  | ⏳ 待读 |
| 287  | [DreamGen: Unlocking Generalization in Robot Learning through Neural Trajectories](https://arxiv.org/abs/2505.12705) | 2025.05 |  | ⏳ 待读 |
| 288  | [EgoDex: Learning Dexterous Manipulation from Large-Scale Egocentric Video](https://arxiv.org/abs/2505.11709) | 2025.05 |  | ⏳ 待读 |
| 289  | DexUMI: Using Human Hand as the Universal Manipulation Interface for Dexterous Manipulation | 2025.05 |  | ⏳ 待读 |
| 290  | [GR00T N1: An Open Foundation Model for Generalist Humanoid Robots](https://arxiv.org/abs/2503.14734) | 2025.03 |  | ⏳ 待读 |
| 291  | [Humanoid Policy ~ Human Policy](https://arxiv.org/abs/2503.13441) | 2025.03 |  | ⏳ 待读 |
| 292  | [Humanoids in Hospitals: A Technical Study of Humanoid Surrogates for Dexterous Medical Interventions](https://arxiv.org/abs/2503.12725) | 2025.03 |  | ⏳ 待读 |
| 293  | [Unified Video Action Model](https://arxiv.org/abs/2503.00200) | 2025.03 |  | ⏳ 待读 |
| 294  | [Dexterous Safe Control for Humanoids in Cluttered Environments via Projected Safe Set Algorithm](https://arxiv.org/abs/2502.02858) | 2025.02 |  | ⏳ 待读 |
| 295  | [MobileH2R: Learning Generalizable Human to Mobile Robot Handover Exclusively from Scalable and Diverse Synthetic Data](https://arxiv.org/abs/2501.04595) | 2025.01 |  | ⏳ 待读 |
| 296  | [ARMADA: Augmented Reality for Robot Manipulation and Robot-Free Data Acquisition](https://arxiv.org/abs/2412.10631) | 2024.12 |  | ⏳ 待读 |
| 297  | [Object-Centric Dexterous Manipulation from Human Motion Data](https://arxiv.org/abs/2411.04005) | 2024.11 |  | ⏳ 待读 |
| 298  | [DexHub and DART: Towards Internet-Scale Robot Data Collection](https://arxiv.org/abs/2411.02214) | 2024.11 |  | ⏳ 待读 |
| 299  | [Learning to Look Around: Enhancing Teleoperation and Learning with a Human-like Actuated Neck](https://arxiv.org/abs/2411.00704) | 2024.11 |  | ⏳ 待读 |
| 300  | [EgoMimic: Scaling Imitation Learning via Egocentric Video](https://arxiv.org/abs/2410.24221) | 2024.10 |  | ⏳ 待读 |
| 301  | [Learning to Look: Seeking Information for Decision Making via Policy Factorization](https://arxiv.org/abs/2410.18964) | 2024.10 |  | ⏳ 待读 |
| 302  | [OKAMI: Teaching Humanoid Robots Manipulation Skills through Single Video Imitation](https://arxiv.org/abs/2410.11792) | 2024.10 |  | ⏳ 待读 |
| 303  | [Generalizable Humanoid Manipulation with Improved 3D Diffusion Policies](https://arxiv.org/abs/2410.10803) | 2024.10 |  | ⏳ 待读 |
| 304  | Bimanual Dexterity for Complex Tasks | 2024.09 |  | ⏳ 待读 |
| 305  | [ACE: A Cross-Platform Visual-Exoskeletons System for Low-Cost Dexterous Teleoperation](https://arxiv.org/abs/2408.11805) | 2024.08 |  | ⏳ 待读 |
| 306  | [Bunny-VisionPro: Real-Time Bimanual Dexterous Teleoperation for Imitation Learning](https://arxiv.org/abs/2407.03162) | 2024.07 |  | ⏳ 待读 |
| 307  | [Open-TeleVision: Teleoperation with Immersive Active Visual Feedback](https://arxiv.org/abs/2407.01512) | 2024.07 |  | ⏳ 待读 |
| 308  | [Learning Visuotactile Skills with Two Multifingered Hands](https://arxiv.org/abs/2404.16823) | 2024.04 |  | ⏳ 待读 |
| 309  | [DexCap: Scalable and Portable Mocap Data Collection System for Dexterous Manipulation](https://arxiv.org/abs/2403.07788) | 2024.03 |  | ⏳ 待读 |
| 310  | DreamZero: World Action Models are Zero-shot Policies | - |  | ⏳ 待读 |
| 311  | A Systematic Study of Data Modalities and Strategies for Co-training Large Behavior Models for Robot Manipulation | - |  | ⏳ 待读 |
| 312  | Learning to Grasp Anything by Playing with Random Toys | - |  | ⏳ 待读 |

### Teleoperation（21篇）

| #   | 论文 | 日期 | 🌟 | 状态 |
| --- | ---- | ---- | -- | ---- |
| 313  | [CLOT: Closed-Loop Global Motion Tracking for Whole-Body Humanoid Teleoperation](https://arxiv.org/abs/2602.15060) | 2026.02 |  | ⏳ 待读 |
| 314  | [ExtremControl: Low-Latency Humanoid Teleoperation with Direct Extremity Control](https://arxiv.org/abs/2602.11321) | 2026.02 |  | ⏳ 待读 |
| 315  | [TeleGate: Whole-Body Humanoid Teleoperation via Gated Expert Selection with Motion Prior](https://arxiv.org/abs/2602.09628) | 2026.02 |  | ⏳ 待读 |
| 316  | [A Closed-Form Geometric Retargeting Solver for Upper Body Humanoid Robot Teleoperation](https://arxiv.org/abs/2602.01632) | 2026.02 |  | ⏳ 待读 |
| 317  | [Learning Adaptive Neural Teleoperation for Humanoid Robots](https://arxiv.org/abs/2511.12390) | 2025.11 |  | ⏳ 待读 |
| 318  | [Development of an Intuitive GUI for Non-Expert Teleoperation of Humanoid Robots](https://arxiv.org/abs/2510.13594) | 2025.10 |  | ⏳ 待读 |
| 319  | [Stability-Aware Retargeting for Humanoid Multi-Contact Teleoperation](https://arxiv.org/abs/2510.04353) | 2025.10 |  | ⏳ 待读 |
| 320  | [LapSurgie: Humanoid Robots Performing Surgery via Teleoperated Handheld Laparoscopy](https://arxiv.org/abs/2510.03529) | 2025.10 |  | ⏳ 待读 |
| 321  | [Whole-Body Bilateral Teleoperation with Multi-Stage Object Parameter Estimation for Wheeled Humanoid Locomanipulation](https://arxiv.org/abs/2508.09846) | 2025.08 |  | ⏳ 待读 |
| 322  | [CHILD: a Whole-Body Humanoid Teleoperation System](https://arxiv.org/abs/2508.00162) | 2025.08 |  | ⏳ 待读 |
| 323  | CHILD: Controller for Humanoid Imitation and Live Demonstration a Whole-Body Humanoid Teleoperation System | 2025.08 |  | ⏳ 待读 |
| 324  | [CLONE: Closed-Loop Whole-Body Humanoid Teleoperation for Long-Horizon Tasks](https://arxiv.org/abs/2506.08931) | 2025.06 |  | ⏳ 待读 |
| 325  | [Heavy lifting tasks via haptic teleoperation of a wheeled humanoid](https://arxiv.org/abs/2505.19530) | 2025.05 |  | ⏳ 待读 |
| 326  | [TeleOpBench: A Simulator-Centric Benchmark for Dual-Arm Dexterous Teleoperation](https://arxiv.org/abs/2505.12748) | 2025.05 |  | ⏳ 待读 |
| 327  | [Human-Robot Collaboration for the Remote Control of Mobile Humanoid Robots](https://arxiv.org/abs/2505.05773) | 2025.05 |  | ⏳ 待读 |
| 328  | [NuExo: A Wearable Exoskeleton Covering all Upper Limb ROM for Outdoor Data Collection and Teleoperation of Humanoid Robots](https://arxiv.org/abs/2503.10554) | 2025.03 |  | ⏳ 待读 |
| 329  | [Generalizable Humanoid Manipulation with 3D Diffusion Policies](https://arxiv.org/abs/2410.10803) | 2024.10 |  | ⏳ 待读 |
| 330  | [High-Speed and Impact Resilient Teleoperation of Humanoid Robots](https://arxiv.org/abs/2409.04639v1) | 2024.09 |  | ⏳ 待读 |
| 331  | [Deep Imitation Learning for Humanoid Loco-manipulation through Human Teleoperation](https://arxiv.org/abs/2309.01952) | 2023.09 |  | ⏳ 待读 |
| 332  | [Teleoperation of Humanoid Robots: A Survey](https://arxiv.org/abs/2301.04317) | 2023.01 |  | ⏳ 待读 |
| 333  | [iCub3 Avatar System: Enabling Remote Fully-Immersive Embodiment of Humanoid Robots](https://arxiv.org/abs/2203.06972) | 2022.03 |  | ⏳ 待读 |

### Navigation（15篇）

| #   | 论文 | 日期 | 🌟 | 状态 |
| --- | ---- | ---- | -- | ---- |
| 334  | [EgoActor: Grounding Task Planning into Spatial-aware Egocentric Actions for Humanoid Robots via Visual-Language Models](https://arxiv.org/abs/2602.04515) | 2026.02 |  | ⏳ 待读 |
| 335  | [FocusNav: Spatial Selective Attention with Waypoint Guidance for Humanoid Local Navigation](https://arxiv.org/abs/2601.12790) | 2026.01 |  | ⏳ 待读 |
| 336  | [STATE-NAV: Stability-Aware Traversability Estimation for Bipedal Navigation on Rough Terrain / [code](https://github.com/yzwfromk/STATE-NAV)](https://arxiv.org/abs/2506.01046) | 2025.12 |  | ⏳ 待读 |
| 337  | [Thinking in 360: Humanoid Visual Search in the Wild](https://arxiv.org/abs/2511.20351) | 2025.11 |  | ⏳ 待读 |
| 338  | [Quantum deep reinforcement learning for humanoid robot navigation task](https://arxiv.org/abs/2509.11388) | 2025.09 |  | ⏳ 待读 |
| 339  | [LookOut: Real-World Humanoid Egocentric Navigation](https://arxiv.org/abs/2508.14466) | 2025.08 |  | ⏳ 待读 |
| 340  | [INTENTION: Inferring Tendencies of Humanoid Robot Motion Through Interactive Intuition and Grounded VLM](https://arxiv.org/abs/2508.04931) | 2025.08 |  | ⏳ 待读 |
| 341  | [Hand-Eye Autonomous Delivery: Learning Humanoid Navigation, Locomotion and Reaching](https://arxiv.org/abs/2508.03068) | 2025.08 |  | ⏳ 待读 |
| 342  | Humanoid Occupancy: Enabling A Generalized Multimodal Occupancy Perception System on Humanoid Robots | 2025.07 |  | ⏳ 待读 |
| 343  | LOVON: Legged Open-Vocabulary Object Navigator | 2025.07 |  | ⏳ 待读 |
| 344  | [RL with Data Bootstrapping for Dynamic Subgoal Pursuit in Humanoid Robot Navigation](https://arxiv.org/abs/2506.02206) | 2025.06 |  | ⏳ 待读 |
| 345  | [HumanoidPano: Hybrid Spherical Panoramic-LiDAR Cross-Modal Perception for Humanoid Robots](https://arxiv.org/abs/2503.09010) | 2025.03 |  | ⏳ 待读 |
| 346  | [NaVILA: Legged Robot Vision-Language-Action Model for Navigation](https://arxiv.org/abs/2412.04453) | 2024.12 |  | ⏳ 待读 |
| 347  | [ARMOR: Egocentric Perception for Humanoid Robot Collision Avoidance and Motion Planning](https://arxiv.org/abs/2412.00396) | 2024.12 |  | ⏳ 待读 |
| 348  | [NoMaD: Goal Masked Diffusion Policies for Navigation and Exploration](https://arxiv.org/abs/2310.07896) | 2023.10 |  | ⏳ 待读 |

### State Estimation（10篇）

| #   | 论文 | 日期 | 🌟 | 状态 |
| --- | ---- | ---- | -- | ---- |
| 349  | [AutoOdom: Learning Auto-regressive Proprioceptive Odometry for Legged Locomotion](https://arxiv.org/abs/2511.18857) | 2025.11 |  | ⏳ 待读 |
| 350  | [InEKFormer: A Hybrid State Estimator for Humanoid Robots](https://arxiv.org/abs/2511.16306) | 2025.11 |  | ⏳ 待读 |
| 351  | [Physics-Informed Neural Networks with Unscented Kalman Filter for Sensorless Joint Torque Estimation](https://arxiv.org/abs/2507.10105) | 2025.07 |  | ⏳ 待读 |
| 352  | [An Empirical Evaluation of Four Off-the-Shelf Proprietary Visual-Inertial Odometry Systems](https://arxiv.org/abs/2207.06780) | 2022.07 |  | ⏳ 待读 |
| 353  | [Contact-Aided Invariant Extended Kalman Filtering for Robot State Estimation](https://arxiv.org/abs/1904.09251) | 2019.04 |  | ⏳ 待读 |
| 354  | [Legged Robot State-Estimation Through Combined Forward Kinematic and Preintegrated Contact Factors](https://arxiv.org/abs/1712.05873) | 2017.05 |  | ⏳ 待读 |
| 355  | [The invariant extended Kalman filter as a stable observer](https://arxiv.org/abs/1410.1465) | 2014.10 |  | ⏳ 待读 |
| 356  | GTSAM: Factor graphs for Sensor Fusion in Robotics | - |  | ⏳ 待读 |
| 357  | Kimera: an Open-Source Library for Real-Time Metric-Semantic Localization and Mapping | - |  | ⏳ 待读 |
| 358  | ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual-Inertial and Multi-Map SLAM | - |  | ⏳ 待读 |

### Sim-to-Real（10篇）

| #   | 论文 | 日期 | 🌟 | 状态 |
| --- | ---- | ---- | -- | ---- |
| 359  | [RAPT: Model-Predictive Out-of-Distribution Detection and Failure Diagnosis for Sim-to-Real Humanoid Robots](https://arxiv.org/abs/2602.01515) | 2026.02 |  | ⏳ 待读 |
| 360  | [Towards Bridging the Gap between Large-Scale Pretraining and Efficient Finetuning for Humanoid Control](https://arxiv.org/abs/2601.21363) | 2026.01 |  | ⏳ 待读 |
| 361  | [PolySim: Bridging the Sim-to-Real Gap for Humanoid Control via Multi-Simulator Dynamics Randomization](https://arxiv.org/abs/2510.01708) | 2025.10 |  | ⏳ 待读 |
| 362  | [Contrastive Representation Learning for Robust Sim-to-Real Transfer of Adaptive Humanoid Locomotion](https://arxiv.org/abs/2509.12858) | 2025.09 |  | ⏳ 待读 |
| 363  | [Towards bridging the gap: Systematic sim-to-real transfer for diverse legged robots](https://arxiv.org/abs/2509.06342) | 2025.09 |  | ⏳ 待读 |
| 364  | [Robot Trains Robot: Automatic Real-World Policy Adaptation and Learning for Humanoids](https://arxiv.org/abs/2508.12252) | 2025.08 |  | ⏳ 待读 |
| 365  | [DiffCoTune: Differentiable Co-Tuning for Cross-domain Robot Control](https://arxiv.org/abs/2505.24068) | 2025.05 |  | ⏳ 待读 |
| 366  | [Sim-to-Real of Humanoid Locomotion Policies via Joint Torque Space Perturbation Injection](https://arxiv.org/abs/2504.06585) | 2025.04 |  | ⏳ 待读 |
| 367  | [Bridging the Sim-to-Real Gap for Athletic Loco-Manipulation](https://arxiv.org/abs/2502.10894) | 2025.02 |  | ⏳ 待读 |
| 368  | [Learning Agile and Dynamic Motor Skills for Legged Robots](https://arxiv.org/abs/1901.08652) | 2019.01 |  | ⏳ 待读 |

### Simulation Benchmark（19篇）

| #   | 论文 | 日期 | 🌟 | 状态 |
| --- | ---- | ---- | -- | ---- |
| 369  | [GRUtopia: Dream General Robots in a City at Scale](https://arxiv.org/abs/2407.10943) | 2407.10 |  | ⏳ 待读 |
| 370  | [Towards Motion Turing Test: Evaluating Human-Likeness in Humanoid Robots](https://arxiv.org/abs/2603.06181) | 2026.03 |  | ⏳ 待读 |
| 371  | [MolmoSpaces: A Large-Scale Open Ecosystem for Robot Navigation and Manipulation](https://arxiv.org/abs/2602.11337) | 2026.02 |  | ⏳ 待读 |
| 372  | [Benchmarking Humanoid Imitation Learning with Motion Difficulty](https://arxiv.org/abs/2512.07248) | 2025.12 |  | ⏳ 待读 |
| 373  | [Generative World Modelling for Humanoids: 1X World Model Challenge Technical Report](https://arxiv.org/abs/2510.07092) | 2025.10 |  | ⏳ 待读 |
| 374  | [HumanoidGen: Data Generation for Bimanual Dexterous Manipulation via LLM Reasoning](https://arxiv.org/abs/2507.00833) | 2025.07 |  | ⏳ 待读 |
| 375  | [DualTHOR: A Dual-Arm Humanoid Simulation Platform for Contingency-Aware Planning](https://arxiv.org/abs/2506.16012) | 2025.06 |  | ⏳ 待读 |
| 376  | [Learning with pyCub: A Simulation and Exercise Framework for Humanoid Robotics](https://arxiv.org/abs/2506.01756) | 2025.06 |  | ⏳ 待读 |
| 377  | [Humanoid World Models: Open World Foundation Models for Humanoid Robotics](https://arxiv.org/abs/2506.01182) | 2025.06 |  | ⏳ 待读 |
| 378  | [Mimicking-Bench: A Benchmark for Generalizable Humanoid-Scene Interaction Learning via Human Mimicking](https://arxiv.org/abs/2412.17730) | 2024.12 |  | ⏳ 待读 |
| 379  | [ManiSkill-HAB: A Benchmark for Low-Level Manipulation in Home Rearrangement Tasks](https://arxiv.org/abs/2412.13211) | 2024.12 |  | ⏳ 待读 |
| 380  | Genesis: A Generative and Universal Physics Engine for Robotics and Beyond | 2024.12 |  | ⏳ 待读 |
| 381  | [DexMimicGen: Automated Data Generation for Bimanual Dexterous Manipulation via Imitation Learning](https://arxiv.org/abs/2410.24185) | 2024.10 |  | ⏳ 待读 |
| 382  | [ManiSkill3: GPU Parallelized Robotics Simulation and Rendering for Generalizable Embodied AI](https://arxiv.org/abs/2410.00425) | 2024.10 |  | ⏳ 待读 |
| 383  | [BiGym: A Demo-Driven Mobile Bi-Manual Manipulation Benchmark](https://arxiv.org/abs/2407.07788) | 2024.07 |  | ⏳ 待读 |
| 384  | [RoboCasa: Large-Scale Simulation of Everyday Tasks for Generalist Robots](https://arxiv.org/abs/2406.02523) | 2024.06 |  | ⏳ 待读 |
| 385  | [Humanoid-Gym: Reinforcement Learning for Humanoid Robot with Zero-Shot Sim2Real Transfer](https://arxiv.org/abs/2404.05695) | 2024.04 |  | ⏳ 待读 |
| 386  | [HumanoidBench: Simulated Humanoid Benchmark for Whole-Body Locomotion and Manipulation](https://arxiv.org/abs/2403.10506) | 2024.03 |  | ⏳ 待读 |
| 387  | RoboCasa365: A Large-Scale Simulation Framework for Training and Benchmarking Generalist Robots | - |  | ⏳ 待读 |

### Hardware Design（36篇）

| #   | 论文 | 日期 | 🌟 | 状态 |
| --- | ---- | ---- | -- | ---- |
| 388  | [Characteristics, Management, and Utilization of Muscles in Musculoskeletal Humanoids](https://arxiv.org/abs/2602.08518) | 2026.02 |  | ⏳ 待读 |
| 389  | [Fauna Sprout: A lightweight, approachable, developer-ready humanoid robot](https://arxiv.org/abs/2601.18963) | 2026.01 |  | ⏳ 待读 |
| 390  | [Antagonistic Bowden-Cable Actuation of a Lightweight Robotic Hand: Toward Dexterous Manipulation for Payload Constrained Humanoids](https://arxiv.org/abs/2512.24657) | 2025.12 |  | ⏳ 待读 |
| 391  | [Olaf: Bringing an Animated Character to Life in the Physical World](https://arxiv.org/abs/2512.16705) | 2025.12 |  | ⏳ 待读 |
| 392  | [OSMO: Open-Source Tactile Glove for Human-to-Robot Skill Transfer](https://arxiv.org/abs/2512.08920) | 2025.12 |  | ⏳ 待读 |
| 393  | [DIJIT: A Robotic Head for an Active Observer](https://arxiv.org/abs/2512.07998) | 2025.12 |  | ⏳ 待读 |
| 394  | [DecARt Leg: Design and Evaluation of a Novel Humanoid Robot Leg with Decoupled Actuation for Agile Locomotion](https://arxiv.org/abs/2511.10021) | 2025.11 |  | ⏳ 待读 |
| 395  | [Human-Level Actuation for Humanoids](https://arxiv.org/abs/2511.06796) | 2025.11 |  | ⏳ 待读 |
| 396  | [Toward Humanoid Brain-Body Co-design: Joint Optimization of Control and Morphology for Fall Recovery](https://arxiv.org/abs/2510.22336) | 2025.10 |  | ⏳ 待读 |
| 397  | [Embracing Evolution: A Call for Body-Control Co-Design in Embodied Humanoid Robot](https://arxiv.org/abs/2510.03081) | 2025.10 |  | ⏳ 待读 |
| 398  | [Evolutionary Continuous Adaptive RL-Powered Co-Design for Humanoid Chin-Up Performance](https://arxiv.org/abs/2509.26082) | 2025.09 |  | ⏳ 待读 |
| 399  | [A Framework for Optimal Ankle Design of Humanoid Robots](https://arxiv.org/abs/2509.16469) | 2025.09 |  | ⏳ 待读 |
| 400  | [CAD-Driven Co-Design for Flight-Ready Jet-Powered Humanoids](https://arxiv.org/abs/2509.14935) | 2025.09 |  | ⏳ 待读 |
| 401  | [AGILOped: Agile Open-Source Humanoid Robot for Research](https://arxiv.org/abs/2509.09364) | 2025.09 |  | ⏳ 待读 |
| 402  | [A 21-DOF Humanoid Dexterous Hand with Hybrid SMA-Motor Actuation: CYJ Hand-0](https://arxiv.org/abs/2507.14538) | 2025.07 |  | ⏳ 待读 |
| 403  | [Dexterous Teleoperation of 20-DoF ByteDexter Hand via Human Motion Retargeting](https://arxiv.org/abs/2507.03227) | 2025.07 |  | ⏳ 待读 |
| 404  | [PIMBS: Efficient Body Schema Learning for Musculoskeletal Humanoids](https://arxiv.org/abs/2506.20343) | 2025.06 |  | ⏳ 待读 |
| 405  | [Explosive Output to Enhance Jumping Ability: A Variable Reduction Ratio Design Paradigm for Humanoid Robots Knee Joint](https://arxiv.org/abs/2506.12314) | 2025.06 |  | ⏳ 待读 |
| 406  | [RAPID Hand: A Robust, Affordable, Perception-Integrated, Dexterous Manipulation Platform for Generalist Robot Autonomy](https://arxiv.org/abs/2506.07490) | 2025.06 |  | ⏳ 待读 |
| 407  | [iRonCub 3: The Jet-Powered Flying Humanoid Robot](https://arxiv.org/abs/2506.01125) | 2025.06 |  | ⏳ 待读 |
| 408  | [Berkeley Humanoid Lite: An Open-source, Accessible, and Customizable 3D-printed Humanoid Robot](https://arxiv.org/abs/2504.17249) | 2025.04 |  | ⏳ 待读 |
| 409  | [RUKA: Rethinking the Design of Humanoid Hands with Learning](https://arxiv.org/abs/2504.13165) | 2025.04 |  | ⏳ 待读 |
| 410  | [ORCA: Open-Source, Reliable, Cost-Effective, Anthropomorphic Robotic Hand for Uninterrupted Dexterous Task Learning](https://arxiv.org/abs/2504.04259) | 2025.04 |  | ⏳ 待读 |
| 411  | [Control of Humanoid Robots with Parallel Mechanisms using Kinematic Actuation Models](https://arxiv.org/abs/2503.22459) | 2025.03 |  | ⏳ 待读 |
| 412  | [Exceeding the Maximum Speed Limit of the Joint Angle for the Redundant Tendon-driven Structures of Musculoskeletal Humanoids](https://arxiv.org/abs/2502.12808) | 2025.02 |  | ⏳ 待读 |
| 413  | [ToddlerBot: Open-Source ML-Compatible Humanoid Platform for Loco-Manipulation](https://arxiv.org/abs/2502.00893) | 2025.02 |  | ⏳ 待读 |
| 414  | [Design and Control of a Bipedal Robotic Character](https://arxiv.org/abs/2501.05204) | 2025.01 |  | ⏳ 待读 |
| 415  | [The Duke Humanoid: Design and Control For Energy Efficient Bipedal Locomotion Using Passive Dynamics](https://arxiv.org/abs/2409.19795) | 2024.09 |  | ⏳ 待读 |
| 416  | [The MIT Humanoid Robot: Design, Motion Planning, and Control For Acrobatic Behaviors](https://arxiv.org/abs/2104.09025) | 2021.04 |  | ⏳ 待读 |
| 417  | [Quasi-Direct Drive for Low-Cost Compliant Robotic Manipulation](https://arxiv.org/abs/1904.03815) | 2019.04 |  | ⏳ 待读 |
| 418  | Micro-Wheeled_leg-Robot | - |  | ⏳ 待读 |
| 419  | Aero Hand Open | - |  | ⏳ 待读 |
| 420  | DexWrist: A Robotic Wrist for Constrained and Dynamic Manipulation | - |  | ⏳ 待读 |
| 421  | ByteWrist: A Parallel Robotic Wrist Enabling Flexible and Anthropomorphic Motion for Confined Spaces | - |  | ⏳ 待读 |
| 422  | Integrated linkage-driven dexterous anthropomorphic robotic hand | - |  | ⏳ 待读 |
| 423  | Proprioceptive actuator design in the MIT Cheetah: Impact mitigation and high‑bandwidth physical interaction for dynamic legged robots | - |  | ⏳ 待读 |

### Physics-Based Character Animation（23篇）

| #   | 论文 | 日期 | 🌟 | 状态 |
| --- | ---- | ---- | -- | ---- |
| 424  | Spatial relationship preserving character motion adaptation | 3349.17 |  | ⏳ 待读 |
| 425  | [Iterative Closed-Loop Motion Synthesis for Scaling the Capabilities of Humanoid Control](https://arxiv.org/abs/2602.21599) | 2026.02 |  | ⏳ 待读 |
| 426  | [CRISP: Contact-Guided Real2Sim from Monocular Video with Planar Scene Primitives](https://arxiv.org/abs/2512.14696) | 2025.12 |  | ⏳ 待读 |
| 427  | [Learning to Control Physically-simulated 3D Characters via Generating and Mimicking 2D Motions](https://arxiv.org/abs/2512.08500) | 2025.12 |  | ⏳ 待读 |
| 428  | [PhysHMR: Learning Humanoid Control Policies from Vision for Physically Plausible Human Motion Reconstruction](https://arxiv.org/abs/2510.02566) | 2025.10 |  | ⏳ 待读 |
| 429  | [Learning to Ball: Composing Policies for Long-Horizon Basketball Moves](https://arxiv.org/abs/2509.22442) | 2025.09 |  | ⏳ 待读 |
| 430  | [RobotDancing: Residual-Action RL Enables Robust Long-Horizon Humanoid Motion Tracking](https://arxiv.org/abs/2509.20717) | 2025.09 |  | ⏳ 待读 |
| 431  | [SimGenHOI: Physically Realistic Whole-Body Humanoid-Object Interaction via Generative Modeling and RL](https://arxiv.org/abs/2508.14120) | 2025.08 |  | ⏳ 待读 |
| 432  | [Humanoid Robot Acrobatics Utilizing Complete Articulated Rigid Body Dynamics](https://arxiv.org/abs/2508.08258) | 2025.08 |  | ⏳ 待读 |
| 433  | [RL from Physical Feedback: Aligning Large Motion Models with Humanoid Control](https://arxiv.org/abs/2506.12769) | 2025.06 |  | ⏳ 待读 |
| 434  | [AMOR: Adaptive Character Control through Multi-Objective Reinforcement Learning](https://arxiv.org/abs/2505.23708) | 2025.05 |  | ⏳ 待读 |
| 435  | [MaskedManipulator: Versatile Whole-Body Control for Loco-Manipulation](https://arxiv.org/abs/2505.19086) | 2025.05 |  | ⏳ 待读 |
| 436  | [Emergent Active Perception and Dexterity of Simulated Humanoids from Visual Reinforcement Learning](https://arxiv.org/abs/2505.12278) | 2025.05 |  | ⏳ 待读 |
| 437  | [Zero-Shot Whole-Body Humanoid Control via Behavioral Foundation Models](https://arxiv.org/abs/2504.11054) | 2025.04 |  | ⏳ 待读 |
| 438  | [CLoSD: Closing the Loop between Simulation and Diffusion for multi-task character control](https://arxiv.org/abs/2410.03441) | 2024.10 |  | ⏳ 待读 |
| 439  | [SkillMimic: Learning Basketball Interaction Skills from Demonstrations](https://arxiv.org/abs/2408.15270) | 2024.08 |  | ⏳ 待读 |
| 440  | [Unified Human-Scene Interaction via Prompted Chain-of-Contacts](https://arxiv.org/abs/2309.07918) | 2023.09 |  | ⏳ 待读 |
| 441  | [Hierarchical Planning and Control for Box Loco-Manipulation](https://arxiv.org/abs/2306.09532) | 2023.06 |  | ⏳ 待读 |
| 442  | [Perpetual Humanoid Control for Real-time Simulated Avatars](https://arxiv.org/abs/2305.06456) | 2023.05 |  | ⏳ 待读 |
| 443  | [Hierarchical visuomotor control of humanoids](https://arxiv.org/abs/1811.09656) | 2018.11 |  | ⏳ 待读 |
| 444  | [Multi-task Deep Reinforcement Learning with PopArt](https://arxiv.org/abs/1809.04474) | 2018.09 |  | ⏳ 待读 |
| 445  | [Learning Symmetric and Low-energy Locomotion](https://arxiv.org/abs/1801.08093) | 2018.01 |  | ⏳ 待读 |
| 446  | Composite Motion Learning with Task Control | - |  | ⏳ 待读 |

### Human Motion Analysis and Synthesis（22篇）

| #   | 论文 | 日期 | 🌟 | 状态 |
| --- | ---- | ---- | -- | ---- |
| 447  | Learned motion matching | 6569.33 |  | ⏳ 待读 |
| 448  | [EmbodMocap: In-the-Wild 4D Human-Scene Reconstruction for Embodied Agents](https://arxiv.org/abs/2602.23205) | 2026.02 |  | ⏳ 待读 |
| 449  | [WHOLE: World-Grounded Hand-Object Lifted from Egocentric Videos](https://arxiv.org/abs/2602.22209) | 2026.02 |  | ⏳ 待读 |
| 450  | [Diffusion Forcing for Multi-Agent Interaction Sequence Modeling](https://arxiv.org/abs/2512.17900) | 2025.12 |  | ⏳ 待读 |
| 451  | Control Operators for Interactive Character Animation | 2025.12 |  | ⏳ 待读 |
| 452  | Implicit Bézier Motion Model for Precise Spatial and Temporal Control | 2025.12 |  | ⏳ 待读 |
| 453  | [Efficient and Scalable Monocular Human-Object Interaction Motion Reconstruction](https://arxiv.org/abs/2512.00960) | 2025.12 |  | ⏳ 待读 |
| 454  | [Being-M0.5: A Real-Time Controllable Vision-Language-Motion Model](https://arxiv.org/abs/2508.07863) | 2025.08 |  | ⏳ 待读 |
| 455  | Go to Zero: Towards Zero-shot Motion Generation with Million-scale Data | 2025.07 |  | ⏳ 待读 |
| 456  | [GENMO: A GENeralist Model for Human MOtion](https://arxiv.org/abs/2505.01425) | 2025.05 |  | ⏳ 待读 |
| 457  | [PICO: Reconstructing 3D People In Contact with Objects](https://arxiv.org/abs/2504.17695) | 2025.04 |  | ⏳ 待读 |
| 458  | Climber Force and Motion Estimation from Video | 2025.04 |  | ⏳ 待读 |
| 459  | [FRAME: Floor-aligned Representation for Avatar Motion from Egocentric Video](https://arxiv.org/abs/2503.23094) | 2025.03 |  | ⏳ 待读 |
| 460  | [PRIMAL Physically Reactive and Interactive Motor Model for Avatar Learning](https://arxiv.org/abs/2503.17544) | 2025.03 |  | ⏳ 待读 |
| 461  | [Scaling Large Motion Models with Million-Level Human Motions](https://arxiv.org/abs/2410.03311) | 2024.10 |  | ⏳ 待读 |
| 462  | [Flexible Motion In-betweening with Diffusion Models](https://arxiv.org/abs/2405.11126) | 2024.05 |  | ⏳ 待读 |
| 463  | [Taming Diffusion Probabilistic Models for Character Control](https://arxiv.org/abs/2404.15121) | 2024.04 |  | ⏳ 待读 |
| 464  | [OmniControl: Control Any Joint at Any Time for Human Motion Generation](https://arxiv.org/abs/2310.08580) | 2023.10 |  | ⏳ 待读 |
| 465  | [TEDi: Temporally-Entangled Diffusion for Long-Term Motion Synthesis](https://arxiv.org/abs/2307.15042) | 2023.07 |  | ⏳ 待读 |
| 466  | [Guided Motion Diffusion for Controllable Human Motion Synthesis](https://arxiv.org/abs/2305.12577) | 2023.05 |  | ⏳ 待读 |
| 467  | [PhysDiff: Physics-Guided Human Motion Diffusion Model](https://arxiv.org/abs/2212.02500) | 2022.12 |  | ⏳ 待读 |
| 468  | Generating Diverse and Natural 3D Human Motions From Text | - |  | ⏳ 待读 |
| 469  | [Ψ₀: An Open Foundation Model Towards Universal Humanoid Loco-Manipulation](https://arxiv.org/abs/2603.12263) | 2026.03 |  | ⏳ 待读 |
| 470  | [SteadyTray: Learning Object Balancing Tasks in Humanoid Tray Transport via Residual RL](https://arxiv.org/abs/2603.10306) | 2026.03 |  | ⏳ 待读 |
| 471  | [ZeroWBC: Learning Natural Visuomotor Humanoid Control from Human Egocentric Video](https://arxiv.org/abs/2603.09170) | 2026.03 |  | ⏳ 待读 |
| 472  | [FAME: Force-Adaptive RL for Expanding the Manipulation Envelope of a Full-Scale Humanoid](https://arxiv.org/abs/2603.08961) | 2026.03 |  | ⏳ 待读 |
| 473  | [Embedding Classical Balance Control Principles in RL for Humanoid Recovery](https://arxiv.org/abs/2603.08619) | 2026.03 |  | ⏳ 待读 |
| 474  | [ULTRA: Unified Multimodal Control for Autonomous Humanoid Whole-Body Loco-Manipulation](https://arxiv.org/abs/2603.03279) | 2026.03 |  | ⏳ 待读 |
| 475  | [OmniXtreme: Breaking the Generality Barrier in High-Dynamic Humanoid Control](https://arxiv.org/abs/2602.23843) | 2026.02 |  | ⏳ 待读 |
| 476  | [LessMimic: Long-Horizon Humanoid Interaction with Unified Distance Field Representations](https://arxiv.org/abs/2602.21723) | 2026.02 |  | ⏳ 待读 |
| 477  | [Learning Humanoid End-Effector Control for Open-Vocabulary Visual Loco-Manipulation](https://arxiv.org/abs/2602.16705) | 2026.02 |  | ⏳ 待读 |
| 478  | [VIGOR: Visual Goal-In-Context Inference for Unified Humanoid Fall Safety](https://arxiv.org/abs/2602.16511) | 2026.02 |  | ⏳ 待读 |
| 479  | [Humanoid Hanoi: Investigating Shared Whole-Body Control for Skill-Based Box Rearrangement](https://arxiv.org/abs/2602.13850) | 2026.02 |  | ⏳ 待读 |
| 480  | [DynaRetarget: Dynamically-Feasible Retargeting using Sampling-Based Trajectory Optimization](https://arxiv.org/abs/2602.06827) | 2026.02 |  | ⏳ 待读 |
| 481  | [SoftMimic: Learning Compliant Whole-body Control from Examples](https://arxiv.org/abs/2510.17792) | 2025.10 |  | ⏳ 待读 |
| 482  | [Learning Differentiable Reachability Maps for Optimization-based Humanoid Motion Generation](https://arxiv.org/abs/2508.11275) | 2025.08 |  | ⏳ 待读 |
| 483  | [BeyondMimic: From Motion Tracking to Versatile Humanoid Control via Guided Diffusion](https://arxiv.org/abs/2508.08241) | 2025.08 |  | ⏳ 待读 |
| 484  | [KungfuBot: Physics-Based Humanoid Whole-Body Control for Learning Highly-Dynamic Skills](https://arxiv.org/abs/2506.12851) | 2025.06 |  | ⏳ 待读 |
| 485  | [Whole-body Multi-contact Motion Control for Humanoid Robots Based on Distributed Tactile Sensors](https://arxiv.org/abs/2505.19580) | 2025.05 |  | ⏳ 待读 |
| 486  | [FLAM: Foundation Model-Based Body Stabilization for Humanoid Locomotion and Manipulation](https://arxiv.org/abs/2503.22249) | 2025.03 |  | ⏳ 待读 |
| 487  | [The Role of Domain Randomization in Training Diffusion Policies for Whole-Body Humanoid Control](https://arxiv.org/abs/2411.01349) | 2024.11 |  | ⏳ 待读 |
| 488  | [Full-Order Sampling-Based MPC for Torque-Level Locomotion Control via Diffusion-Style Annealing](https://arxiv.org/abs/2409.15610) | 2024.09 |  | ⏳ 待读 |
| 489  | [Flow Matching Imitation Learning for Multi-Support Manipulation](https://arxiv.org/abs/2407.12381) | 2024.07 |  | ⏳ 待读 |
| 490  | [Predictive Sampling: Real-time Behaviour Synthesis with MuJoCo](https://arxiv.org/abs/2212.00541) | 2022.12 |  | ⏳ 待读 |
