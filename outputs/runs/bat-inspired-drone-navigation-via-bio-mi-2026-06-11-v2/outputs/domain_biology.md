# Domain Contribution: Neuroethology, Biological Sensing & Bio-Inspired Systems

**Contributor:** Dr. Noa Tal, Ph.D. (Neuroethology and Computational Neuroscience, Tel Aviv University, 2017)
**Specialization:** Bat echolocation (CF-FM sonar, acoustic fovea, DSC mechanism), neural computation for spatial mapping, bio-inspired algorithm design, dolphin biosonar, lateral line sensing

---

## 1. TECHNICAL ANALYSIS (500+ words)

### State-of-the-Art in Bat Neuroethology and Bio-Inspired Sonar

The biological sonar of echolocating bats represents the most sophisticated active sensing system in the natural world, achieving 3D navigation in complete darkness with a neural power budget of approximately 2 mW (Griffin, 1958; Schnitzler & Denzinger, 2011). Two distinct echolocation strategies have evolved: constant-frequency (CF) bats (Rhinolophidae, Hipposideridae) and frequency-modulated (FM) bats (Vespertilionidae, Molossidae). The greater horseshoe bat, *Rhinolophus ferrumequinum*, employs CF-FM hybrid pulses centred near 83 kHz, with a duty cycle of 30–50% — the highest of any echolocating bat (Schuller et al., 1974).

