# Domain Contribution: Control Systems for AUV Navigation — Quadrotor Dynamics, PID/LQR Control, Path Planning, and State Estimation

## 1. Technical Analysis (1,200+ words)

### 1.1 Quadrotor Dynamics and Equations of Motion

The dynamics of an autonomous underwater vehicle (AUV) — and by extension the quadrotor-inspired control architectures adapted for underwater flight — are governed by the Newton-Euler equations of motion for a 6-degree-of-freedom (6-DOF) rigid body. For an AUV operating in the underwater domain, the vehicle is subject to hydrodynamic forces (added mass, drag, lift, buoyancy) that are absent in aerial quadrotors but share the same fundamental rigid-body dynamics framework (Fossen, 2011, *Handbook of Marine Craft Hydrodynamics and Motion Control*, pp. 15–42).

The 6-DOF kinematic and dynamic equations are expressed in two coordinate frames: the inertial (navigation) frame {n} and the body-fixed frame {b}. The generalized position vector is (oldsymbol{eta} = [x, y, z, phi, 	heta, psi]^	op) in {n}, and the generalized velocity vector is (oldsymbol{
u} = [u, v, w, p, q, r]^	op) in {b}. The kinematic transformation is:

[
dot{oldsymbol{eta}} = mathbf{J}(oldsymbol{eta}) oldsymbol{
u}
]

where (mathbf{J}(oldsymbol{eta})) is the 6×6 transformation matrix composed of the rotation matrix (mathbf{R}_b^n(phi, 	heta, psi)) and the angular velocity transformation matrix (mathbf{T}(phi, 	heta)) (Fossen, 2011, Eq. 2.24–2.28).

The dynamic equations in the body frame are:

[
mathbf{M} dot{oldsymbol{
u}} + mathbf{C}(oldsymbol{
u}) oldsymbol{
u} + mathbf{D}(oldsymbol{
u}) oldsymbol{
u} + mathbf{g}(oldsymbol{eta}) = oldsymbol{	au}
]

where (mathbf{M} = mathbf{M}_{RB} + mathbf{M}_A) is the sum of rigid-body inertia and added mass, (mathbf{C}(oldsymbol{
u})) is the Coriolis-centripetal matrix (including added mass contributions), (mathbf{D}(oldsymbol{
u})) is the hydrodynamic damping matrix (linear + quadratic drag), (mathbf{g}(oldsymbol{eta})) is the restoring force vector (gravity and buoyancy), and (oldsymbol{	au}) is the control input vector (thruster forces and moments) (Fossen, 2011, Ch. 3).

For quadrotor-inspired AUV designs (vehicles with four thrusters in a cross configuration), the control allocation matrix maps individual thruster forces to body-frame forces and moments:

[
oldsymbol{	au} = mathbf{B} mathbf{u}, quad mathbf{u} = [f_1, f_2, f_3, f_4]^	op
]

where (mathbf{B}) is the 6×4 thrust allocation matrix depending on thruster geometry (Mahony et al., 2012, *IEEE Control Systems Magazine*, Eq. 7).

### 1.2 PID and LQR Controller Design

**PID Control:** The proportional-integral-derivative (PID) controller remains the most widely deployed control law for AUV depth, heading, and speed regulation due to its simplicity and robustness (Li et al., 2021, *Journal of Marine Science and Engineering*, Vol. 9, No. 9, p. 1020). For depth control, the PID law is:

[
	au_z(t) = K_p e_z(t) + K_i int_0^t e_z(	au) d	au + K_d dot{e}_z(t), quad e_z(t) = z_{	ext{des}}(t) - z(t)
]

Joshi and Talange (2015, *International Conference on Industrial Instrumentation and Control*) demonstrated that PID control achieves zero steady-state error for REMUS AUV depth control with settling time under 2 seconds, though with 5–8% overshoot depending on tuning.

**LQR Control:** The linear quadratic regulator (LQR) provides optimal state feedback for linearized AUV models. The AUV dynamics are linearized about an operating point (e.g., constant forward speed (u_0), zero pitch/roll) to obtain:

