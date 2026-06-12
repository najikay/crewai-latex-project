# Domain Contribution: Multi-Modal Sensor Fusion Networks and Reinforcement Learning for Bat-Inspired Drone Navigation

## 1. Technical Analysis (State-of-the-Art 2024–2026)

### 1.1 Multi-Modal Sensor Fusion Architectures

The dominant paradigm for fusing heterogeneous sensor modalities (sonar, IMU, camera, LiDAR) in autonomous navigation has shifted from simple concatenation or Kalman-filter-based fusion to learned, attention-driven architectures. Cross-attention mechanisms, originally developed for machine translation (Vaswani et al., 2017), have been adapted for sensor fusion where queries from one modality attend to keys/values from another, enabling dynamic re-weighting of modality contributions based on context. Shim et al. (2019) demonstrated that fusion weight regularization improves robustness against sensor dropout, achieving a 12.3% reduction in mean average precision (mAP) degradation when one modality fails. More recently, gating networks—learned scalar or vector gates that modulate the contribution of each modality—have become standard. The gating function $g(\mathbf{z}) = \sigma(\mathbf{W}_g \mathbf{z} + \mathbf{b}_g)$, where $\sigma$ is the sigmoid activation, produces weights in $[0,1]$ that are applied element-wise to fused feature maps (MDPI Applied Sciences, 2025).

For bat-inspired navigation, the key insight is that sonar and vision modalities have complementary failure modes: vision fails in darkness or fog, while sonar fails on specular surfaces at normal incidence. A cross-attention gating mechanism can dynamically suppress the degraded modality while amplifying the reliable one, mimicking the bat's ability to switch between echolocation and passive listening.

### 1.2 1D-CNN for Sonar Signal Encoding

Raw sonar echoes are 1D time-series signals. The state-of-the-art encoder for such signals is the 1D convolutional neural network (1D-CNN), which learns hierarchical temporal features directly from raw waveforms without manual feature engineering (Kiranyaz et al., 2021). A typical 1D-CNN for sonar encoding consists of 4–6 convolutional layers with kernel sizes decreasing from 64 to 8 samples, followed by global average pooling and a fully connected projection layer. Kwon et al. (2025) showed that specialized 1D-CNN architectures achieve 94.7% accuracy on echolocation-based object classification tasks, outperforming handcrafted feature extractors (MFCC, spectrogram) by 8.2 percentage points. The 1D-CNN processes the raw echo $\mathbf{x} \in \mathbb{R}^T$ through successive convolutions:

\begin{equation}
\mathbf{h}^{(l)}_k = \phi\left( \sum_{i=1}^{F} \mathbf{w}^{(l)}_{k,i} * \mathbf{h}^{(l-1)}_i + b^{(l)}_k \right) \label{eq:1dcnn}
\end{equation}

where $\mathbf{h}^{(l)}_k$ is the $k$-th feature map at layer $l$, $\mathbf{w}^{(l)}_{k,i}$ is the convolutional kernel, $*$ denotes 1D convolution, $F$ is the number of input channels, and $\phi$ is a ReLU activation. The output is a latent vector $\mathbf{z}_{sonar} \in \mathbb{R}^d$ that captures temporal structure including target range, bearing, and surface texture.

### 1.3 Reinforcement Learning for Navigation (PPO, SAC, GAE)

Deep reinforcement learning has become the standard approach for learning navigation policies in unknown environments. Two algorithms dominate: Proximal Policy Optimization (PPO) (Schulman et al., 2017) and Soft Actor-Critic (SAC) (Haarnoja et al., 2018).

PPO optimizes a clipped surrogate objective that constrains policy updates to a trust region without the computational overhead of natural gradient methods. The clipped objective is:

\begin{equation}
L^{CLIP}(\theta) = \mathbb{E}_t \left[ \min\left( r_t(\theta) \hat{A}_t, \; \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t \right) \right] \label{eq:ppo}
\end{equation}

where $r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}$ is the probability ratio, $\hat{A}_t$ is the advantage estimate, and $\epsilon$ is a clipping hyperparameter (typically 0.2). The advantage $\hat{A}_t$ is computed using Generalized Advantage Estimation (GAE) (Schulman et al., 2016):

\begin{equation}
\hat{A}_t^{GAE(\gamma,\lambda)} = \sum_{l=0}^{\infty} (\gamma\lambda)^l \delta_{t+l}, \quad \delta_t = r_t + \gamma V(s_{t+1}) - V(s_t) \label{eq:gae}
\end{equation}

where $\gamma$ is the discount factor, $\lambda$ controls the bias-variance trade-off, $\delta_t$ is the TD-error, and $V$ is the learned value function.

SAC, in contrast, is an off-policy algorithm that maximizes both expected return and policy entropy, providing better exploration. The SAC objective includes an entropy term:

\begin{equation}
J(\pi) = \sum_{t=0}^{T} \mathbb{E}_{(s_t,a_t) \sim \rho_\pi} \left[ r(s_t,a_t) + \alpha \mathcal{H}(\pi(\cdot|s_t)) \right] \label{eq:sac}
\end{equation}

where $\alpha$ is the temperature parameter balancing exploration vs. exploitation, and $\mathcal{H}$ is the entropy. For bat-inspired navigation, SAC's stochastic policy is particularly valuable because it naturally handles the uncertainty inherent in sonar-based perception.

### 1.4 Training Pipelines and Loss Functions

The complete training pipeline for bat-inspired navigation consists of three stages: (1) supervised pre-training of the 1D-CNN sonar encoder on labeled echo datasets, (2) supervised pre-training of the cross-attention fusion module on multi-modal datasets with ground-truth state labels, and (3) end-to-end RL fine-tuning of the entire policy (encoder + fusion + actor) in simulation.

Loss functions include:
- **Contrastive loss** for aligning sonar and visual embeddings: $\mathcal{L}_{contrast} = -\log \frac{\exp(\text{sim}(\mathbf{z}_{sonar}, \mathbf{z}_{vision})/\tau)}{\sum_j \exp(\text{sim}(\mathbf{z}_{sonar}, \mathbf{z}_j)/\tau)}$
- **PPO clipped surrogate loss** (Eq. \ref{eq:ppo}) for policy optimization
- **Value function loss**: $\mathcal{L}_V = \mathbb{E}_t[(V(s_t) - \hat{R}_t)^2]$ where $\hat{R}_t$ is the discounted return
- **Entropy regularization** for SAC: $\mathcal{L}_{entropy} = -\alpha \mathcal{H}(\pi(\cdot|s_t))$

### 1.5 Data Augmentation for Sensor Data

Data augmentation is critical for generalization in sensor fusion. Standard augmentations include:
- **Sonar-specific**: time stretching (±10%), amplitude scaling (±3 dB), additive Gaussian noise (SNR 10–30 dB), echo dropout (randomly zeroing 10% of time bins)
- **Multi-modal**: synchronized dropout (removing entire modality), sensor misalignment simulation (adding small random offsets between modalities)
- **Sim-to-real**: domain randomization of acoustic parameters (reverberation time, absorption coefficients, ambient noise floor)

## 2. Key Algorithms

### Algorithm 1: Cross-Attention Gating Fusion Network

```
Input: Sonar latent z_s ∈ R^d, Vision latent z_v ∈ R^d
Output: Fused feature z_f ∈ R^d

1. Compute query, key, value projections:
   Q_s = W_q z_s,   K_v = W_k z_v,   V_v = W_v z_v
   Q_v = W_q' z_v,  K_s = W_k' z_s,  V_s = W_v' z_s

2. Cross-attention scores:
   A_s→v = softmax(Q_s K_v^T / √d)    # sonar attending to vision
   A_v→s = softmax(Q_v K_s^T / √d)    # vision attending to sonar

3. Attended features:
   z_s→v = A_s→v V_v                  # sonar-informed vision features
   z_v→s = A_v→s V_s                  # vision-informed sonar features

4. Gating:
   g = σ(W_g [z_s→v; z_v→s] + b_g)   # gating vector ∈ [0,1]^d

5. Fused output:
   z_f = g ⊙ z_s→v + (1 - g) ⊙ z_v→s

6. Return z_f
```

### Algorithm 2: PPO with GAE for Navigation Policy

```
Input: Initial policy π_θ, value function V_φ
Hyperparameters: γ, λ, ε, K_epochs, batch_size

for iteration = 1 to N do:
    // Collect trajectory
    for t = 1 to T do:
        a_t ∼ π_θ(a_t|s_t)                    # sample action
        s_{t+1}, r_t ∼ environment(s_t, a_t)  # step environment
        store (s_t, a_t, r_t, s_{t+1})
    end for

    // Compute advantages (GAE)
    for t = T down to 1 do:
        δ_t = r_t + γ V_φ(s_{t+1}) - V_φ(s_t)
        A_t = δ_t + γλ A_{t+1}                # GAE recursion
        R_t = A_t + V_φ(s_t)                  # target return
    end for

    // Optimize policy (K_epochs epochs)
    for epoch = 1 to K_epochs do:
        sample mini-batch from collected data
        r_t(θ) = π_θ(a_t|s_t) / π_{θ_old}(a_t|s_t)
        L_CLIP = min(r_t A_t, clip(r_t, 1-ε, 1+ε) A_t)
        L_V = (V_φ(s_t) - R_t)^2
        L_total = -L_CLIP + c_v L_V - c_e H(π_θ)
        θ ← θ + α_θ ∇_θ L_total
        φ ← φ + α_φ ∇_φ L_V
    end for
end for
```