**The Acoustic Fovea — A Biological Matched Filter:** The most remarkable specialization in the *Rhinolophus* auditory system is the acoustic fovea: a discrete, mechanically stiffened region of the basilar membrane covering approximately 30% of its length while representing only a 3 kHz bandwidth around 83 kHz (Vater & K\"ossl, 2011; Duifhuis & Vater, 1985). The basilar membrane stiffness in the foveal region is approximately 100 times greater than in the guinea pig cochlea (Wilson & Bruns, 1983), creating a mechanical impedance discontinuity that standard cochlear models (e.g., Greenwood, 1990) cannot predict without explicitly modelling the stiffness gradient. This structure provides hyper-acute frequency discrimination of approximately 0.05% around the reference frequency — a resolution unmatched by any engineered sonar system operating at comparable power levels.

**Doppler Shift Compensation (DSC) — The Most Precise Biological Control Loop:** DSC is a closed-loop frequency-tracking servo that stabilises the returning echo frequency onto the acoustic fovea. As the bat approaches a target, the echo returns blue-shifted; the animal lowers its emission frequency by exactly the expected Doppler offset so that the echo always lands on the 83 kHz fovea (Schuller et al., 1974; Schnitzler & Denzinger, 2011). The control loop operates with sub-millisecond latency, zero overshoot, and steady-state accuracy of ±0.05% — a performance specification that no engineered phase-locked loop achieves without digital correction. The neural implementation resides in the paralemniscal tegmental area and the superior olivary complex, with the inferior colliculus providing the frequency-error signal (Metzner, 1993).

**Neural Computation for 3D Spatial Mapping:** The bat brain constructs spatial representations through a hierarchy of neural computations. In the inferior colliculus (IC), delay-tuned neurons respond selectively to specific pulse-echo delays, encoding target range with microsecond temporal precision (O'Neill & Suga, 1982; Portfors & Wenstrup, 1999). Combination-sensitive neurons in the auditory cortex respond to specific pulse-echo pairs, enabling clutter rejection and surface texture classification (Suga et al., 1978; Suga, 1990). The bat hippocampus contains 3D volumetric place cells that fire when the animal occupies a specific location in volumetric space, with isotropic firing fields spanning approximately 30 cm (Yartsev & Ulanovsky, 2013). Grid cells in the entorhinal cortex provide a metric coordinate frame with grid spacing increasing along the dorsoventral axis from approximately 30 cm to over 100 cm (Hafting et al., 2005; Ginosar et al., 2021).

**Dolphin Biosonar and Lateral Line Sensing:** For comparative context, delphinid odontocetes (e.g., *Tursiops truncatus*) produce broadband click trains (40–150 kHz) with inter-click intervals that encode target range; the melon serves as an acoustic lens for beam forming with a beamwidth of approximately 10° (Au, 1993). The blind Mexican cave fish (*Astyanax mexicanus*) uses the lateral line system — an array of mechanosensory hair-cell neuromasts — for hydrodynamic imaging of nearby obstacles at ranges up to 1 body length, analogous to a passive sonar array (Windsor et al., 2008).

**Dominant Approaches and Failure Modes:** Current bio-inspired sonar systems for drones (Müller et al., 2024; Velmurugan et al., 2026) use MEMS piezoelectric transducers operating at 40 kHz with 5 kHz bandwidth, achieving range resolution of approximately 3.4 cm. The dominant failure modes are: (1) motor noise masking weak echoes (PSNR drops to -4.9 dB during flight), (2) multipath interference in reverberant environments, and (3) limited angular resolution from single-element transducers (beamwidth 30–60°). The BatDeck system (Müller et al., 2024) achieves 20 Hz update rate with < 50 mW power consumption, but lacks Doppler estimation capability — a critical omission given that bats rely on Doppler information for velocity estimation and flutter detection.

---

## 2. EQUATIONS (minimum 3, LaTeX-ready)

### Equation 1: Acoustic Fovea Frequency Selectivity (Basilar Membrane Mechanical Model)

\begin{equation}
Q_{\text{fovea}} = \frac{f_0}{\Delta f_{3\text{dB}}} = \frac{\sqrt{k_{\text{BM}}(x) / m_{\text{BM}}(x)}}{2\pi \cdot \gamma \cdot \sqrt{k_{\text{BM}}(x) / m_{\text{BM}}(x)}} = \frac{1}{2\pi \gamma} \label{eq:fovea_q}
\end{equation}

where $Q_{\text{fovea}}$ is the quality factor of the acoustic fovea (measured $\approx 100$ in *R. ferrumequinum*), $f_0 = 83$ kHz is the reference frequency, $\Delta f_{3\text{dB}}$ is the 3 dB bandwidth, $k_{\text{BM}}(x)$ is the basilar membrane stiffness per unit length at position $x$ along the cochlea, $m_{\text{BM}}(x)$ is the mass per unit length, and $\gamma$ is the damping coefficient. The stiffness in the foveal region is approximately $40 \times 10^6$ dyne/cm³, approximately 100× greater than non-foveal regions (Wilson & Bruns, 1983).

### Equation 2: Doppler Shift Compensation Control Law

\begin{equation}
f_{\text{emit}}^{(n+1)} = f_{\text{ref}} - \frac{2 f_{\text{ref}}}{c} \cdot v_r^{(n)} \cdot \cos\theta^{(n)} + \eta \cdot \left( f_{\text{ref}} - f_{\text{echo}}^{(n)} \right) \label{eq:dsc_control}
\end{equation}

where $f_{\text{emit}}^{(n+1)}$ is the next emission frequency, $f_{\text{ref}} = 83$ kHz is the reference (foveal) frequency, $c = 343$ m/s is the speed of sound, $v_r^{(n)}$ is the radial velocity at pulse $n$, $\theta^{(n)}$ is the angle between the velocity vector and the target direction, $\eta$ is the feedback gain (measured $\eta \approx 0.95$ in *R. ferrumequinum*; Schuller et al., 1974), and $f_{\text{echo}}^{(n)}$ is the measured echo frequency. The steady-state error satisfies $|f_{\text{ref}} - f_{\text{echo}}| < 0.05\% \cdot f_{\text{ref}}$.

### Equation 3: Bat Sonar Range-Doppler Ambiguity Function (CF-FM Pulse)

\begin{equation}
\chi(\tau, f_d) = \int_{-\infty}^{\infty} s_{\text{CF-FM}}(t) \cdot s_{\text{CF-FM}}^*(t + \tau) \cdot e^{j2\pi f_d t} \, dt \label{eq:ambiguity}
\end{equation}

where $s_{\text{CF-FM}}(t) = A \cdot \text{rect}\left(\frac{t}{T}\right) \cdot \left[ e^{j2\pi f_c t} + e^{j2\pi (f_c + \alpha t) t} \right]$ is the CF-FM pulse model, $f_c = 83$ kHz is the CF component, $\alpha$ is the FM sweep rate (typically 10–20 kHz/ms), $T$ is the pulse duration (10–50 ms for CF bats), $\tau$ is the time delay, and $f_d$ is the Doppler shift. The ambiguity function for CF-FM pulses exhibits a thumbtack-like central peak with range resolution $\Delta r = c/(2B_{\text{FM}})$ where $B_{\text{FM}}$ is the FM bandwidth (typically 5–10 kHz), and Doppler resolution $\Delta v = c/(2f_c T_{\text{CF}})$ where $T_{\text{CF}}$ is the CF duration.

### Equation 4: Neural Delay-Tuning Curve (Inferior Colliculus)

\begin{equation}
R(\tau) = R_0 + R_{\text{max}} \cdot \exp\left( -\frac{(\tau - \tau_{\text{BD}})^2}{2\sigma_\tau^2} \right) \label{eq:delay_tuning}
\end{equation}

where $R(\tau)$ is the firing rate of a delay-tuned neuron in the inferior colliculus as a function of echo delay $\tau$, $R_0$ is the spontaneous firing rate (typically 5–10 spikes/s), $R_{\text{max}}$ is the peak firing rate (50–200 spikes/s), $\tau_{\text{BD}}$ is the best delay (range: 0.5–20 ms, corresponding to target ranges of 8.6 cm to 3.4 m), and $\sigma_\tau$ is the tuning width (typically 0.1–0.5 ms). Source: O'Neill & Suga (1982), *J. Neurosci.*

### Equation 5: 3D Hippocampal Place Field Model

\begin{equation}
f(\mathbf{p}) = f_0 + f_{\text{max}} \cdot \exp\left( -\frac{(x - x_0)^2}{2\sigma_x^2} - \frac{(y - y_0)^2}{2\sigma_y^2} - \frac{(z - z_0)^2}{2\sigma_z^2} \right) \label{eq:place_field_3d}
\end{equation}

where $f(\mathbf{p})$ is the firing rate at position $\mathbf{p} = (x, y, z)$, $\mathbf{p}_0 = (x_0, y_0, z_0)$ is the place field centre, $f_0$ is the baseline firing rate, $f_{\text{max}}$ is the peak rate, and $\sigma_x, \sigma_y, \sigma_z$ are the field dimensions. In flying bats, place fields are approximately isotropic: $\sigma_x \approx \sigma_y \approx \sigma_z \approx 30$ cm (Yartsev & Ulanovsky, 2013).

---

## 3. ALGORITHMS OR METHODS (minimum 2)

### Algorithm 1: Bio-Inspired Doppler Shift Compensation (DSC) for Drone Sonar

```
Algorithm: Bio-Inspired Doppler Shift Compensation for Drone Ego-Velocity Estimation

Input: 
  - Transmitted pulse s(t) at carrier frequency f_c = 40 kHz
  - Received echo signal r(t) sampled at f_s = 500 kHz
  - Reference frequency f_ref (set to f_c for stationary targets)
  - Feedback gain eta (default 0.9)
  - Pulse repetition interval T_PRI = 10 ms (100 Hz PRF)

Output:
  - Radial velocity estimate v_r_hat
  - Compensated emission frequency f_emit_next
  - Range estimate r_hat

Procedure:
  1. TRANSMIT: Emit CF pulse s(t) = A * cos(2*pi*f_emit*t) for duration T_pulse = 1 ms
  
  2. RECEIVE: Sample echo r(t) for T_window = 10 ms (range gate up to 1.7 m)
  
  3. MATCHED FILTER: 
     h(t) = s*(-t)  // Matched filter impulse response
     y(t) = conv(r(t), h(t))  // Filter output
     
  4. RANGE ESTIMATION:
     t_peak = argmax_t |y(t)|  // Echo arrival time
     r_hat = c * t_peak / 2  // Range in meters
     
  5. DOPPLER ESTIMATION (Phase Method):
     phi_echo = angle(y(t_peak))  // Phase at peak
     phi_ref = angle(s(t)) at t = 0  // Reference phase
     Delta_phi = phi_echo - phi_ref  // Phase difference
     f_d_hat = Delta_phi / (2*pi * T_PRI)  // Doppler shift in Hz
     v_r_hat = f_d_hat * c / (2 * f_emit)  // Radial velocity in m/s
     
  6. DSC CONTROL LAW:
     f_error = f_ref - (f_emit + f_d_hat)  // Frequency error
     f_emit_next = f_emit + eta * f_error  // Compensated emission
     
  7. CONSTRAINTS:
     if f_emit_next < f_min: f_emit_next = f_min  // Lower bound
     if f_emit_next > f_max: f_emit_next = f_max  // Upper bound
     
  8. RETURN: v_r_hat, f_emit_next, r_hat
```

**Biological Basis:** This algorithm directly mimics the DSC behaviour of *R. ferrumequinum* (Schuller et al., 1974). The feedback gain $\eta = 0.9$ is slightly lower than the biological value ($\eta \approx 0.95$) to ensure stability in the presence of motor noise. The phase-based Doppler estimation replaces the biological cochlear frequency analysis with a computationally efficient method suitable for ARM Cortex-M4 processors.

### Algorithm 2: Bio-Inspired Delay-Tuned Neural Network for Range Estimation

```
Algorithm: Delay-Tuned Neural Network for Sonar Range Estimation

Inspiration: Delay-tuned combination-sensitive neurons in the bat inferior colliculus 
and auditory cortex (O'Neill & Suga, 1982; Suga, 1990)

Architecture:
  - Input layer: 100 LIF neurons encoding echo arrival time via TTFS
  - Delay layer: 50 coincidence detector neurons, each tuned to a specific delay
  - Output layer: Range estimate via population vector decoding

Input Encoding (Time-to-First-Spike):
  For each echo sample at time t_i:
    I_stim(t_i) = |y(t_i)| / max(|y|)  // Normalized matched filter output
    t_spike = t_0 + tau * ln(I_0 / (I_0 - I_stim))  // TTFS encoding
    If I_stim > threshold: emit spike at t_spike

Delay Layer (Coincidence Detection):
  For each delay-tuned neuron j with best delay tau_BD_j:
    V_j(t) = sum_i w_ij * K(t - t_i) * K(t - (t_i + tau_BD_j))  // Coincidence
    If V_j(t) > V_th: fire spike at time t
    
  Where K(t) = (t/tau_s) * exp(1 - t/tau_s) is the synaptic kernel
  tau_s = 0.5 ms (synaptic time constant)
  
  Best delays: tau_BD_j in [0.5, 20] ms, linearly spaced (50 neurons)
  Corresponding ranges: r_j = c * tau_BD_j / 2 in [0.086, 3.43] m

Population Vector Decoding:
  For each detected target:
    n_j = number of spikes from neuron j in response window
    r_hat = (sum_j n_j * r_j) / (sum_j n_j)  // Weighted average
    confidence = sum_j n_j / max_possible_spikes
    
  If confidence > threshold: declare detection at range r_hat

Learning (STDP for Synaptic Weights):
  For each pre-post spike pair with interval Delta_t = t_post - t_pre:
    If Delta_t > 0:  // Causal (pre before post)
      Delta_w = A_plus * exp(-Delta_t / tau_plus)
    Else:  // Acausal (post before pre)
      Delta_w = -A_minus * exp(Delta_t / tau_minus)
    w_ij = w_ij + Delta_w
    Clip w_ij to [w_min, w_max]
  
  Parameters: A_plus = 0.01, A_minus = 0.012, tau_plus = 20 ms, tau_minus = 20 ms

Complexity:
  - Operations per pulse: O(N_delay * N_input) = O(50 * 100) = 5000 operations
  - Memory: 50 * 100 = 5000 synapses, ~20 KB (4-byte weights)
  - Suitable for real-time on Cortex-M4 at 100 Hz PRF
```

**Biological Basis:** This algorithm mimics the delay-tuned neurons found in the bat inferior colliculus and auditory cortex (O'Neill & Suga, 1982; Portfors & Wenstrup, 1999). The coincidence detection mechanism is biologically plausible: bat IC neurons exhibit facilitated responses when a pulse-echo pair arrives with a specific delay, and suppressed responses otherwise. The STDP learning rule (Bi & Poo, 1998) allows the network to adapt to new environments without supervised training.

---

## 4. BIBTEX REFERENCES (minimum 5)

```bibtex
@article{Schuller1974,
  author = {Schuller, G. and Beuter, K. and Schnitzler, H.-U.},
  title = {Response to frequency shifted artificial echoes in the bat {Rhinolophus ferrumequinum}},
  journal = {Journal of Comparative Physiology},
  volume = {89},
  pages = {275--286},
  year = {1974},
  doi = {10.1007/BF00694787}
}

@article{ONeill1982,
  author = {O'Neill, W. E. and Suga, N.},
  title = {Encoding of target range and its representation in the auditory cortex of the mustached bat},
  journal = {Journal of Neuroscience},
  volume = {2},
  number = {1},
  pages = {17--31},
  year = {1982},
  doi = {10.1523/JNEUROSCI.02-01-00017.1982}
}

@article{Yartsev2013,
  author = {Yartsev, M. M. and Ulanovsky, N.},
  title = {Representation of three-dimensional space in the hippocampus of flying bats},
  journal = {Science},
  volume = {340},
  number = {6130},
  pages = {367--372},
  year = {2013},
  doi = {10.1126/science.1235338}
}

@article{Schnitzler2011,
  author = {Schnitzler, H.-U. and Denzinger, A.},
  title = {Auditory fovea and Doppler shift compensation: adaptations for flutter detection in echolocating bats using {CF-FM} signals},
  journal = {Journal of Comparative Physiology A},
  volume = {197},
  pages = {541--559},
  year = {2011},
  doi = {10.1007/s00359-010-0569-6}
}

@article{Wilson1983,
  author = {Wilson, J. P. and Bruns, V.},
  title = {Basilar membrane tuning properties in the specialised cochlea of the {CF-bat}, {Rhinolophus ferrumequinum}},
  journal = {Hearing Research},
  volume = {10},
  number = {1},
  pages = {15--35},
  year = {1983},
  doi = {10.1016/0378-5955(83)90074-3}
}

@article{Bi1998,
  author = {Bi, G.-Q. and Poo, M.-M.},
  title = {Synaptic modifications in cultured hippocampal neurons: Dependence on spike timing, synaptic strength, and postsynaptic cell type},
  journal = {Journal of Neuroscience},
  volume = {18},
  number = {24},
  pages = {10464--10472},
  year = {1998},
  doi = {10.1523/JNEUROSCI.18-24-10464.1998}
}

@article{Hafting2005,
  author = {Hafting, T. and Fyhn, M. and Molden, S. and Moser, M.-B. and Moser, E. I.},
  title = {Microstructure of a spatial map in the entorhinal cortex},
  journal = {Nature},
  volume = {436},
  pages = {801--806},
  year = {2005},
  doi = {10.1038/nature03721}
}

@article{Muller2024BatDeck,
  author = {M\"uller, H. and Kartsch, V. and Magno, M. and Benini, L.},
  title = {{BatDeck}: Advancing nano-drone navigation with low-power ultrasound-based obstacle avoidance},
  journal = {arXiv preprint arXiv:2403.16696},
  year = {2024}
}

@article{Velmurugan2026,
  author = {Velmurugan, M. and Brush, P. and Balfour, C. and Przybyla, R. J. and Sanket, N. J.},
  title = {MilliWatt ultrasound for navigation in visually degraded environments on palm-sized aerial robots},
  journal = {Science Robotics},
  volume = {11},
  number = {112},
  year = {2026}
}

@article{Au1993,
  author = {Au, W. W. L.},
  title = {The sonar of dolphins},
  journal = {Springer-Verlag, New York},
  year = {1993},
  doi = {10.1007/978-1-4612-4356-4}
}

@article{Suga1990,
  author = {Suga, N.},
  title = {Biosonar and neural computation in bats},
  journal = {Scientific American},
  volume = {262},
  number = {6},
  pages = {60--69},
  year = {1990}
}

@article{Portfors1999,
  author = {Portfors, C. V. and Wenstrup, J. J.},
  title = {Delay-tuned neurons in the inferior colliculus of the mustached bat: implications for analyses of target range},
  journal = {Journal of Neurophysiology},
  volume = {82},
  number = {3},
  pages = {1326--1338},
  year = {1999},
  doi = {10.1152/jn.1999.82.3.1326}
}

@article{Metzner1993,
  author = {Metzner, W.},
  title = {An audio-vocal interface in echolocating horseshoe bats},
  journal = {Journal of Neuroscience},
  volume = {13},
  number = {5},
  pages = {1899--1915},
  year = {1993},
  doi = {10.1523/JNEUROSCI.13-05-01899.1993}
}

@article{Ginosar2021,
  author = {Ginosar, G. and Finkelstein, A. and Las, L. and Ulanovsky, N.},
  title = {The 3{D} geometry of grid cells in flying bats},
  journal = {Nature Neuroscience},
  volume = {24},
  pages = {1146--1157},
  year = {2021},
  doi = {10.1038/s41593-021-00879-9}
}
```

---

## 5. INTEGRATION NOTES (200+ words)

### How Domain Contributions Connect to the Paper's Overall System

The biological principles described above map directly onto the engineering components of the proposed bat-inspired drone navigation system. The following mappings are critical for the paper's technical architecture:

**1. Acoustic Fovea to Matched Filter Bank:** The acoustic fovea of *R. ferrumequinum* provides the biological template for the matched filter bank used in the sonar receiver (Chapter 3). Just as the fovea provides hyper-acute frequency discrimination around 83 kHz, the engineered system should implement a narrowband filter centred at 40 kHz with high Q-factor (Q \u2265 50) for Doppler estimation, complemented by a broadband filter (B = 5 kHz) for range resolution. This dual-filter architecture — inspired by the CF-FM dichotomy — is absent from existing sonar systems (Müller et al., 2024) and represents a key innovation.

**2. DSC to Adaptive Carrier Tracking:** The Doppler shift compensation control law (Equation 2) provides the mathematical framework for the Doppler-aware EKF measurement model (Chapter 4). The biological feedback gain $\eta \approx 0.95$ can be used as an initial value for the Kalman filter's velocity innovation covariance, with adaptation via online noise covariance estimation (Ben-David & Indelman, 2022).

**3. Delay-Tuned Neurons to Range-Gating:** The delay-tuned neurons in the bat inferior colliculus (Algorithm 2) directly inspire the range-gating and pulse-compression algorithms in the sonar signal processing pipeline (Chapter 3). The population vector decoding approach — weighting multiple delay-tuned channels by their spike counts — is computationally efficient and robust to multipath interference, as demonstrated by Vanderelst et al. (2016) in robotic implementations.

**4. Hippocampal Place Cells to SLAM Landmarks:** The 3D volumetric place fields of bat hippocampal neurons (Equation 5) provide a biological justification for the 3D point-feature representation in FastSLAM 2.0 (Chapter 5). The isotropic field dimensions ($\sigma \approx 30$ cm) suggest that sonar landmarks should be represented with approximately spherical uncertainty ellipsoids, rather than the elongated ellipsoids typical of vision-based SLAM.

**5. Grid Cells to Metric Space Representation:** The grid cell system in the bat entorhinal cortex (Hafting et al., 2005; Ginosar et al., 2021) provides a biological analogue for the metric coordinate frame in SLAM. The multiple spatial scales of grid cells (30 cm to > 100 cm spacing) suggest a hierarchical mapping approach: fine-scale maps for local obstacle avoidance and coarse-scale maps for global navigation.

**6. Multi-Sensory Integration in Superior Colliculus:** The convergence of auditory, visual, and vestibular inputs onto single neurons in the bat superior colliculus (Meredith & Stein, 1986) provides the biological motivation for the multi-modal sensor fusion framework (Chapter 4). The spatially aligned receptive fields across modalities suggest that the EKF's measurement models should be calibrated to produce congruent estimates — a principle that guides the asynchronous fusion of sonar (20 Hz), IMU (200 Hz), and optical flow (30 Hz) measurements.

**Critical Caveat for Engineers:** It is essential to note that the bat cochlea is not a simple frequency analyser. The acoustic fovea is a discrete, mechanically specialised structure with a stiffness discontinuity that no standard cochlear model (e.g., Greenwood, 1990) predicts. Engineers designing matched filter banks should model this as a discrete narrowband resonance superimposed on a broadband gradient, not as a continuous tonotopic map. Failure to do so will result in suboptimal filter design, particularly for Doppler estimation where the foveal precision is most critical.

---

## Summary of Domain Contributions

| Component | Biological Inspiration | Engineering Mapping | Key Reference |
|-----------|----------------------|---------------------|---------------|
| Acoustic fovea | *R. ferrumequinum* basilar membrane stiffness discontinuity | Narrowband matched filter (Q \u2265 50) at 40 kHz | Wilson & Bruns (1983) |
| DSC control loop | Frequency-tracking servo with $\eta \approx 0.95$ | Adaptive carrier tracking in Doppler-aware EKF | Schuller et al. (1974) |
| Delay-tuned neurons | IC coincidence detectors with best delays 0.5–20 ms | Range-gating with population vector decoding | O'Neill & Suga (1982) |
| 3D place cells | Hippocampal volumetric firing fields ($\sigma \approx 30$ cm) | 3D point features with isotropic uncertainty | Yartsev & Ulanovsky (2013) |
| Grid cells | Entorhinal metric coordinates (30–100 cm spacing) | Hierarchical SLAM with multiple spatial scales | Hafting et al. (2005) |
| Multi-sensory integration | SC convergence of auditory, visual, vestibular | Asynchronous EKF with congruent measurement models | Meredith & Stein (1986) |

---

**END OF DOMAIN CONTRIBUTION**