[
dot{mathbf{x}} = mathbf{A} mathbf{x} + mathbf{B} mathbf{u}, quad mathbf{x} = [delta u, v, w, p, q, r, phi, 	heta, psi, delta z]^	op
]

The LQR gain (mathbf{K}) minimizes the quadratic cost:

[
J = int_0^infty (mathbf{x}^	op mathbf{Q} mathbf{x} + mathbf{u}^	op mathbf{R} mathbf{u}) dt
]

yielding the optimal control law (mathbf{u} = -mathbf{K} mathbf{x}) where (mathbf{K} = mathbf{R}^{-1} mathbf{B}^	op mathbf{P}) and (mathbf{P}) solves the algebraic Riccati equation (mathbf{A}^	op mathbf{P} + mathbf{P} mathbf{A} - mathbf{P} mathbf{B} mathbf{R}^{-1} mathbf{B}^	op mathbf{P} + mathbf{Q} = 0) (Athans and Falb, 1966, *Optimal Control*, Ch. 3).

Joshi and Talange (2015) reported that LQR achieves zero overshoot for AUV depth control with settling time comparable to PID (1.5–2.0 s), but with superior disturbance rejection. Priyadarshini et al. (2022, *Engineering, Technology & Applied Science Research*, Vol. 12, No. 6) confirmed LQR outperforms PID in terms of overshoot (0% vs. 5–8%) for pitch control of an AUV.

### 1.3 Path Planning: RRT*, A*, and D*

**RRT* (Rapidly-exploring Random Tree Star):** The RRT* algorithm provides asymptotically optimal path planning by rewiring the tree to minimize path cost (Karaman and Frazzoli, 2011, *International Journal of Robotics Research*, Vol. 30, No. 7, pp. 846–894). For AUV navigation in 3D underwater environments, the RRT* algorithm samples configuration space (mathcal{C} subset mathbb{R}^3 	imes SO(3)) and builds a tree (mathcal{T} = (V, E)) where vertices (v in V) represent collision-free poses and edges (e in E) represent feasible trajectories.

The key innovation in RRT* is the **rewiring step**: after adding a new vertex (v_{	ext{new}}), the algorithm considers all vertices within a ball of radius (r = gamma (log n / n)^{1/d}) (where (d) is the dimension and (n) is the number of vertices) and rewires the tree to minimize the cost-to-come from the start (Karaman and Frazzoli, 2011, Theorem 38).

Recent advances for AUV applications include:
- **Current-Biased RRT* (CB-RRT*):** Incorporates ocean current information into the sampling distribution to generate energy-efficient paths (MDPI J. Mar. Sci. Eng., 2025, Vol. 15, No. 1, p. 18).
- **DCGB-DAPF-RRT*:** Integrates directional cone sampling, goal-biasing, adaptive step length, and dynamic artificial potential fields for underactuated AUVs (Nature Scientific Reports, 2025).

**A* and D*:** The A* algorithm uses a heuristic (h(n)) to guide search on a discretized grid, guaranteeing optimality when (h(n)) is admissible (Hart et al., 1968, *IEEE Trans. Systems Science and Cybernetics*, Vol. 4, No. 2). D* (Dynamic A*) extends A* to handle dynamic obstacles by repairing the search tree incrementally (Stentz, 1994, *ICRA*). For AUVs, D* Lite (Koenig and Likhachev, 2002, *AAAI*) is preferred for real-time replanning in partially known environments.

### 1.4 Trajectory Optimization

Trajectory optimization for AUVs typically employs direct transcription methods (Betts, 2010, *Practical Methods for Optimal Control and Estimation Using Nonlinear Programming*). The optimal control problem is:

[
min_{mathbf{x}(t), mathbf{u}(t)} Phi(mathbf{x}(t_f)) + int_{t_0}^{t_f} L(mathbf{x}(t), mathbf{u}(t)) dt
]

subject to dynamics (dot{mathbf{x}} = mathbf{f}(mathbf{x}, mathbf{u})), state constraints (mathbf{x}(t) in mathcal{X}), and control constraints (mathbf{u}(t) in mathcal{U}).

