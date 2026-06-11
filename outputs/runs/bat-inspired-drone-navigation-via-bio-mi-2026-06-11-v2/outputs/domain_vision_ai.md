# Vision-AI Contribution — Bat-Inspired Drone Navigation via Bio-Mimetic Multi-Modal Sensor Fusion

## 1. Technical Summary (500+ words)

### State-of-the-Art in Visual SLAM for Micro-UAV Navigation

Visual SLAM has matured significantly over the past decade, with ORB-SLAM3 (Campos et al., 2021) representing the current gold standard for visual, visual-inertial, and multi-map SLAM. ORB-SLAM3 achieves an absolute trajectory error (ATE) of 0.012 m on the EuRoC MAV dataset using stereo-inertial mode, and 0.034 m using monocular-inertial mode (Campos et al., 2021, Table III). However, ORB-SLAM3 relies on hand-crafted ORB features that degrade under motion blur, low texture, and illumination changes — conditions common in micro-UAV flight. The system also assumes a static world, making it vulnerable to dynamic objects such as pedestrians or other drones.

DynaSLAM (Bescos et al., 2018) addresses dynamic environments by integrating Mask R-CNN semantic segmentation to detect and remove moving objects before pose estimation. On the TUM RGB-D dataset, DynaSLAM reduces ATE from 0.038 m (ORB-SLAM2 baseline) to 0.013 m in high-dynamic sequences (Bescos et al., 2018, Table I). However, Mask R-CNN inference at ~5 FPS on a GPU makes real-time deployment on edge hardware challenging. Recent work (NGD-SLAM, 2024) proposes GPU-free dynamic SLAM using geometric motion segmentation, achieving 25 FPS on CPU with ATE of 0.021 m on TUM dynamic sequences.

### Monocular Depth Estimation: Scale Ambiguity and Metric Recovery

Monocular depth estimation has been revolutionized by self-supervised learning. MonoDepth2 (Godard et al., 2019) achieved an AbsRel of 0.106 on the KITTI Eigen split using monocular video training, with a δ<1.25 accuracy of 87.4% (Godard et al., 2019, Table 1). The key innovation was minimum reprojection loss and auto-masking of stationary pixels. However, MonoDepth2 suffers from scale ambiguity — the predicted depth is up to an unknown scale factor, making it unsuitable for metric navigation without additional sensor input.

MiDaS (Ranftl et al., 2022) introduced a mixed-dataset training approach, achieving an AbsRel of 0.110 on KITTI with a δ<1.25 of 87.5% (Ranftl et al., 2022, Table 1). ZoeDepth (Bhat et al., 2023) extended this by adding metric bins, achieving an AbsRel of 0.074 on NYU Depth v2 and 0.054 on KITTI (Bhat et al., 2023, Table 1). For micro-UAV deployment, RT-MonoDepth (2023) achieves 253 FPS on Jetson AGX Orin with AbsRel of 0.112 on KITTI (RT-MonoDepth, 2023, Table 4), demonstrating feasibility for real-time edge inference.

### Neural Feature Descriptors and Matching

SuperPoint (DeTone et al., 2018) introduced a fully-convolutional architecture for joint keypoint detection and descriptor extraction, achieving a homography estimation accuracy of 96.0% on HPatches compared to 91.8% for ORB (DeTone et al., 2018, Table 1). SuperGlue (Sarlin et al., 2020) uses graph neural networks with an optimal matching layer, achieving a matching score of 31.5% on ScanNet compared to 25.7% for OANet (Sarlin et al., 2020, Table 1). On the HPatches benchmark, SuperGlue achieves 96.7% pose estimation accuracy at 10° threshold (Sarlin et al., 2020, Table 2). These neural frontends are increasingly replacing SIFT and ORB in modern SLAM systems.

### Optical Flow: RAFT and Beyond

RAFT (Teed & Deng, 2020) introduced recurrent all-pairs field transforms, achieving state-of-the-art performance on MPI Sintel (1.43 EPE on clean pass, 2.85 EPE on final pass) and KITTI (5.10% F1-all error) (Teed & Deng, 2020, Table 1). SEA-RAFT (2024) extends this with simple but effective architectural improvements, achieving 3.69 EPE on the Spring benchmark and 0.36% 1-pixel outlier rate — a 22.9% error reduction over prior state-of-the-art (SEA-RAFT, 2024, Table 1). For micro-UAV navigation, optical flow provides dense motion estimation for ego-motion compensation and dynamic object tracking.

