# Paper Outline: Octopus-Inspired Soft Robotic Drone Navigation Using Bio-Mimetic SLAM

**Target Length:** 25–30 pages (IEEE double-column format)
**Primary Venue:** IEEE Transactions on Robotics
**Lead Author:** Dr. Yael Cohen (D.Sc., Technion)

---

## Chapter 1: מבוא — Introduction
**Hebrew Title:** \section{מבוא: ניווט רחפן רובוטי רך בהשראת תמנון תוך שימוש ב-SLAM ביומימטי}
**Target Pages:** 3–4

### Subsections:
1. \subsection{רקע מוטיבציוני — אתגרי ניווט תת-ימי לרובוטים רכים}
2. \subsection{השראה ביולוגית ממערכת העצבים המבוזרת של התמנון}
3. \subsection{תרומות עיקריות של המאמר}
4. \subsection{מבנה המאמר ומפת דרכים}

### Key Equations:
- General SLAM formulation: $p(\mathbf{x}_{1:k}, \mathbf{m} \mid \mathbf{z}_{1:k}, \mathbf{u}_{1:k}) \propto p(\mathbf{x}_0) \prod_{t=1}^{k} p(\mathbf{x}_t \mid \mathbf{x}_{t-1}, \mathbf{u}_t) \prod_{t=1}^{k} p(\mathbf{z}_t \mid \mathbf{x}_t, \mathbf{m})$
- Bio-mimetic sensing likelihood: $\mathcal{L}_{\text{bio}}(\mathbf{z}_t \mid \mathbf{x}_t, \mathbf{m}) = \prod_{i=1}^{N_s} \mathcal{N}(\mathbf{z}_{t,i} \mid h_i(\mathbf{x}_t, \mathbf{m}), \Sigma_i)$
- Soft robot state transition: $\mathbf{x}_{t+1} = f_{\text{soft}}(\mathbf{x}_t, \mathbf{u}_t, \boldsymbol{\kappa}_t) + \mathbf{w}_t, \quad \mathbf{w}_t \sim \mathcal{N}(0, Q_t)$

### Figures:
- `fig_octopus_biological_inspiration.png`: Diagram of octopus nervous system (central brain + 8 arm ganglia) mapped to distributed SLAM architecture
- `fig_system_overview.png`: High-level system block diagram showing soft drone, sensor suite, and SLAM pipeline

### Table:
- **Table 1.1:** Comparison of bio-inspired SLAM approaches (octopus vs. insect vs. mammal vs. fish-inspired)

### Search Keywords:
- "octopus nervous system distributed control soft robot"
- "underwater SLAM soft robot navigation"
- "bio-mimetic SLAM survey"
- "soft drone state estimation"

### Primary Sources:
- [1] Nature 2026: "Peripheral control enabled by distributed sensing in an octopus-inspired soft robotic arm"
- [2] Dellaert & Kaess, "Factor Graphs for Robot Perception", Foundations and Trends in Robotics, 2017
- [3] Rus & Tolley, "Design, fabrication and control of soft robots", Nature, 2015

---

## Chapter 2: מודל קינמטי ודינמי של רחפן רך רב-זרועי — Kinematic and Dynamic Model of a Multi-Arm Soft Drone
**Hebrew Title:** \section{מודל קינמטי ודינמי של רחפן רך רב-זרועי בהשראת זרועות התמנון}
**Target Pages:** 3–4

### Subsections:
1. \subsection{קינמטיקה של רובוט רציף — מודל מקוטע למקטעים מתעקמים}
2. \subsection{דינמיקה מבוססת אלמנטים סופיים לרובוט רך}
3. \subsection{מודל הנעה הידרודינמית — כוחות גרר ודחף בזרועות גמישות}

