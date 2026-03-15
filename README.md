# 📚 每日论文阅读计划

**来源**: [awesome-humanoid-robot-learning](https://github.com/YanjieZe/awesome-humanoid-robot-learning)

**当前板块**: Loco-Manipulation and Whole-Body-Control

## 规则

1. 每天早上 7:00 推送当日论文阅读提醒
2. 冲回复"理解了"后，才进入下一篇
3. 如果当天没有回复"理解了"，第二天继续提醒同一篇
4. 回复"理解了"后，对话记录也会保存到对应的 MD 笔记中
5. 可以随时说"读下一篇"跳到一篇

## 笔记说明

每篇笔记包含：
- 论文基本信息（PDF、GitHub、项目主页等）
- 核心问题与动机
- 方法详解（深入浅出，面试可答）
- 工程复现要点
- 关键公式与算法
- 面试高频问题 & 参考回答
- 讨论记录

## 学习路线图

```
【基础RL】
  PPO → AWR
       ↓
【精确模仿主线】          【风格学习主线】
  DeepMimic (2018)  →→→  AMP (2021)
       ↓                    ↓
  PHC (2023)            ADD (2025)
       ↓
【技能组合主线】
  ASE (2022) → CALM (2023) → PULSE (2024)
       ↓
【扩散+控制终点】
  Diffusion Policy → BeyondMimic (2025)

【Sim-to-Real 工程层】  ← 横跨整个路线
  LCP (2025)  ← 动作平滑，替代低通滤波器
```

## 进度

### 已完成（Loco-Manipulation 前置）

| #   | 论文                                                                                       | 笔记                                                                                          | PDF           | 状态     | 日期         |
| --- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------- | ------ | ---------- |
| 1   | ULTRA: Unified Multimodal Control for Autonomous Humanoid Whole-Body Loco-Manipulation   | [[ULTRA_Unified_Multimodal_Control_for_Autonomous_Humanoid_Whole-Body_Loco-Manipulation]]   | [[ULTRA.pdf]] | ✅ 完成  | 2026-03-07 |
| 2   | OmniXtreme: Breaking the Generality Barrier in High-Dynamic Humanoid Control             | [[OmniXtreme_Breaking_the_Generality_Barrier_in_High-Dynamic_Humanoid_Control]]             | [[OmniXtreme.pdf]] | ✅ 完成  | 2026-03-08 |

### 基础路线图（当前）

| #   | 论文                                                                                       | 笔记                                                                                          | PDF           | 状态     | 日期         | 路线 |
| --- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------- | ------ | ---------- | ---- |
| 3   | PPO: Proximal Policy Optimization                                                        | [[PPO_Proximal_Policy_Optimization]]                                                        | [[PPO_Proximal_Policy_Optimization.pdf]] | 📖 进行中 | -          | 基础RL |
| 4   | AWR: Advantage Weighted Regression                                                       | [[AWR_Advantage_Weighted_Regression]]                                                       | [[AWR.pdf]] | ⏳ 待读   | -          | 基础RL |
| 5   | DeepMimic: Example-Guided Deep RL of Physics-Based Character Skills                     | [[DeepMimic_Example-Guided_Deep_RL_of_Physics-Based_Character_Skills]]                     | [[DeepMimic.pdf]] | ⏳ 待读   | -          | 精确模仿 |
| 6   | AMP: Adversarial Motion Priors for Stylized Physics-Based Character Control              | [[AMP_Adversarial_Motion_Priors]]                                                           | [[AMP.pdf]] | ⏳ 待读   | -          | 风格学习 |
| 7   | PHC: Perpetual Humanoid Control for Real-time Simulated Avatars                          | [[PHC_Perpetual_Humanoid_Control]]                                                          | [[PHC.pdf]] | ⏳ 待读   | -          | 精确模仿 |
| 8   | ADD: Adversarial Disentanglement and Distillation                                        | [[ADD_Adversarial_Disentanglement_and_Distillation]]                                        | [[ADD.pdf]] | ⏳ 待读   | -          | 风格学习 |
| 9   | ASE: Adversarial Skill Embeddings for Large-Scale Motion Control                         | [[ASE_Adversarial_Skill_Embeddings]]                                                        | [[ASE.pdf]] | ⏳ 待读   | -          | 技能组合 |
| 10  | CALM: Conditional Adversarial Latent Models for Directable Virtual Characters            | [[CALM_Conditional_Adversarial_Latent_Models]]                                              | [[CALM.pdf]] | ⏳ 待读   | -          | 技能组合 |
| 11  | PULSE: Physically Plausible Universal Latent Skill Extraction                            | [[PULSE_Physically_Plausible_Universal_Latent_Skill_Extraction]]                            | [[PULSE.pdf]] | ⏳ 待读   | -          | 技能组合 |
| 12  | Diffusion Policy: Visuomotor Policy Learning via Action Diffusion                        | [[Diffusion_Policy_Visuomotor_Policy_Learning]]                                             | [[Diffusion_Policy.pdf]] | ⏳ 待读   | -          | 扩散+控制 |
| 13  | BeyondMimic: From Motion Tracking to Versatile Humanoid Control via Guided Diffusion     | [[BeyondMimic_From_Motion_Tracking_to_Versatile_Humanoid_Control]]                          | [[BeyondMimic.pdf]] | ⏳ 待读   | -          | 扩散+控制 |
| 14  | LCP: Sim-to-Real Action Smoothing                                                        | [[LCP_Sim-to-Real_Action_Smoothing]]                                                        | [[LCP.pdf]] | ⏳ 待读   | -          | Sim-to-Real |

### Loco-Manipulation 论文（路线图之后）

| #   | 论文                                                                                       | 笔记                                                                                          | PDF           | 状态     | 日期         |
| --- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------- | ------ | ---------- |
| 15  | LessMimic: Long-Horizon Humanoid Interaction with Unified Distance Field Representations | [[LessMimic_Long-Horizon_Humanoid_Interaction_with_Unified_Distance_Field_Representations]] | [[LessMimic.pdf]]  | ⏳ 待读   | -          |
| 16  | Learning Humanoid End-Effector Control for Open-Vocabulary Visual Loco-Manipulation      | [[Learning_Humanoid_End-Effector_Control_for_Open-Vocabulary_Visual_Loco-Manipulation]]     | [[Learning_Humanoid_End-Effector.pdf]] | ⏳ 待读   | -          |
| 17  | VIGOR: Visual Goal-In-Context Inference for Unified Humanoid Fall Safety                 | [[VIGOR_Visual_Goal-In-Context_Inference_for_Unified_Humanoid_Fall_Safety]]                 | [[VIGOR.pdf]]      | ⏳ 待读   | -          |
| 18  | Ψ₀: An Open Foundation Model Towards Universal Humanoid Loco-Manipulation               | [[Psi0_An_Open_Foundation_Model_Towards_Universal_Humanoid_Loco-Manipulation]]               | [[Psi0.pdf]] | ⏳ 待读   | -          |
| 19  | SteadyTray: Learning Object Balancing Tasks in Humanoid Tray Transport via Residual RL   | [[SteadyTray_Learning_Object_Balancing_Tasks_via_Residual_RL]]                               | [[SteadyTray.pdf]] | ⏳ 待读   | -          |
| 20  | ZeroWBC: Learning Natural Visuomotor Humanoid Control from Egocentric Video              | [[ZeroWBC_Learning_Natural_Visuomotor_Humanoid_Control_from_Egocentric_Video]]               | [[ZeroWBC.pdf]] | ⏳ 待读   | -          |
| 21  | Embedding Classical Balance Control Principles in RL for Humanoid Recovery               | [[Embedding_Classical_Balance_Control_in_RL_for_Humanoid_Recovery]]                          | [[Embedding_Classical_Balance_Control.pdf]] | ⏳ 待读   | -          |
| 22  | FAME: Force-Adaptive RL for Expanding the Manipulation Envelope of a Full-Scale Humanoid | [[FAME_Force-Adaptive_RL_for_Expanding_Manipulation_Envelope]]                               | [[FAME.pdf]] | ⏳ 待读   | -          |