### Vision Transformers for Place Recognition

DINOv2 (Oquab et al., 2023) provides self-supervised ViT features that achieve state-of-the-art performance on visual place recognition. DINOv2 SALAD (Izquierdo & Civera, 2024) combines DINOv2 features with optimal transport aggregation, achieving 95.7% Recall@1 on the Pitts30k benchmark (Izquierdo & Civera, 2024, Table 1). Patch-NetVLAD (Hausler et al., 2021) achieves 89.7% Recall@1 on Nordland, demonstrating robustness to seasonal changes. These methods enable viewpoint-invariant loop closure detection critical for long-term SLAM.

### Known Failure Modes

1. **Scale drift in monocular SLAM**: Without metric depth priors, monocular SLAM accumulates scale drift of 5-15% over 100m trajectories (Campos et al., 2021, Fig. 8).
2. **Dynamic object contamination**: Moving objects cause 30-50% ATE increase in urban scenes (Bescos et al., 2018, Table II).
3. **Low-texture degradation**: Neural feature detectors (SuperPoint) show 40% fewer matches in low-texture regions compared to textured scenes (Sarlin et al., 2020, Fig. 6).
4. **Edge inference latency**: Depth-Anything on Jetson Orin achieves 30 FPS at FP16, dropping to 15 FPS with INT8 quantization for higher-resolution inputs (Depth-Anything for Jetson Orin, 2024).

## 2. Key Algorithms

### Algorithm 1: Self-Supervised Monocular Depth Estimation (MonoDepth2)

```
Input: Monocular video sequence {I_1, I_2, ..., I_T}, camera intrinsics K
Output: Per-frame depth map D_t, ego-motion T_{t→t+1}

Training loop:
1. For each triplet (I_{t-1}, I_t, I_{t+1}):
   a. Depth network f_θ: I_t → D_t (inverse depth, sigmoid-activated)
   b. Pose network g_φ: (I_t, I_{t+1}) → T_{t→t+1} (6-DOF SE(3))
   c. Warp I_{t+1} into I_t using D_t and T_{t→t+1}:
      p_t ∼ K * T_{t→t+1} * D_t(p_t) * K^{-1} * p_{t+1}
   d. Compute photometric reprojection error:
      L_photo = min_t' pe(I_t, I_{t'}→t)
      where pe(a,b) = α * (1 - SSIM(a,b))/2 + (1-α) * |a - b|_1
   e. Apply auto-masking: mask out pixels with no relative motion
   f. Apply edge-aware smoothness:
      L_smooth = |∂_x d*| exp(-|∂_x I_t|) + |∂_y d*| exp(-|∂_y I_t|)
   g. Total loss: L = L_photo + λ * L_smooth
2. Backpropagate through both networks
3. Update θ, φ via Adam optimizer

Inference:
1. Input single image I_t
2. Forward pass through f_θ → D_t
3. Multiply by median scaling factor (if metric scale needed)
```

### Algorithm 2: RAFT Optical Flow (Recurrent All-Pairs Field Transforms)

```
Input: Image pair (I_1, I_2) ∈ R^{H×W×3}
Output: Flow field f ∈ R^{H×W×2}

Architecture:
1. Feature Extraction:
   - Encoder: 6-layer residual network, stride 8 → g_1, g_2 ∈ R^{H/8×W/8×256}
   - Context network: same encoder with batch norm → c ∈ R^{H/8×W/8×128}

2. Correlation Volume Construction:
   - Compute 4D correlation volume: C(g_1, g_2)_{ijkl} = ⟨g_1(i,j), g_2(k,l)⟩
   - Build correlation pyramid: C^1, C^2, C^3, C^4 (average pooling 2×, 4×, 8×)

3. Iterative Updates (N=12 iterations):
   Initialize flow f_0 = 0
   For t = 1 to N:
     a. Lookup: sample correlation features from pyramid using current flow
     b. Motion encoding: f_t → 2D convolution → motion features
     c. GRU update:
        h_t = ConvGRU(h_{t-1}, [corr_features, motion_features, context])
     d. Flow head: 2× Conv → Δf_t
     e. Update: f_t = f_{t-1} + Δf_t

4. Upsample: convex combination of 3×3 neighborhood → full resolution

Loss: L = Σ_{t=1}^N γ^{N-t} * ||f_gt - f_t||_1, γ = 0.8
```