### Key Equations:
- Piecewise constant curvature (PCC) kinematics for a single arm segment:
  $\mathbf{T}_i(\kappa_i, \phi_i, l_i) = \begin{bmatrix} \mathbf{R}_i(\kappa_i, \phi_i) & \mathbf{p}_i(\kappa_i, \phi_i, l_i) \\ \mathbf{0}^T & 1 \end{bmatrix}$
  where $\kappa_i = 1/r_i$ is curvature, $\phi_i$ is bending plane angle, $l_i$ is arc length
- Forward kinematics of $N$ arms: $\mathbf{T}_{\text{drone}} = \prod_{j=1}^{N} \prod_{i=1}^{M_j} \mathbf{T}_{j,i}(\kappa_{j,i}, \phi_{j,i}, l_{j,i})$
- Hydrodynamic drag on a soft arm segment: $\mathbf{F}_{\text{drag},i} = -\frac{1}{2} \rho C_d A_i \|\mathbf{v}_{\perp,i}\| \mathbf{v}_{\perp,i}$
- Euler-Lagrange dynamics with soft constraints: $\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{\mathbf{q}}}\right) - \frac{\partial L}{\partial \mathbf{q}} + \frac{\partial \mathcal{D}}{\partial \dot{\mathbf{q}}} = \boldsymbol{\tau}_{\text{muscle}} + \boldsymbol{\tau}_{\text{hydro}}$

### Figures:
- `fig_soft_arm_kinematics.png`: PCC model illustration showing curvature $\kappa$, bending plane $\phi$, and arc length $l$ for a single continuum arm segment
- `fig_multi_arm_drone_model.png`: CAD model of the 6-arm soft drone with coordinate frames

### Table:
- **Table 2.1:** Comparison of continuum robot kinematic models (PCC vs. Cosserat rod vs. FEM vs. learned)

### Search Keywords:
- "continuum robot kinematics piecewise constant curvature"
- "soft robot dynamics Cosserat rod model"
- "hydrodynamic modeling soft underwater robot"
- "multi-arm soft drone kinematics"

### Primary Sources:
- [4] Webster & Jones, "Design and Kinematic Modeling of Constant Curvature Continuum Robots", IJRR, 2010
- [5] Renda et al., "Dynamic model of a soft-bodied manipulator", Soft Robotics, 2018
- [6] Jones & Walker, "Kinematics for multisection continuum robots", IEEE TRO, 2006

---

## Chapter 3: חישת מישוש מבוזרת בהשראת כפתורי היניקה של התמנון — Distributed Tactile Sensing Inspired by Octopus Suckers
**Hebrew Title:** \section{חישת מישוש מבוזרת בהשראת כפתורי היניקה של התמנון לניווט בסביבות מוגבלות}
**Target Pages:** 3–4

### Subsections:
1. \subsection{ארכיטקטורת חיישני מישוש מבוזרים — מערך לחץ קיבולי על גבי הרחפן}
2. \subsection{מודל חישה רב-מודאלי — מיזוג מישוש, לחץ הידרוסטטי ועקמומיות}
3. \subsection{הערכת מצב גוף באמצעות חישה פרופריוצפטיבית מוטבעת}

### Key Equations:
- Capacitive tactile sensor model: $C_{ij} = \varepsilon_0 \varepsilon_r \frac{A_{ij}}{d_0 - \Delta d_{ij}(F_{ij})}$
- Curvature estimation from embedded Hall-effect sensors: $\kappa_i = \frac{2}{L} \arctan\left(\frac{B_{x,i}}{B_{z,i}}\right)$
- Multi-modal observation model: $\mathbf{z}_t^{\text{tactile}} = \begin{bmatrix} \mathbf{C}_t \\ \boldsymbol{\kappa}_t \\ P_t^{\text{hydro}} \end{bmatrix} = h_{\text{tactile}}(\mathbf{x}_t, \mathbf{m}) + \mathbf{v}_t$
- Contact detection likelihood: $P(\text{contact} \mid \mathbf{z}_t) = \sigma\left( \mathbf{w}^T \mathbf{z}_t^{\text{tactile}} + b \right)$