For real-time implementation on embedded platforms (ARM Cortex-M, NVIDIA Jetson), the trajectory is often parameterized using polynomial splines (minimum-jerk or minimum-snap trajectories) as in Mellinger and Kumar (2011, *ICRA*), adapted for underwater vehicles by considering hydrodynamic drag.

### 1.5 State Estimation for Control

State estimation for AUV control relies on sensor fusion of IMU, DVL, depth sensor, and sonar. The Extended Kalman Filter (EKF) is the standard approach (Thrun et al., 2005, *Probabilistic Robotics*, Ch. 3). The prediction step propagates the state using the kinematic model:

[
hat{mathbf{x}}_{k|k-1} = mathbf{f}(hat{mathbf{x}}_{k-1|k-1}, mathbf{u}_k), quad mathbf{P}_{k|k-1} = mathbf{F}_k mathbf{P}_{k-1|k-1} mathbf{F}_k^	op + mathbf{Q}_k
]

The update step corrects using DVL velocity and depth sensor measurements:

[
mathbf{K}_k = mathbf{P}_{k|k-1} mathbf{H}_k^	op (mathbf{H}_k mathbf{P}_{k|k-1} mathbf{H}_k^	op + mathbf{R}_k)^{-1}
]
[
hat{mathbf{x}}_{k|k} = hat{mathbf{x}}_{k|k-1} + mathbf{K}_k (mathbf{z}_k - mathbf{h}(hat{mathbf{x}}_{k|k-1}))
]

Krauss and Stilwell (2022, arXiv:2210.06510) demonstrated that the Unscented Kalman Filter (UKF) on manifolds outperforms EKF for AUV navigation, achieving 30% lower RMSE in position estimation during experimental trials.

### 1.6 Real-Time Control on Embedded Platforms

Real-time control on embedded platforms (ARM Cortex-M4/M7, STM32, NVIDIA Jetson) requires careful attention to timing constraints. Typical control loops run at 50–200 Hz for inner-loop attitude control and 10–50 Hz for outer-loop position control. The computational budget for each control cycle is typically 1–5 ms on ARM Cortex-M4 (168 MHz) and 0.1–1 ms on Jetson Orin.

Key considerations include:
- **Fixed-point arithmetic** for PID controllers on low-end MCUs to avoid floating-point overhead
- **Look-up tables** for trigonometric functions in kinematic transformations
- **Priority-based scheduling** with IMU readings at highest priority (1 kHz), DVL at medium (10 Hz), and sonar at lowest (1–5 Hz)

---

## 2. Key Algorithms

### Algorithm 1: LQR Depth Controller for AUV

```
Input: Desired depth z_des, current state estimate [z, w, theta, q]^T
Output: Thruster command tau_z

1. Compute depth error: e_z = z_des - z
2. Form error state vector: x_e = [e_z, w, theta, q]^T
3. Compute LQR control law: tau_z = -K * x_e
   where K = lqr(A, B, Q, R) solved offline via algebraic Riccati equation
4. Apply saturation: tau_z = clamp(tau_z, -tau_max, +tau_max)
5. Return tau_z
```

**Reference:** Athans and Falb (1966), *Optimal Control*, Ch. 3; Joshi and Talange (2015), ICIC.

### Algorithm 2: RRT* Path Planning for AUV in 3D Underwater Environment

```
Input: Start pose q_start, goal pose q_goal, obstacle map O, max iterations N
Output: Path P from q_start to q_goal

1. Initialize tree T with root q_start
2. For i = 1 to N:
   a. Sample random configuration q_rand from C_free with goal bias p_goal
   b. Find nearest vertex q_nearest = argmin_{v in V} ||v - q_rand||
   c. Steer: q_new = steer(q_nearest, q_rand, step_size)
   d. If collision_free(q_nearest, q_new, O):
      i. Find near vertices: Q_near = {v in V : ||v - q_new|| < r_n}
      ii. Choose parent: q_min = argmin_{v in Q_near} cost(v) + cost(v, q_new)
      iii. Add edge (q_min, q_new) to T
      iv. Rewire: for each v in Q_near:
          if cost(q_new) + cost(q_new, v) < cost(v):
              rewire parent of v to q_new
   e. If ||q_new - q_goal|| < goal_threshold:
      i. Extract path P from q_start to q_goal
      ii. Return P
3. Return failure (no path found)
```