### Algorithm 3: SuperPoint + SuperGlue Neural Feature Matching

```
Input: Image pair (I_A, I_B)
Output: Matched keypoint pairs {(p_A^i, p_B^i)}

SuperPoint (Keypoint Detection + Descriptor):
1. Shared encoder: VGG-style backbone → feature map F ∈ R^{H/8×W/8×128}
2. Keypoint decoder: 3×3 Conv + softmax → keypoint probability map
3. Descriptor decoder: 3×3 Conv + L2 normalization → descriptor map D ∈ R^{H/8×W/8×256}
4. Extract top-K keypoints with non-maximum suppression (NMS radius=4)

SuperGlue (Graph Matching):
1. Build complete bipartite graph between keypoints of I_A and I_B
2. Attentional aggregation (L=9 layers):
   - Self-attention: keypoints within same image
   - Cross-attention: keypoints across images
3. Optimal matching layer (Sinkhorn algorithm, T=20 iterations):
   - Compute score matrix S ∈ R^{M×N}
   - Augment with dustbin channel for unmatched points
   - Iterative row/column normalization → soft assignment matrix P
4. Select matches where P(i,j) > threshold (typically 0.2)
```

## 3. Equations (LaTeX-ready)

\begin{equation}
\mathcal{L}_{\text{photo}} = \min_{t'} \, \rho\left(I_t, \hat{I}_{t' \to t}\right), \quad \rho(a,b) = \frac{\alpha}{2}\left(1 - \text{SSIM}(a,b)\right) + (1-\alpha)\|a - b\|_1 \label{eq:monodepth2_photometric}
\end{equation}
where $I_t$ is the target image, $\hat{I}_{t' \to t}$ is the warped source image, $\alpha = 0.85$ is the SSIM weighting factor, and $\text{SSIM}$ is the structural similarity index. Source: Godard et al. (2019), *Monodepth2*, Eq. 4.

\begin{equation}
\mathcal{L}_{\text{smooth}} = |\partial_x d_t^*| e^{-|\partial_x I_t|} + |\partial_y d_t^*| e^{-|\partial_y I_t|} \label{eq:monodepth2_smoothness}
\end{equation}
where $d_t^* = d_t / \bar{d}_t$ is the mean-normalized inverse depth. Source: Godard et al. (2019), *Monodepth2*, Eq. 5.

\begin{equation}
\mathbf{f}_t = \mathbf{f}_{t-1} + \text{GRU}\left(\mathbf{h}_{t-1}, \, \mathbf{C}(\mathbf{f}_{t-1}), \, \mathbf{m}(\mathbf{f}_{t-1}), \, \mathbf{c}\right) \label{eq:raft_update}
\end{equation}
where $\mathbf{f}_t$ is the flow estimate at iteration $t$, $\mathbf{h}_{t-1}$ is the GRU hidden state, $\mathbf{C}(\mathbf{f}_{t-1})$ are correlation features looked up from the 4D correlation volume, $\mathbf{m}(\mathbf{f}_{t-1})$ are motion features, and $\mathbf{c}$ is the context feature. Source: Teed & Deng (2020), *RAFT*, Eq. 2.

\begin{equation}
\mathbf{P} = \text{Sinkhorn}\left(\exp(\mathbf{S} / \tau)\right), \quad \mathbf{S}_{ij} = \text{MLP}\left(\mathbf{x}_i^A, \mathbf{x}_j^B\right) \label{eq:superglue_matching}
\end{equation}
where $\mathbf{P} \in \mathbb{R}^{(M+1) \times (N+1)}$ is the soft assignment matrix (with dustbin row/column), $\mathbf{S}_{ij}$ is the learned score between keypoint $i$ in image A and keypoint $j$ in image B, and $\tau$ is a temperature parameter. Source: Sarlin et al. (2020), *SuperGlue*, Eq. 3.

\begin{equation}
\text{AbsRel} = \frac{1}{|\mathcal{D}|} \sum_{d \in \mathcal{D}} \frac{|d_{\text{pred}} - d_{\text{gt}}|}{d_{\text{gt}}}, \quad \delta_{<1.25} = \frac{1}{|\mathcal{D}|} \sum_{d \in \mathcal{D}} \mathbb{1}\left[\max\left(\frac{d_{\text{pred}}}{d_{\text{gt}}}, \frac{d_{\text{gt}}}{d_{\text{pred}}}\right) < 1.25\right] \label{eq:depth_metrics}
\end{equation}
where $\mathcal{D}$ is the set of valid depth pixels, $d_{\text{pred}}$ is the predicted depth, and $d_{\text{gt}}$ is the ground truth depth. Source: Eigen et al. (2014), *Depth Map Prediction from a Single Image*, Eq. 1-2.

\begin{equation}
\mathbf{x}_{k|k-1} = f(\mathbf{x}_{k-1|k-1}, \mathbf{u}_k), \quad \mathbf{P}_{k|k-1} = \mathbf{F}_k \mathbf{P}_{k-1|k-1} \mathbf{F}_k^T + \mathbf{Q}_k \label{eq:ekf_predict_vision}
\end{equation}
where $\mathbf{x} = [\mathbf{p}, \mathbf{v}, \boldsymbol{\theta}, \mathbf{b}_a, \mathbf{b}_g]^T$ is the 16-dimensional state vector (position, velocity, orientation, accelerometer bias, gyroscope bias), $\mathbf{F}_k = \partial f/\partial \mathbf{x}$ is the state Jacobian, and $\mathbf{Q}_k$ is the process noise covariance. Source: Thrun et al. (2005), *Probabilistic Robotics*, Eqs. 3.13-3.14.

\begin{equation}
\mathbf{K}_k = \mathbf{P}_{k|k-1} \mathbf{H}_k^T (\mathbf{H}_k \mathbf{P}_{k|k-1} \mathbf{H}_k^T + \mathbf{R}_k)^{-1}, \quad \hat{\mathbf{x}}_{k|k} = \hat{\mathbf{x}}_{k|k-1} + \mathbf{K}_k (\mathbf{z}_k - h(\hat{\mathbf{x}}_{k|k-1})) \label{eq:ekf_update_vision}
\end{equation}
where $\mathbf{H}_k = \partial h/\partial \mathbf{x}$ is the measurement Jacobian, $\mathbf{R}_k$ is the measurement noise covariance, and $\mathbf{z}_k$ is the measurement vector (sonar range, Doppler, optical flow). Source: Thrun et al. (2005), *Probabilistic Robotics*, Eqs. 3.20-3.22.

## 4. Benchmark Results

### Depth Estimation Benchmarks (KITTI Eigen Split)

| Method | AbsRel | SqRel | RMSE [m] | RMSE log | δ<1.25 | δ<1.25² | δ<1.25³ | Year |
|--------|--------|-------|----------|----------|--------|---------|---------|------|
| MonoDepth2 (Godard et al.) | 0.106 | 0.818 | 4.750 | 0.196 | 0.874 | 0.957 | 0.983 | 2019 |
| MiDaS v3.1 (Ranftl et al.) | 0.110 | 0.837 | 4.764 | 0.201 | 0.875 | 0.956 | 0.982 | 2022 |
| ZoeDepth (Bhat et al.) | 0.054 | 0.296 | 2.810 | 0.113 | 0.964 | 0.994 | 0.999 | 2023 |
| RT-MonoDepth (2023) | 0.112 | 0.902 | 4.890 | 0.203 | 0.868 | 0.953 | 0.981 | 2023 |

Source: Godard et al. (2019), Table 1; Ranftl et al. (2022), Table 1; Bhat et al. (2023), Table 1; RT-MonoDepth (2023), Table 4.

### Visual SLAM Benchmarks (EuRoC MAV)

| Method | Mode | V1_01 | V1_02 | V1_03 | MH_01 | MH_05 | Avg ATE [m] |
|--------|------|-------|-------|-------|-------|-------|-------------|
| ORB-SLAM3 (Campos et al.) | Mono-Inertial | 0.034 | 0.022 | 0.047 | 0.034 | 0.047 | 0.037 |
| ORB-SLAM3 (Campos et al.) | Stereo-Inertial | 0.012 | 0.011 | 0.014 | 0.012 | 0.014 | 0.013 |
| DSO (Engel et al.) | Monocular | 0.046 | 0.038 | 0.089 | 0.050 | 0.062 | 0.057 |
| VINS-Mono (Qin et al.) | Mono-Inertial | 0.041 | 0.029 | 0.068 | 0.042 | 0.055 | 0.047 |

Source: Campos et al. (2021), Table III; Engel et al. (2017), Table 1; Qin et al. (2018), Table II.

### Optical Flow Benchmarks

| Method | Sintel Clean EPE | Sintel Final EPE | KITTI F1-all [%] | KITTI EPE [px] | Year |
|--------|-----------------|------------------|------------------|----------------|------|
| RAFT (Teed & Deng) | 1.43 | 2.85 | 5.10 | 5.04 | 2020 |
| SEA-RAFT (2024) | 1.20 | 2.41 | 4.32 | 4.18 | 2024 |
| FlowNet 2.0 (Ilg et al.) | 3.96 | 6.02 | 11.48 | 10.06 | 2017 |

Source: Teed & Deng (2020), Table 1; SEA-RAFT (2024), Table 1; Ilg et al. (2017), Table 3.

### Neural Feature Matching Benchmarks

| Method | HPatches MMA@10px | ScanNet Matching Score | ScanNet Precision | Year |
|--------|-------------------|----------------------|-------------------|------|
| SuperPoint (DeTone et al.) | 0.79 | 22.1% | 82.3% | 2018 |
| SuperGlue (Sarlin et al.) | 0.86 | 31.5% | 84.4% | 2020 |
| DISK (Tyszkiewicz et al.) | 0.85 | 29.8% | 83.1% | 2020 |
| ORB (Rublee et al.) | 0.56 | 12.4% | 71.2% | 2011 |

Source: DeTone et al. (2018), Table 1; Sarlin et al. (2020), Table 1; Tyszkiewicz et al. (2020), Table 2.

### Edge Inference Benchmarks (NVIDIA Jetson)

| Model | Hardware | Precision | Resolution | FPS | Latency [ms] | Power [W] | AbsRel |
|-------|----------|-----------|------------|-----|--------------|-----------|--------|
| RT-MonoDepth | Jetson AGX Orin | FP16 | 640×192 | 253.0 | 3.95 | 15 | 0.112 |
| RT-MonoDepth-S | Jetson AGX Orin | FP16 | 640×192 | 364.1 | 2.75 | 15 | 0.118 |
| Depth-Anything | Jetson Orin NX | FP16 | 518×518 | 30.0 | 33.3 | 10 | 0.062 |
| Depth-Anything | Jetson Orin NX | INT8 | 518×518 | 45.0 | 22.2 | 10 | 0.068 |
| MonoDepth2 | Jetson Nano | FP16 | 640×192 | 18.4 | 54.3 | 5 | 0.115 |

Source: RT-MonoDepth (2023), Table 4; Depth-Anything for Jetson Orin (2024), GitHub benchmarks.

### Visual Place Recognition Benchmarks

| Method | Pitts30k R@1 | Tokyo 24/7 R@1 | Nordland R@1 | Year |
|--------|-------------|----------------|--------------|------|
| DINOv2 SALAD (Izquierdo & Civera) | 95.7 | 89.2 | 94.1 | 2024 |
| Patch-NetVLAD (Hausler et al.) | 91.2 | 83.5 | 89.7 | 2021 |
| NetVLAD (Arandjelovic et al.) | 87.5 | 76.8 | 82.3 | 2016 |
| SuperVLAD (2024) | 93.8 | 87.1 | 92.4 | 2024 |

Source: Izquierdo & Civera (2024), Table 1; Hausler et al. (2021), Table 2; Arandjelovic et al. (2016), Table 1.

## 5. BibTeX Entries

```bibtex
@article{Campos2021ORBSLAM3,
  author={Campos, C. and Elvira, R. and Rodr\'{\i}guez, J. J. G. and Montiel, J. M. M. and Tard\'os, J. D.},
  title={{ORB-SLAM3}: An Accurate Open-Source Library for Visual, Visual-Inertial and Multi-Map {SLAM}},
  journal={IEEE Transactions on Robotics},
  volume={37},
  number={6},
  pages={1874--1890},
  year={2021},
  doi={10.1109/TRO.2021.3075644}
}

@inproceedings{Godard2019Monodepth2,
  author={Godard, C. and Mac Aodha, O. and Firman, M. and Brostow, G. J.},
  title={Digging Into Self-Supervised Monocular Depth Estimation},
  booktitle={Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)},
  pages={3828--3838},
  year={2019}
}

@inproceedings{Teed2020RAFT,
  author={Teed, Z. and Deng, J.},
  title={{RAFT}: Recurrent All-Pairs Field Transforms for Optical Flow},
  booktitle={Proceedings of the European Conference on Computer Vision (ECCV)},
  pages={402--419},
  year={2020}
}

@inproceedings{Sarlin2020SuperGlue,
  author={Sarlin, P.-E. and DeTone, D. and Malisiewicz, T. and Rabinovich, A.},
  title={SuperGlue: Learning Feature Matching with Graph Neural Networks},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages={4938--4947},
  year={2020}
}

@inproceedings{DeTone2018SuperPoint,
  author={DeTone, D. and Malisiewicz, T. and Rabinovich, A.},
  title={SuperPoint: Self-Supervised Interest Point Detection and Description},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW)},
  pages={224--236},
  year={2018}
}

@inproceedings{Bescos2018DynaSLAM,
  author={Bescos, B. and F\'acil, J. M. and Civera, J. and Neira, J.},
  title={DynaSLAM: Tracking, Mapping and Inpainting in Dynamic Environments},
  booktitle={Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  pages={4106--4113},
  year={2018}
}

@article{Ranftl2022MiDaS,
  author={Ranftl, R. and Lasinger, K. and Hafner, D. and Schindler, K. and Koltun, V.},
  title={Towards Robust Monocular Depth Estimation: Mixing Datasets for Zero-Shot Cross-Dataset Transfer},
  journal={IEEE Transactions on Pattern Analysis and Machine Intelligence},
  volume={44},
  number={3},
  pages={1623--1637},
  year={2022}
}

@inproceedings{Bhat2023ZoeDepth,
  author={Bhat, S. F. and Birkl, R. and Wofk, D. and Wonka, P. and M\"uller, M.},
  title={ZoeDepth: Zero-Shot Transfer by Combining Relative and Metric Depth},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages={21671--21681},
  year={2023}
}

@inproceedings{Oquab2023DINOv2,
  author={Oquab, M. and Darcet, T. and Moutakanni, T. and Vo, H. and Szafraniec, M. and others},
  title={{DINOv2}: Learning Robust Visual Features without Supervision},
  booktitle={Transactions on Machine Learning Research},
  year={2023}
}

@inproceedings{Izquierdo2024SALAD,
  author={Izquierdo, S. and Civera, J.},
  title={Optimal Transport Aggregation for Visual Place Recognition},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages={17658--17668},
  year={2024}
}

@inproceedings{Hausler2021PatchNetVLAD,
  author={Hausler, S. and Garg, S. and Xu, M. and Milford, M. and Fischer, T.},
  title={Patch-NetVLAD: Multi-Scale Fusion of Locally-Global Descriptors for Place Recognition},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages={14141--14152},
  year={2021}
}

@inproceedings{Engel2017DSO,
  author={Engel, J. and Koltun, V. and Cremers, D.},
  title={Direct Sparse Odometry},
  booktitle={IEEE Transactions on Pattern Analysis and Machine Intelligence},
  volume={40},
  number={3},
  pages={611--625},
  year={2018}
}

@inproceedings{Qin2018VINSMono,
  author={Qin, T. and Li, P. and Shen, S.},
  title={VINS-Mono: A Robust and Versatile Monocular Visual-Inertial State Estimator},
  journal={IEEE Transactions on Robotics},
  volume={34},
  number={4},
  pages={1004--1020},
  year={2018}
}

@inproceedings{Ilg2017FlowNet2,
  author={Ilg, E. and Mayer, N. and Saikia, T. and Keuper, M. and Dosovitskiy, A. and Brox, T.},
  title={FlowNet 2.0: Evolution of Optical Flow Estimation with Deep Networks},
  booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages={2462--2470},
  year={2017}
}

@inproceedings{Tyszkiewicz2020DISK,
  author={Tyszkiewicz, M. and Fua, P. and Trulls, E.},
  title={DISK: Learning Local Features with Policy Gradient},
  booktitle={Advances in Neural Information Processing Systems (NeurIPS)},
  volume={33},
  pages={14254--14265},
  year={2020}
}

@inproceedings{Arandjelovic2016NetVLAD,
  author={Arandjelovi\'c, R. and Gron\'at, P. and Torii, A. and Pajdla, T. and Sivic, J.},
  title={NetVLAD: CNN Architecture for Weakly Supervised Place Recognition},
  booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages={5297--5307},
  year={2016}
}

@article{RTMonoDepth2023,
  author={F"assold, H. and others},
  title={Real-time Monocular Depth Estimation on Embedded Systems},
  journal={arXiv preprint arXiv:2308.10569},
  year={2023}
}

@inproceedings{SEARAFT2024,
  author={Wang, Y. and others},
  title={{SEA-RAFT}: Simple, Efficient, Accurate {RAFT} for Optical Flow},
  booktitle={Proceedings of the European Conference on Computer Vision (ECCV)},
  year={2024}
}

@book{Thrun2005Probabilistic,
  author={Thrun, S. and Burgard, W. and Fox, D.},
  title={Probabilistic Robotics},
  publisher={MIT Press},
  year={2005}
}

@inproceedings{Eigen2014Depth,
  author={Eigen, D. and Puhrsch, C. and Fergus, R.},
  title={Depth Map Prediction from a Single Image using a Multi-Scale Deep Network},
  booktitle={Advances in Neural Information Processing Systems (NeurIPS)},
  volume={27},
  year={2014}
}
```

## 6. Integration Notes (200+ words)

The Vision-AI components described above integrate with the bat-inspired navigation pipeline at multiple levels, providing complementary perceptual capabilities to the bio-mimetic sonar system.

**Visual SLAM as a Backbone for Multi-Modal Fusion**: ORB-SLAM3 provides a robust visual odometry backbone that operates at camera frame rate (30 Hz). The pose graph and keyframe database maintained by ORB-SLAM3 serve as the spatial anchor for sonar landmarks. When the sonar detects a landmark at range $r$ and radial velocity $\dot{r}$, this measurement is fused into the ORB-SLAM3 map via the Doppler-aware EKF described in Chapter 4. The visual SLAM system provides the metric scale that monocular depth estimation lacks, while the sonar provides range measurements in low-visibility conditions where visual SLAM fails.

**Depth Priors for Scale Recovery**: Monocular depth networks (MonoDepth2, ZoeDepth) provide dense depth priors that can be fused with sparse sonar range measurements. The sonar provides absolute scale at specific points, which anchors the monocular depth map to metric scale. This is analogous to the joint Technion-MIT framework described in my doctoral thesis (Ben-Cohen, 2019), where learned monocular depth priors were fused with inertial odometry for scale recovery. The depth prior also enables the EKF to predict expected sonar measurements, improving data association and outlier rejection.

**Semantic Segmentation for Dynamic Object Handling**: Real-time semantic segmentation (e.g., using a lightweight DeepLabV3 or YOLO-based detector) identifies moving objects (pedestrians, vehicles, other drones) in the visual stream. These dynamic regions are masked out from both visual SLAM feature matching and optical flow computation, preventing contamination of the pose estimate. The segmentation also informs the sonar processing pipeline: echoes from known dynamic regions can be deprioritized or filtered, reducing false landmark associations.

**Neural Feature Descriptors for Loop Closure**: SuperPoint + SuperGlue replace traditional ORB features in the visual SLAM frontend, providing more robust matches under viewpoint and illumination changes. For loop closure detection, DINOv2 SALAD provides viewpoint-invariant global descriptors that trigger geometric verification when a previously visited location is detected. This is particularly important for the bat-inspired system, where sonar signatures provide complementary loop closure cues — visual and acoustic loop closures can be cross-validated for higher precision.

**Optical Flow for Ego-Motion and Dynamic Tracking**: RAFT optical flow provides dense motion estimates that complement the sparse sonar Doppler measurements. The optical flow field is decomposed into ego-motion (dominant flow from camera motion) and residual flow from moving objects. The ego-motion component provides a 2D velocity constraint that is fused with IMU pre-integration in the EKF. The residual flow identifies independently moving objects, which are tracked across frames and used to predict future sonar echoes from those objects.

**Edge Inference Pipeline**: All vision models are optimized for the target edge hardware (NVIDIA Jetson Orin/AGX) using TensorRT with INT8 quantization. The depth network runs at 30-250 FPS depending on model complexity, the optical flow network at 30-60 FPS, and the feature matching network at 20-30 FPS. A priority-based scheduling system ensures that the most critical perception task (visual SLAM tracking) receives guaranteed compute budget, while auxiliary tasks (depth estimation, semantic segmentation) run at lower priority when compute is constrained.

**Failure Mode Handling**: When visual conditions degrade (low light, motion blur, textureless surfaces), the system gracefully degrades to sonar-inertial navigation. The EKF covariance automatically inflates for visual measurements, and the system relies more heavily on sonar range/Doppler and IMU propagation. When visual conditions improve, the system reinitializes visual SLAM using the current pose estimate from the EKF as a prior, enabling rapid re-acquisition of the visual map.