### Figures:
- `fig_tactile_sensor_array.png`: Layout of distributed capacitive tactile sensors on soft drone arms (16 sensors per arm, 96 total)
- `fig_curvature_sensing.png`: Hall-effect curvature sensor cross-section and calibration curve

### Table:
- **Table 3.1:** Sensor specifications (type, range, resolution, sampling rate, power consumption)

### Search Keywords:
- "soft tactile sensor array capacitive pressure"
- "embedded curvature sensor soft robot proprioception"
- "octopus sucker tactile sensing biomimetic"
- "distributed sensing soft continuum robot"

### Primary Sources:
- [7] Ozel et al., "A precise embedded curvature sensor module for soft-bodied robots", Sensors & Actuators A, 2015
- [8] Shih et al., "Electronic skins and machine learning for intelligent soft robots", Science Advances, 2020
- [9] Mazzolai & Laschi, "A blueprint for a soft robot: From octopus to soft robotics", Bioinspiration & Biomimetics, 2020

---

## Chapter 4: מיזוג חיישנים רב-מודאלי — אקוסטי, חזותי ומישוש — Multi-Modal Sensor Fusion: Acoustic, Visual, and Tactile
**Hebrew Title:** \section{מיזוג חיישנים רב-מודאלי לניווט תת-ימי: שילוב סונאר, מצלמה וחיישני מישוש}
**Target Pages:** 3–4

### Subsections:
1. \subsection{מודל חישת סונאר בתדר גבוה למיפוי סביבה תת-ימית}
2. \subsection{ראייה סטריאוסקופית בתנאי ראות מוגבלים}
3. \subsection{מיזוג הטרוגני מבוסס אי-ודאות — גישת פילטר חלקיקים מותאמת}

### Key Equations:
- Sonar range measurement model: $z_t^{\text{sonar}} = \|\mathbf{p}_t - \mathbf{p}_{\text{obs}}\| + \eta_t, \quad \eta_t \sim \mathcal{N}(0, \sigma_{\text{sonar}}^2 + \sigma_{\text{multipath}}^2)$
- Visual feature observation (pinhole + underwater refraction): $\mathbf{u}_t = \pi(\mathbf{R}_{cw} \mathbf{P}_w + \mathbf{t}_{cw}) + \boldsymbol{\delta}_{\text{refract}}(\theta_i, n_w, n_g)$
- Extended observation vector: $\mathbf{z}_t = [\mathbf{z}_t^{\text{sonar}}; \mathbf{z}_t^{\text{visual}}; \mathbf{z}_t^{\text{tactile}}; \mathbf{z}_t^{\text{IMU}}]^T$
- Multi-modal fusion via importance weighting: $w_t^{(i)} = w_{t-1}^{(i)} \cdot \prod_{s \in \mathcal{S}} p(\mathbf{z}_t^s \mid \mathbf{x}_t^{(i)}, \mathbf{m})$

### Figures:
- `fig_sensor_fusion_architecture.png`: Block diagram of multi-modal sensor fusion pipeline with uncertainty propagation
- `fig_underwater_refraction_model.png`: Ray tracing model for underwater stereo vision with refraction correction

### Table:
- **Table 4.1:** Sensor fusion strategies comparison (EKF vs. particle filter vs. factor graph vs. deep learned)

### Search Keywords:
- "underwater sonar visual inertial fusion SLAM"
- "multi-modal sensor fusion soft robot"
- "underwater refraction correction stereo vision"
- "particle filter multi-modal observation model"

### Primary Sources:
- [10] Rahman et al., "SVIn2: An Underwater SLAM System using Sonar, Visual, Inertial, and Depth", ICRA, 2019
- [11] Thrun, Burgard, Fox, "Probabilistic Robotics", MIT Press, 2005
- [12] Campos et al., "ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual-Inertial, and Multi-Map SLAM", IEEE TRO, 2021

---