**Reference:** Karaman and Frazzoli (2011), *IJRR*, Vol. 30, No. 7, pp. 846–894.

---

## 3. Equations (LaTeX-ready)

### Equation 1: 6-DOF AUV Dynamic Model (Newton-Euler)

egin{equation}
mathbf{M} dot{oldsymbol{
u}} + mathbf{C}(oldsymbol{
u}) oldsymbol{
u} + mathbf{D}(oldsymbol{
u}) oldsymbol{
u} + mathbf{g}(oldsymbol{eta}) = oldsymbol{	au} label{eq:auv_dynamics}
end{equation}

where (oldsymbol{
u} = [u, v, w, p, q, r]^	op in mathbb{R}^6) is the body-fixed velocity vector, (mathbf{M} = mathbf{M}_{RB} + mathbf{M}_A in mathbb{R}^{6 	imes 6}) is the inertia matrix (rigid-body + added mass), (mathbf{C}(oldsymbol{
u}) in mathbb{R}^{6 	imes 6}) is the Coriolis-centripetal matrix, (mathbf{D}(oldsymbol{
u}) = mathbf{D}_{	ext{lin}} + mathbf{D}_{	ext{quad}}|oldsymbol{
u}| in mathbb{R}^{6 	imes 6}) is the hydrodynamic damping matrix, (mathbf{g}(oldsymbol{eta}) in mathbb{R}^6) is the restoring force vector, and (oldsymbol{	au} in mathbb{R}^6) is the control input vector.

**Source:** Fossen (2011), *Handbook of Marine Craft Hydrodynamics and Motion Control*, Eq. 3.1–3.5, pp. 15–42.

### Equation 2: LQR Optimal Control Law via Algebraic Riccati Equation

egin{equation}
mathbf{A}^	op mathbf{P} + mathbf{P} mathbf{A} - mathbf{P} mathbf{B} mathbf{R}^{-1} mathbf{B}^	op mathbf{P} + mathbf{Q} = mathbf{0} label{eq:riccati}
end{equation}

egin{equation}
mathbf{K} = mathbf{R}^{-1} mathbf{B}^	op mathbf{P}, quad mathbf{u} = -mathbf{K} mathbf{x} label{eq:lqr_law}
end{equation}

where (mathbf{A} in mathbb{R}^{n 	imes n}) is the linearized system matrix, (mathbf{B} in mathbb{R}^{n 	imes m}) is the input matrix, (mathbf{Q} = mathbf{Q}^	op succeq mathbf{0} in mathbb{R}^{n 	imes n}) is the state weighting matrix, (mathbf{R} = mathbf{R}^	op succ mathbf{0} in mathbb{R}^{m 	imes m}) is the control weighting matrix, (mathbf{P} in mathbb{R}^{n 	imes n}) is the unique positive semidefinite solution to the algebraic Riccati equation, and (mathbf{K} in mathbb{R}^{m 	imes n}) is the optimal state feedback gain matrix.

**Source:** Athans and Falb (1966), *Optimal Control: An Introduction to the Theory and Its Applications*, Eq. 3.5-12, pp. 164–168.

### Equation 3: RRT* Asymptotic Optimality — Rewiring Radius

egin{equation}
r_n = gamma left( frac{log n}{n} ight)^{1/d} label{eq:rrt_radius}
end{equation}

where (r_n) is the rewiring radius after (n) samples, (d) is the dimension of the configuration space ((d = 3) for position-only planning, (d = 6) for full pose planning), and (gamma > 2^{1/d} (1 + 1/d)^{1/d} (mu(mathcal{C}_{	ext{free}}) / zeta_d)^{1/d}) is a constant ensuring asymptotic optimality, with (mu(mathcal{C}_{	ext{free}})) the Lebesgue measure of the free configuration space and (zeta_d) the volume of the unit ball in (mathbb{R}^d).