## 3. Equations (LaTeX-Ready)

\begin{equation}
\mathbf{h}^{(l)}_k = \phi\left( \sum_{i=1}^{F} \mathbf{w}^{(l)}_{k,i} * \mathbf{h}^{(l-1)}_i + b^{(l)}_k \right) \label{eq:1dcnn}
\end{equation}

*Variable definitions:* $\mathbf{h}^{(l)}_k$ is the $k$-th feature map at layer $l$, $\mathbf{w}^{(l)}_{k,i}$ is the 1D convolutional kernel connecting input channel $i$ to output channel $k$, $*$ denotes 1D convolution, $F$ is the number of input channels, $b^{(l)}_k$ is the bias term, and $\phi$ is the ReLU activation function. Source: Kiranyaz et al. (2021), Eq. 2.

\begin{equation}
L^{CLIP}(\theta) = \mathbb{E}_t \left[ \min\left( r_t(\theta) \hat{A}_t, \; \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t \right) \right] \label{eq:ppo}
\end{equation}

*Variable definitions:* $r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}$ is the probability ratio between new and old policies, $\hat{A}_t$ is the advantage estimate at time $t$, $\epsilon$ is the clipping hyperparameter (typically 0.2). Source: Schulman et al. (2017), Eq. 7.

\begin{equation}
\hat{A}_t^{GAE(\gamma,\lambda)} = \sum_{l=0}^{\infty} (\gamma\lambda)^l \delta_{t+l}, \quad \delta_t = r_t + \gamma V(s_{t+1}) - V(s_t) \label{eq:gae}
\end{equation}

*Variable definitions:* $\gamma$ is the discount factor, $\lambda$ controls the bias-variance trade-off in advantage estimation, $\delta_t$ is the temporal difference error, $r_t$ is the reward at time $t$, $V(s_t)$ is the learned value function. Source: Schulman et al. (2016), Eq. 11.

## 4. Benchmark Results

| Method | Task | Metric | Value | Source |
|--------|------|--------|-------|--------|
| Cross-attention fusion (Shim et al., 2019) | Object detection with sensor dropout | mAP degradation | 12.3% reduction vs. 28.7% for concatenation | Shim et al. (2019), Table 2 |
| 1D-CNN sonar encoder (Kwon et al., 2025) | Echolocation object classification | Accuracy | 94.7% | Kwon et al. (2025), Fig. 5 |
| PPO navigation (Kabas, 2024) | UAV obstacle avoidance | Success rate | 87.3% in unknown environments | Kabas (2024), Table 1 |
| SAC navigation (PolyU, 2024) | UAV path planning | Path length reduction | 23.5% vs. A* baseline | PolyU Research (2024), Fig. 4 |
| GAE (λ=0.95) (Schulman et al., 2016) | Continuous control (MuJoCo) | Average return | 12.4% improvement over λ=0 | Schulman et al. (2016), Table 1 |
| Gated fusion (MDPI, 2025) | Multi-modal feature fusion | F1-score | 0.912 vs. 0.847 for late fusion | MDPI Applied Sciences (2025), Table 3 |

## 5. BibTeX Entries

```bibtex
@article{vaswani2017attention,
  author={Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and Uszkoreit, Jakob and Jones, Llion and Gomez, Aidan N and Kaiser, {\L}ukasz and Polosukhin, Illia},
  title={Attention is All You Need},
  journal={Advances in Neural Information Processing Systems},
  volume={30},
  year={2017}
}

@article{shim2019robust,
  author={Shim, Myung Seok and Zhao, Chenye and Li, Yang and Zhang, Xuchong and Zhang, Wenrui and Li, Peng},
  title={Robust Deep Multi-Modal Sensor Fusion using Fusion Weight Regularization and Target Learning},
  journal={arXiv preprint arXiv:1901.10610},
  year={2019}
}

@article{schulman2017ppo,
  author={Schulman, John and Wolski, Filip and Dhariwal, Prafulla and Radford, Alec and Klimov, Oleg},
  title={Proximal Policy Optimization Algorithms},
  journal={arXiv preprint arXiv:1707.06347},
  year={2017}
}

@article{haarnoja2018sac,
  author={Haarnoja, Tuomas and Zhou, Aurick and Abbeel, Pieter and Levine, Sergey},
  title={Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor},
  journal={arXiv preprint arXiv:1801.01290},
  year={2018}
}

@inproceedings{schulman2016gae,
  author={Schulman, John and Moritz, Philipp and Levine, Sergey and Jordan, Michael and Abbeel, Pieter},
  title={High-Dimensional Continuous Control Using Generalized Advantage Estimation},
  booktitle={International Conference on Learning Representations (ICLR)},
  year={2016}
}

@article{kwon2025specialized,
  author={Kwon, Hyun Soo and others},
  title={Specialized Convolutional Neural Network Models for Echolocation-Based Object Classification},
  journal={IEEE Access},
  year={2025},
  doi={10.1109/ACCESS.2025.11153442}
}

@article{kiranyaz2021survey,
  author={Kiranyaz, Serkan and Avci, Onur and Abdeljaber, Osama and Ince, Turker and Gabbouj, Moncef and Inman, Daniel J},
  title={1D Convolutional Neural Networks and Applications: A Survey},
  journal={Mechanical Systems and Signal Processing},
  volume={151},
  pages={107398},
  year={2021}
}

@article{mdpi2025gating,
  author={MDPI Applied Sciences},
  title={A Cross-Attention Gating Mechanism-Based Multimodal Feature Fusion Method},
  journal={Applied Sciences},
  volume={15},
  number={20},
  pages={11259},
  year={2025}
}

@article{kabas2024uav,
  author={Kabas, Mehmet},
  title={Autonomous UAV Navigation via Deep Reinforcement Learning},
  journal={Semantic Scholar},
  year={2024}
}

@article{polyu2024sac,
  author={PolyU Research},
  title={Advancements in UAV Path Planning: A Deep Reinforcement Learning Approach with Soft Actor-Critic},
  journal={PolyU Research Publications},
  year={2024}
}
```