## Chapter 5: SLAM מבוזר בהשראת מערכת העצבים של התמנון — Octopus-Inspired Distributed SLAM
**Hebrew Title:** \section{SLAM מבוזר בהשראת מערכת העצבים המבוזרת של התמנון: ארכיטקטורת גרף פקטורים מבוזרת}
**Target Pages:** 4–5

### Subsections:
1. \subsection{אנלוגיה ביולוגית — גנגליון מרכזי מול גנגליונים פריפריאליים בזרועות}
2. \subsection{גרף פקטורים מבוזר — כל זרוע כגורם SLAM עצמאי}
3. \subsection{תקשורת בין-זרועית ואלגוריתם איחוי מבוזר (Consensus)}

### Key Equations:
- Distributed factor graph decomposition: $\Phi(\mathbf{X}, \mathbf{M}) = \Phi_{\text{central}}(\mathbf{x}_0) + \sum_{a=1}^{N_{\text{arms}}} \Phi_a(\mathbf{X}_a, \mathbf{M}_a)$
- Arm-level factor: $\Phi_a(\mathbf{X}_a, \mathbf{M}_a) = \sum_{t} \|\mathbf{x}_{a,t+1} - f_a(\mathbf{x}_{a,t}, \mathbf{u}_{a,t})\|_{\Lambda_a}^2 + \sum_{t} \|\mathbf{z}_{a,t} - h_a(\mathbf{x}_{a,t}, \mathbf{m}_a)\|_{\Sigma_a}^2$
- Inter-arm constraint factor: $\Phi_{ab}(\mathbf{x}_a, \mathbf{x}_b) = \|\mathbf{T}_{ab} - \mathbf{T}_a^{-1} \mathbf{T}_b\|_{\Gamma_{ab}}^2$
- Distributed consensus update (ADMM): $\mathbf{x}_a^{k+1} = \arg\min_{\mathbf{x}_a} \left( \Phi_a(\mathbf{x}_a) + \frac{\rho}{2} \|\mathbf{x}_a - \mathbf{z}_a^k + \mathbf{u}_a^k\|^2 \right)$
- Global map update via marginalization: $p(\mathbf{m} \mid \mathbf{z}_{1:T}) = \int p(\mathbf{x}_{1:T}, \mathbf{m} \mid \mathbf{z}_{1:T}) \, d\mathbf{x}_{1:T}$

### Figures:
- `fig_distributed_factor_graph.png`: Factor graph showing central node, 6 arm sub-graphs, and inter-arm constraints
- `fig_consensus_convergence.png`: Convergence plot of distributed consensus algorithm across arms

### Table:
- **Table 5.1:** Computational complexity comparison (centralized SLAM vs. distributed SLAM vs. hierarchical SLAM)

### Search Keywords:
- "distributed factor graph SLAM multi-robot"
- "ADMM distributed optimization SLAM"
- "decentralized state estimation soft robot"
- "octopus nervous system distributed intelligence"

### Primary Sources:
- [13] Choudhary et al., "Distributed Trajectory Estimation with Privacy and Communication Constraints", IEEE TRO, 2017
- [14] Cunningham et al., "DDF-SAM: Fully Distributed SLAM using Constrained Factor Graphs", IROS, 2010
- [15] Sumanaweera et al., "Octopus-inspired distributed control for soft robotic arms", arXiv, 2026

---

## Chapter 6: תכנון תנועה אדפטיבי תוך שימוש בלמידת חיזוק מבוזרת — Adaptive Motion Planning via Distributed Reinforcement Learning
**Hebrew Title:** \section{תכנון תנועה אדפטיבי לניווט בסביבות משתנות באמצעות למידת חיזוק מבוזרת}
**Target Pages:** 3–4

### Subsections:
1. \subsection{מרחב מצב ופעולה לרחפן רך רב-זרועי}
2. \subsection{פונקציית תגמול מבוססת אי-ודאות SLAM}
3. \subsection{למידת חיזוק מבוזרת מרובת-סוכנים — כל זרוע כסוכן עצמאי}