**Source:** Karaman and Frazzoli (2011), *International Journal of Robotics Research*, Vol. 30, No. 7, Theorem 38, p. 870.

### Equation 4: EKF State Estimation for AUV Control

egin{equation}
hat{mathbf{x}}_{k|k-1} = mathbf{f}(hat{mathbf{x}}_{k-1|k-1}, mathbf{u}_k), quad mathbf{P}_{k|k-1} = mathbf{F}_k mathbf{P}_{k-1|k-1} mathbf{F}_k^	op + mathbf{Q}_k label{eq:ekf_predict}
end{equation}

egin{equation}
mathbf{K}_k = mathbf{P}_{k|k-1} mathbf{H}_k^	op (mathbf{H}_k mathbf{P}_{k|k-1} mathbf{H}_k^	op + mathbf{R}_k)^{-1} label{eq:ekf_gain}
end{equation}

egin{equation}
hat{mathbf{x}}_{k|k} = hat{mathbf{x}}_{k|k-1} + mathbf{K}_k (mathbf{z}_k - mathbf{h}(hat{mathbf{x}}_{k|k-1})), quad mathbf{P}_{k|k} = (mathbf{I} - mathbf{K}_k mathbf{H}_k) mathbf{P}_{k|k-1} label{eq:ekf_update}
end{equation}

where (mathbf{x}_k in mathbb{R}^{n}) is the state vector (position, velocity, attitude, IMU biases), (mathbf{f}(cdot)) is the nonlinear kinematic/dynamic model, (mathbf{F}_k = partial mathbf{f}/partial mathbf{x}|_{hat{mathbf{x}}_{k-1|k-1}}) is the Jacobian, (mathbf{Q}_k) is the process noise covariance, (mathbf{z}_k) is the measurement vector (DVL velocity, depth, sonar range), (mathbf{h}(cdot)) is the measurement model, (mathbf{H}_k = partial mathbf{h}/partial mathbf{x}|_{hat{mathbf{x}}_{k|k-1}}) is the measurement Jacobian, and (mathbf{R}_k) is the measurement noise covariance.

**Source:** Thrun, Burgard, and Fox (2005), *Probabilistic Robotics*, Eqs. 3.13–3.15, pp. 54–57.

### Equation 5: Minimum-Jerk Trajectory Optimization

egin{equation}
min_{x(t), y(t), z(t), psi(t)} int_{t_0}^{t_f} left( dddot{x}^2 + dddot{y}^2 + dddot{z}^2 + ddot{psi}^2 ight) dt label{eq:min_jerk}
end{equation}

subject to:
egin{align}
x(t_0) &= x_0, quad dot{x}(t_0) = u_0, quad ddot{x}(t_0) = 0 
onumber \
x(t_f) &= x_f, quad dot{x}(t_f) = u_f, quad ddot{x}(t_f) = 0 
onumber \
y(t_0) &= y_0, quad dot{y}(t_0) = v_0, quad ddot{y}(t_0) = 0 
onumber \
y(t_f) &= y_f, quad dot{y}(t_f) = v_f, quad ddot{y}(t_f) = 0 
onumber \
z(t_0) &= z_0, quad dot{z}(t_0) = w_0, quad ddot{z}(t_0) = 0 
onumber \
z(t_f) &= z_f, quad dot{z}(t_f) = w_f, quad ddot{z}(t_f) = 0 
onumber \
psi(t_0) &= psi_0, quad dot{psi}(t_0) = r_0 
onumber \
psi(t_f) &= psi_f, quad dot{psi}(t_f) = r_f 
onumber
end{align}

The solution is a 5th-order polynomial for each degree of freedom: (x(t) = a_0 + a_1 t + a_2 t^2 + a_3 t^3 + a_4 t^4 + a_5 t^5), with coefficients determined by the boundary conditions.

**Source:** Mellinger and Kumar (2011), *ICRA*, "Minimum snap trajectory generation and control for quadrotors,