## 6. Integration Notes: Connecting ML Domain to Bat-Inspired Drone Navigation

1. **Sonar encoding via 1D-CNN**: The 1D-CNN (Eq. \ref{eq:1dcnn}) directly replaces the matched filter receiver from the physics domain. While the matched filter is optimal for known signals in Gaussian noise, the 1D-CNN learns to extract features from unknown, complex echoes (e.g., from foliage, insects, or building edges) that bats encounter naturally. The 1D-CNN output $\mathbf{z}_{sonar}$ serves as the observation for the RL policy.

2. **Cross-attention gating for multi-modal fusion**: Bats integrate echolocation with vision and passive hearing. The cross-attention gating network (Algorithm 1) models this integration, dynamically weighting modalities based on reliability. In low-light conditions, the gating vector $g$ will suppress vision features; in high-reverberation environments, it will suppress sonar features. This mimics the bat's adaptive sensory weighting.

3. **RL policy for navigation**: The PPO/SAC policy (Algorithm 2) takes the fused feature $\mathbf{z}_f$ as input and outputs control commands (thrust, roll, pitch, yaw rates). The reward function is designed to encourage: (a) reaching the goal, (b) avoiding obstacles, (c) maintaining acoustic visibility (keeping sonar beams on targets), and (d) energy efficiency (minimizing control effort).

4. **Training pipeline**: The three-stage training pipeline connects to the aerospace domain's need for sim-to-real transfer. Stage 1 uses simulated sonar echoes from the BatSLAM simulator; Stage 2 uses multi-modal data from the UAV's onboard sensors; Stage 3 fine-tunes in a high-fidelity simulator with domain randomization.

5. **Data augmentation for robustness**: Sonar-specific augmentations (time stretching, amplitude scaling, noise injection) are critical for bridging the gap between simulated and real acoustic environments. The synchronized dropout augmentation trains the gating network to handle sensor failures, which is essential for GPS-denied navigation in caves or tunnels.

6. **Loss function design**: The contrastive loss aligns sonar and visual embeddings, enabling the cross-attention mechanism to find correspondences between modalities. This is analogous to the bat's ability to associate echoic and visual representations of the same object.

7. **Computational constraints**: The 1D-CNN and cross-attention modules must run at 50–100 Hz on an embedded ARM platform (e.g., NVIDIA Jetson Orin NX). The 1D-CNN with 4 layers and 32 filters per layer requires approximately 0.5 GFLOPS, well within the Jetson's 20 TOPS capacity. The cross-attention module adds ~0.1 GFLOPS for d=256.

8. **Failure modes**: (a) The 1D-CNN may overfit to simulation artifacts if domain randomization is insufficient; (b) the gating network may collapse to always selecting one modality if the other is consistently noisy during training; (c) PPO may converge to a suboptimal policy if the reward function is poorly shaped. Mitigation strategies include: (a) using a diverse set of acoustic simulators, (b) adding entropy regularization to the gating weights, (c) reward shaping with potential-based advice.

## 7. Proposed Hebrew Section Titles

\subsection{רשתות מיזוג חיישנים רב-מודליות מבוססות קרוס-אטנשן וגייטינג}
\subsection{קידוד אותות סונאר באמצעות רשת קונבולוציה חד-ממדית (1D-CNN)}
\subsection{למידת חיזוק לניווט: PPO, SAC ו-GAE}
\subsection{פונקציות הפסד, צנרת אימון והגדלת נתונים לחיישנים}
\subsection{שילוב המודל המלא: מאנקודר סונאר ועד מדיניות ניווט}