### Key Equations:
- State space: $\mathbf{s}_t = [\mathbf{x}_t; \boldsymbol{\kappa}_{1:N}; \mathbf{v}_{1:N}; \Sigma_t^{\text{SLAM}}; \mathbf{d}_{\text{obs}}]$
- Action space (per arm): $\mathbf{a}_{a,t} = [\Delta \kappa_{a,t}; \Delta \phi_{a,t}; \Delta l_{a,t}] \in \mathbb{R}^3$
- Reward function: $r_t = \alpha_1 \cdot \text{IG}(\mathbf{z}_t) - \alpha_2 \cdot \|\mathbf{x}_t - \mathbf{x}_{\text{goal}}\| - \alpha_3 \cdot \|\boldsymbol{\kappa}_t\|^2 - \alpha_4 \cdot \mathbb{I}_{\text{collision}}$
  where $\text{IG}(\mathbf{z}_t) = H(\mathbf{x}_{t-1}) - H(\mathbf{x}_t \mid \mathbf{z}_t)$ is information gain
- Multi-agent PPO objective: $\mathcal{L}_a(\theta_a) = \mathbb{E}_{\mathbf{s}, \mathbf{a}} \left[ \min\left( r_a(\theta_a) \hat{A}_a, \text{clip}(r_a(\theta_a), 1-\epsilon, 1+\epsilon) \hat{A}_a \right) \right]$
- Centralized critic, decentralized actor: $V(\mathbf{s}_t) = \mathbb{E} \left[ \sum_{k=0}^{\infty} \gamma^k r_{t+k} \mid \mathbf{s}_t \right]$

### Figures:
- `fig_reinforcement_learning_architecture.png`: Multi-agent PPO architecture with centralized critic and decentralized actors per arm
- `fig_motion_planning_trajectory.png`: Example trajectory in cluttered underwater environment with obstacle avoidance

### Table:
- **Table 6.1:** Hyperparameters for distributed RL training (learning rate, discount factor, entropy coefficient, batch size, etc.)

### Search Keywords:
- "multi-agent reinforcement learning soft robot control"
- "active SLAM information gain reward"
- "distributed PPO multi-robot navigation"
- "soft robot motion planning reinforcement learning"

### Primary Sources:
- [16] Schulman et al., "Proximal Policy Optimization Algorithms", arXiv, 2017
- [17] Lowe et al., "Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments", NeurIPS, 2017
- [18] Chaplot et al., "Active Neural SLAM", ICLR, 2020

---

## Chapter 7: מיפוי סביבה תוך שימוש במישוש ובאקוסטיקה — Tactile-Acoustic Environment Mapping
**Hebrew Title:** \section{מיפוי סביבה תת-ימית תוך שילוב חישת מישוש ואקוסטיקה}
**Target Pages:** 3–4

### Subsections:
1. \subsection{מיפוי מבוסס סונאר — רשת עצבית לזיהוי מבנים תת-ימיים}
2. \subsection{מיפוי מישוש — זיהוי גאומטריית משטח באמצעות מגע}
3. \subsection{מיזוג מפות — גישת מפת סיכויים (Occupancy Grid) היברידית}

### Key Equations:
- Sonar occupancy grid update (log-odds): $l_{t,i} = l_{t-1,i} + \log\left( \frac{p(m_i \mid \mathbf{z}_t^{\text{sonar}})}{1 - p(m_i \mid \mathbf{z}_t^{\text{sonar}})} \right) - l_0$
- Tactile occupancy update: $p(m_i \mid \mathbf{z}_t^{\text{tactile}}) = \begin{cases} 0.95 & \text{if contact detected at cell } i \\ 0.50 & \text{if no contact but within reach} \\ l_0 & \text{otherwise} \end{cases}$
- Hybrid map fusion: $p(m_i \mid \mathbf{z}_{1:T}) = \sigma\left( l_{0,i} + \sum_{t} \Delta l_{t,i}^{\text{sonar}} + \sum_{t} \Delta l_{t,i}^{\text{tactile}} \right)$
- Surface normal estimation from tactile contact points: $\hat{\mathbf{n}}_i = \arg\min_{\mathbf{n}} \sum_{j \in \mathcal{N}(i)} \left( \mathbf{n}^T (\mathbf{p}_j - \mathbf{p}_i) \right)^2$

### Figures:
- `fig_occupancy_grid_comparison.png`: Comparison of sonar-only, tactile-only, and hybrid occupancy maps in a structured underwater environment
- `fig_tactile_surface_reconstruction.png`: 3D surface reconstruction from tactile contact points with estimated normals

### Table:
- **Table 7.1:** Mapping accuracy metrics (RMSE, completeness, entropy reduction) for each modality and fusion

### Search Keywords:
- "occupancy grid mapping underwater sonar"
- "tactile mapping surface reconstruction soft robot"
- "multi-modal occupancy grid fusion"
- "probabilistic mapping contact sensing"

### Primary Sources:
- [19] Hornung et al., "OctoMap: An Efficient Probabilistic 3D Mapping Framework Based on Octrees", Autonomous Robots, 2013
- [20] Fox et al., "Active SLAM with Exploration", IJRR, 2006
- [21] Luo et al., "Tactile SLAM: Real-time Object Mapping using Tactile Sensing", IEEE TRO, 2022

---

## Chapter 8: תוצאות סימולציה וניסויים — Simulation and Experimental Results
**Hebrew Title:** \section{תוצאות סימולציה וניסויים: הערכת ביצועי מערכת הניווט הביומימטית}
**Target Pages:** 4–5

### Subsections:
1. \subsection{הגדרת סביבת הסימולציה — סימולטור רובוט רך תת-ימי (SOFA + UUV Simulator)}
2. \subsection{תרחישי ניסוי — ניווט במערות תת-ימיות, שדות אצות, מבנים תעשייתיים}
3. \subsection{השוואת ביצועים — SLAM מבוזר מול SLAM ריכוזי}
4. \subsection{ניתוח רגישות — השפעת רעש חיישנים, אובדן חיישן, ועומק}

### Key Equations:
- ATE (Absolute Trajectory Error): $\text{ATE} = \sqrt{\frac{1}{T} \sum_{t=1}^{T} \| \mathbf{T}_{gt,t}^{-1} \mathbf{T}_{est,t} \|_{\text{trans}}^2}$
- RPE (Relative Pose Error): $\text{RPE} = \frac{1}{T-\Delta} \sum_{t=1}^{T-\Delta} \| (\mathbf{T}_{gt,t}^{-1} \mathbf{T}_{gt,t+\Delta})^{-1} (\mathbf{T}_{est,t}^{-1} \mathbf{T}_{est,t+\Delta}) \|_{\text{trans}}$
- Map entropy reduction: $\Delta H = H_{\text{prior}} - H_{\text{posterior}} = \sum_i \left[ p_i \log p_i + (1-p_i) \log(1-p_i) \right]_{\text{prior}} - \left[ \cdot \right]_{\text{posterior}}$
- Computation time scaling: $T_{\text{comp}}(N_{\text{arms}}) = T_0 + \alpha N_{\text{arms}} + \beta N_{\text{arms}}^2$ (centralized) vs. $T_{\text{comp}}^{\text{dist}}(N_{\text{arms}}) = T_0 + \alpha N_{\text{arms}}$ (distributed)

### Figures:
- `fig_trajectory_comparison.png`: Ground truth vs. estimated trajectories for centralized SLAM, distributed SLAM, and baseline (ORB-SLAM3 underwater)
- `fig_error_metrics.png`: Box plots of ATE and RPE across 50 Monte Carlo runs for each method

### Table:
- **Table 8.1:** Quantitative results (ATE [m], RPE [m], map entropy, computation time [ms/frame], success rate) for all methods across all scenarios

### Search Keywords:
- "underwater SLAM benchmark dataset"
- "soft robot simulation SOFA framework"
- "SLAM evaluation metrics ATE RPE"
- "distributed SLAM experimental results"

### Primary Sources:
- [22] Sturm et al., "A Benchmark for the Evaluation of RGB-D SLAM Systems", IROS, 2012
- [23] Faure et al., "SOFA: A Multi-Model Framework for Interactive Physical Simulation", Springer, 2012
- [24] Manhaes et al., "UUV Simulator: A Gazebo-based package for underwater robotics", JOSS, 2016

---

## Chapter 9: סיכום, מגבלות ועבודה עתידית — Conclusion, Limitations, and Future Work
**Hebrew Title:** \section{סיכום, מגבלות המחקר והצעות להמשך}
**Target Pages:** 2–3

### Subsections:
1. \subsection{סיכום התרומות המרכזיות}
2. \subsection{מגבלות המחקר — מגבלות חומרה, סביבת ניסוי, והכללה}
3. \subsection{כיווני מחקר עתידיים — רובוט רך אוטונומי לחלוטין, למידה אנד-טו-אנד, מערכות רב-רחפנים}

### Key Equations:
- Summary of key performance: $\eta_{\text{system}} = \frac{\text{ATE}_{\text{baseline}} - \text{ATE}_{\text{proposed}}}{\text{ATE}_{\text{baseline}}} \times 100\%$
- Scalability bound: $N_{\text{arms}}^{\text{max}} = \arg\max_N \left( \text{SuccessRate}(N) \geq 0.95 \right)$

### Figures:
- `fig_limitations_analysis.png`: Failure mode analysis pie chart (sensor dropout, communication loss, model mismatch)

### Table:
- **Table 9.1:** Summary of contributions mapped to specific research questions

### Search Keywords:
- "soft robot future challenges SLAM"
- "bio-inspired robotics limitations"
- "underwater autonomous navigation open problems"

### Primary Sources:
- [25] Laschi et al., "Soft robotics: Technologies and systems pushing the boundaries of robot abilities", Science Robotics, 2016
- [26] Cadena et al., "Past, Present, and Future of Simultaneous Localization and Mapping", IEEE TRO, 2016

---

## Appendix A: נספח מתמטי — Mathematical Derivations
**Hebrew Title:** \section{נספח מתמטי: גזירות מפורטות}
**Target Pages:** 1–2

### Content:
- Full derivation of distributed ADMM consensus update
- Jacobian matrices for soft arm kinematics
- Sensor noise covariance calibration procedure

---

## Appendix B: נספח ניסויי — Experimental Setup Details
**Hebrew Title:** \section{נספח ניסויי: פרטי מערך הניסוי}
**Target Pages:** 1

### Content:
- Hardware specifications (soft drone prototype, sensor part numbers, microcontroller)
- Software stack (ROS2, GTSAM, PyTorch, SOFA)
- Dataset availability and download link

---

## Summary Statistics

| Chapter | Hebrew Title | Pages | Equations | Figures | Tables |
|---------|-------------|-------|-----------|---------|--------|
| 1 | מבוא | 3–4 | 3 | 2 | 1 |
| 2 | מודל קינמטי ודינמי | 3–4 | 4 | 2 | 1 |
| 3 | חישת מישוש מבוזרת | 3–4 | 4 | 2 | 1 |
| 4 | מיזוג חיישנים רב-מודאלי | 3–4 | 4 | 2 | 1 |
| 5 | SLAM מבוזר | 4–5 | 5 | 2 | 1 |
| 6 | תכנון תנועה אדפטיבי | 3–4 | 4 | 2 | 1 |
| 7 | מיפוי סביבה | 3–4 | 4 | 2 | 1 |
| 8 | תוצאות | 4–5 | 4 | 2 | 1 |
| 9 | סיכום | 2–3 | 2 | 1 | 1 |
| **Total** | | **28–37** | **34** | **17** | **9** |

*Note: Target is 25–30 pages; final trimming will occur during writing phase.*

---

**OUTLINE COMPLETE**