# Domain Contribution: Neuroethology, Biological Sensing & Bio-Inspired Systems

## 1. TECHNICAL ANALYSIS (500+ words)

### State-of-the-Art in Bat Echolocation and Neural Computation for Navigation

The greater horseshoe bat (*Rhinolophus ferrumequinum*) represents the gold standard for bio-inspired sonar navigation, operating with a sensory-motor control loop that outperforms any engineered system in its weight class. The animal emits CF-FM pulses centered near 83 kHz, with the constant-frequency (CF) component lasting 10–100 ms and the frequency-modulated (FM) sweep covering approximately 10–20 kHz bandwidth (Schnitzler and Denzinger, 2011). The CF component enables Doppler shift detection with a precision of 0.01–0.05%, while the FM component provides range resolution of approximately 1–3 cm via echo delay estimation (Moss and Surlykke, 2001).

**The Acoustic Fovea.** The defining specialization of rhinolophid bats is the acoustic fovea: a mechanically stiffened, expanded region of the basilar membrane covering approximately 30% of its length while representing only a 3–4 kHz bandwidth centered on the resting echo frequency of ~83 kHz (Neuweiler, 1980; Vater and Kössl, 2011). This structure provides a frequency resolution of 0.1–0.3%—an order of magnitude finer than the generic mammalian cochlea. The fovea arises from a discrete stiffness discontinuity in the basilar membrane, with the thickness-to-width ratio changing abruptly at the foveal boundary (Duifhuis and Vater, 1985). This is not a smooth tonotopic gradient; it is a mechanical matched filter. The engineering analogue is the Rihaczek matched filter (Rihaczek, 1969), but the biological implementation achieves its selectivity through passive mechanics alone, without the computational overhead of digital correlation.

**Doppler Shift Compensation (DSC).** DSC is the most precise closed-loop frequency-tracking control system in the animal kingdom. As the bat approaches a target, the echo returns Doppler-shifted upward by Δf = 2f₀v/c, where v is the approach velocity. Within 50–100 ms, the bat lowers its emission frequency by exactly the expected Doppler offset, so that the echo always lands on the 83 kHz fovea (Schnitzler, 1968; Schuller et al., 1974). The control loop achieves steady-state accuracy of ±0.02% with zero overshoot—a performance characteristic that would require a Type II servo with carefully tuned damping in an engineered system. The neural substrate involves the superior olivary complex (SOC) for frequency comparison, the paralemniscal tegmental area for vocal-motor control, and the auditory cortex for reference frequency maintenance (Metzner, 1993; Smotherman, 2007).

**Neural Computation for 3D Spatial Mapping.** The bat auditory system computes 3D space through a hierarchical processing chain. In the inferior colliculus (IC), delay-tuned neurons respond selectively to specific pulse-echo delays, encoding target range with precision down to 1–2 cm (Portfors and Wenstrup, 1999). Binaural neurons in the IC compute interaural time differences (ITDs) and interaural level differences (ILDs) for azimuthal localization, with ITD sensitivity down to 10–20 μs (Grothe et al., 2001). The auditory cortex contains combination-sensitive neurons that respond to specific pulse-echo pairs, enabling clutter rejection and surface texture classification (Suga, 1990; Fitzpatrick et al., 1993). At the highest level, hippocampal place cells in bats fire when the animal occupies a specific location in 3D space, providing an allocentric cognitive map (Ulanovsky and Moss, 2007; Yartsev and Ulanovsky, 2013). Entorhinal grid cells impose a metric coordinate frame on this map, functioning as a neural odometer with hexagonal firing fields (Ginosar et al., 2021).

**Cross-Species Comparisons.** Dolphin biosonar (*Tursiops truncatus*) uses broadband click trains (40–150 kHz) with inter-click intervals that encode target range; the melon serves as an acoustic lens for beamforming with a beamwidth of approximately 10° (Au, 1993). Blind Mexican cave fish (*Astyanax mexicanus*) use the lateral line system—an array of mechanosensory hair-cell neuromasts—for hydrodynamic imaging of nearby obstacles, analogous to a passive sonar array with a detection range of 2–5 body lengths (Windsor et al., 2008). Weakly electric fish (*Eigenmannia virescens*) perform active electrolocation with a quasi-sinusoidal electric organ discharge (EOD) at 200–600 Hz, detecting distortions in the self-generated electric field via electroreceptor ampullae; the jamming avoidance response (JAR) shifts EOD frequency away from conspecifics, providing a biological analogue of frequency-division multiple access (FDMA) (Heiligenberg, 1991).

**Known Failure Modes in Engineering Approximations.** The most common error in bio-inspired sonar papers is conflating the acoustic fovea with a generic tonotopic gradient. Standard cochlear models (e.g., Greenwood, 1990) predict a logarithmic frequency map, but the fovea violates this with a discrete, mechanically specialized region. Engineers who model the bat cochlea as a simple filter bank miss the key insight: the fovea is a *matched filter* that trades bandwidth for sensitivity at the behaviorally critical frequency. A second failure mode is ignoring the active control loop of DSC; many systems use fixed-frequency sonar and miss the adaptive carrier-frequency tracking that gives bats their robustness to Doppler shifts. A third failure is neglecting the multi-modal integration: bats combine echolocation with vision (in dim light) and inertial sensing (via the vestibular system), and the neural circuits for this fusion are tightly coupled, not loosely coupled as in most engineered systems.

---

## 2. EQUATIONS (LaTeX-ready)

### Equation 1: Basilar Membrane Frequency Map with Acoustic Fovea

egin{equation}
f(x) = 
egin{cases}
f_0 cdot 10^{(x - x_0)/L_{	ext{base}}}, & 0 leq x < x_{	ext{fovea}} \
f_{	ext{fovea}} + Delta f_{	ext{fovea}} cdot frac{x - x_{	ext{fovea}}}{L_{	ext{fovea}}}, & x_{	ext{fovea}} leq x leq x_{	ext{fovea}} + L_{	ext{fovea}} \
f_0 cdot 10^{(x - x_0 - L_{	ext{fovea}})/L_{	ext{apex}}}, & x > x_{	ext{fovea}} + L_{	ext{fovea}}
end{cases}
label{eq:bm_fovea_map}
end{equation}

Where:
- $f(x)$ is the characteristic frequency at basilar membrane position $x$ (mm from base)
- $f_0 = 83$ kHz is the foveal center frequency for *Rhinolophus ferrumequinum*
- $x_{	ext{fovea}}$ is the start of the foveal region (~2.5 mm from base)
- $L_{	ext{fovea}} approx 4.5$ mm is the foveal length (30% of total BM length of ~15 mm)
- $Delta f_{	ext{fovea}} approx 3$ kHz is the frequency range represented in the fovea
- $L_{	ext{base}}$ and $L_{	ext{apex}}$ are the space constants for the non-foveal regions
- The foveal slope $Delta f_{	ext{fovea}} / L_{	ext{fovea}} approx 0.67$ kHz/mm is ~10× shallower than the non-foveal gradient, giving hyper-acute frequency discrimination

### Equation 2: Doppler Shift Compensation Control Loop

egin{equation}
f_{	ext{emit}}(t+1) = f_{	ext{ref}} - frac{2 f_{	ext{ref}} v(t)}{c} - K_p left( f_{	ext{echo}}(t) - f_{	ext{ref}} ight) - K_i sum_{	au=0}^{t} left( f_{	ext{echo}}(	au) - f_{	ext{ref}} ight) Delta t
label{eq:dsc_control}
end{equation}

Where:
- $f_{	ext{emit}}(t+1)$ is the next emitted pulse CF frequency
- $f_{	ext{ref}} approx 83$ kHz is the reference frequency maintained by the bat
- $v(t)$ is the approach velocity at time $t$
- $c = 343$ m/s is the speed of sound
- $f_{	ext{echo}}(t)$ is the received echo CF frequency
- $K_p$ is the proportional gain (neural analogue: SOC frequency comparator)
- $K_i$ is the integral gain (neural analogue: auditory cortex reference maintenance)
- $Delta t$ is the inter-pulse interval (typically 10–100 ms)
- The biological system achieves $K_p approx 0.95$, $K_i approx 0.05$, yielding zero steady-state error with no overshoot

### Equation 3: Delay-Tuned Neuron Response in Inferior Colliculus

egin{equation}
R(	au) = R_0 + A cdot expleft( -frac{(	au - 	au_{	ext{best}})^2}{2sigma_{	au}^2} ight) cdot left[ 1 + alpha cdot cosleft( 2pi f_{	ext{CF}} 	au + phi ight) ight]
label{eq:delay_tuned}
end{equation}

Where:
- $R(	au)$ is the firing rate (spikes/s) as a function of echo delay $	au$
- $R_0$ is the spontaneous firing rate (typically 5–15 spikes/s)
- $A$ is the peak amplitude of the delay-tuned response
- $	au_{	ext{best}}$ is the best delay (typically 1–20 ms, corresponding to 0.17–3.4 m range)
- $sigma_{	au}$ is the delay tuning width (typically 0.5–2 ms, giving range resolution of 8.5–34 cm)
- $f_{	ext{CF}}$ is the CF component frequency (~83 kHz)
- $alpha$ is the modulation depth of the phase-sensitive component (0 ≤ α ≤ 1)
- $phi$ is the phase offset
- The cosine term models the phase-locking observed in IC neurons to the fine structure of the CF component

### Equation 4: Hippocampal Place Cell Firing Field in 3D

egin{equation}
P(mathbf{x} | mathbf{x}_{	ext{center}}, oldsymbol{Sigma}) = P_{	ext{max}} cdot expleft( -frac{1}{2} (mathbf{x} - mathbf{x}_{	ext{center}})^T oldsymbol{Sigma}^{-1} (mathbf{x} - mathbf{x}_{	ext{center}}) ight)
label{eq:place_field_3d}
end{equation}

Where:
- $P(mathbf{x})$ is the firing probability at 3D position $mathbf{x} = [x, y, z]^T$
- $mathbf{x}_{	ext{center}}$ is the place field center (the location where the cell fires maximally)
- $oldsymbol{Sigma}$ is the 3×3 covariance matrix defining the field shape and orientation
- $P_{	ext{max}}$ is the peak firing rate (typically 10–30 Hz in bat CA1)
- In bats, place fields are isotropic in the horizontal plane ($sigma_x approx sigma_y approx 30$–50 cm) but elongated vertically ($sigma_z approx 50$–100 cm), reflecting the 3D nature of flight (Yartsev and Ulanovsky, 2013)

### Equation 5: Jamming Avoidance Response Frequency Shift

egin{equation}
Delta f_{	ext{EOD}} = 
egin{cases}
+Delta f_{	ext{max}} cdot 	anhleft( frac{f_{	ext{neighbor}} - f_{	ext{self}}}{Delta f_{	ext{threshold}}} ight), & f_{	ext{neighbor}} > f_{	ext{self}} \
-Delta f_{	ext{max}} cdot 	anhleft( frac{f_{	ext{self}} - f_{	ext{neighbor}}}{Delta f_{	ext{threshold}}} ight), & f_{	ext{neighbor}} < f_{	ext{self}}
end{cases}
label{eq:jar_frequency}
end{equation}

Where:
- $Delta f_{	ext{EOD}}$ is the change in electric organ discharge frequency
- $f_{	ext{self}}$ is the fish's own EOD frequency (typically 200–600 Hz for *Eigenmannia*)
- $f_{	ext{neighbor}}$ is the neighbor's EOD frequency
- $Delta f_{	ext{max}} approx 10$–15 Hz is the maximum frequency shift
- $Delta f_{	ext{threshold}} approx 3$–5 Hz is the frequency difference threshold for JAR initiation
- The sign convention: the fish raises its frequency if the neighbor is lower, and lowers it if the neighbor is higher, thus increasing the frequency separation

---

## 3. ALGORITHMS OR METHODS

### Algorithm 1: Bio-Mimetic Doppler Shift Compensation for Drone Sonar

```
Input: 
  - f_emit: current emitted sonar frequency (Hz)
  - f_echo: received echo frequency (Hz)
  - f_ref: reference frequency (target echo frequency, e.g., 40 kHz)
  - v_est: estimated approach velocity from IMU (m/s)
  - c: speed of sound (343 m/s)
  - K_p, K_i: proportional and integral gains
  - Δt: inter-pulse interval (s)
  - integral_error: accumulated frequency error (persistent state)

Output:
  - f_emit_next: next emitted frequency (Hz)
  - updated integral_error

1. Compute Doppler shift from velocity:
   f_doppler = 2 * f_ref * v_est / c

2. Compute frequency error relative to reference:
   f_error = f_echo - f_ref

3. Update integral term:
   integral_error = integral_error + f_error * Δt

4. Compute frequency adjustment:
   f_adjust = K_p * f_error + K_i * integral_error

5. Set next emitted frequency:
   f_emit_next = f_ref - f_doppler - f_adjust

6. Apply frequency bounds:
   f_emit_next = clamp(f_emit_next, f_min, f_max)
   // f_min = f_ref - 2 kHz, f_max = f_ref + 0.5 kHz (bat-like asymmetry)

7. Return f_emit_next, integral_error

Note: The biological DSC achieves steady-state accuracy of ±0.02% within 50-100 ms.
For a 40 kHz sonar, this corresponds to ±8 Hz accuracy.
```

### Algorithm 2: Bio-Inspired Echo Processing Pipeline with Combination-Sensitive Detection

```
Input:
  - s(t): raw ultrasonic recording (sampled at f_s ≥ 200 kHz)
  - pulse_template: known emitted pulse waveform
  - τ_min, τ_max: minimum and maximum echo delays (range gate)
  - SNR_threshold: minimum SNR for detection (e.g., 6 dB)

Output:
  - echo_list: list of detected echoes with {delay, amplitude, Doppler shift, texture}

1. Matched Filtering (Cochlear Analogue):
   a. Compute cross-correlation: R(τ) = ∫ s(t) * pulse_template(t - τ) dt
   b. Normalize: R_norm(τ) = R(τ) / sqrt(∫ |pulse_template|² dt * ∫ |s(t)|² dt)
   c. Apply bandpass filter bank centered on f_ref ± 3 kHz (foveal analogue)
   d. Extract envelope: E(τ) = |Hilbert(R_norm(τ))|

2. Delay-Tuned Detection (IC Analogue):
   a. Identify peaks in E(τ) for τ ∈ [τ_min, τ_max]
   b. For each peak at delay τ_i:
      - Compute SNR_i = 20 * log10(E(τ_i) / noise_floor)
      - If SNR_i < SNR_threshold: reject
      - Compute range: r_i = c * τ_i / 2
      - Compute Doppler shift from phase: f_D_i = (1/(2π)) * dφ/dτ at τ_i

3. Combination-Sensitive Verification (Auditory Cortex Analogue):
   a. For each detected echo, form pulse-echo pair (pulse at t=0, echo at t=τ_i)
   b. Compute spectrogram of the pair: S(t, f) = |STFT(s(t) * window(t - τ_i/2))|
   c. Classify echo type using pre-trained CNN (see Chapter 6):
      - Surface type: {wall, foliage, glass, human, clutter}
      - Target strength: σ_target = (4π)³ * SNR * R⁴ * kT₀BF / (P_T G_T G_R λ²)
   d. Assign confidence score based on combination-sensitive neuron model:
      C_i = σ( w_1 * SNR_i + w_2 * |f_D_i| + w_3 * texture_score_i + b )

4. Multi-Echo Integration (Spatial Scene Analysis):
   a. Group echoes by azimuth (from binaural ITD/ILD cues)
   b. Update occupancy grid map (see Chapter 4)
   c. Identify potential obstacles with range < safety_threshold

5. Return echo_list with {range, azimuth, Doppler, texture, confidence}
```

### Algorithm 3: Bio-Inspired Multi-Modal Fusion with Adaptive Sensor Weighting

```
Input:
  - x_t: current state estimate (pose, velocity)
  - z_sonar: sonar range measurements {r_i, θ_i, φ_i}
  - z_IMU: IMU measurements {a_x, a_y, a_z, ω_x, ω_y, ω_z}
  - z_optical: optical flow measurements {v_x, v_y}
  - R_sonar, R_IMU, R_optical: nominal measurement noise covariances
  - Q: process noise covariance
  - sensor_health: {sonar: 0-1, IMU: 0-1, optical: 0-1}

Output:
  - x_{t+1}: updated state estimate
  - P_{t+1}: updated state covariance

1. IMU Propagation (Vestibular Analogue):
   a. Predict state using IMU measurements:
      x_pred = f(x_t, z_IMU)  // motion model
   b. Propagate covariance:
      P_pred = F * P_t * F^T + Q

2. Adaptive Sensor Weighting (Bat Attention Analogue):
   a. For each sensor modality i:
      - Compute innovation: ν_i = z_i - h_i(x_pred)
      - Compute innovation covariance: S_i = H_i * P_pred * H_i^T + R_i
      - Compute Mahalanobis distance: d_i² = ν_i^T * S_i^{-1} * ν_i
      - Update sensor health: health_i = exp(-d_i² / (2 * χ²_threshold))
      - Adjust measurement noise: R_i_eff = R_i / (health_i + ε)
   b. Normalize health weights: w_i = health_i / Σ health_i

3. Multi-Modal Update (Echolocation + Vision + Inertial Fusion):
   a. For each sensor with w_i > 0.1:
      - Compute Kalman gain: K_i = P_pred * H_i^T * (H_i * P_pred * H_i^T + R_i_eff)^{-1}
      - Update state: x_pred = x_pred + K_i * ν_i
      - Update covariance: P_pred = (I - K_i * H_i) * P_pred
   b. Apply sequential update (all sensors processed in order of decreasing w_i)

4. Echo-Adaptive Horizon Adjustment:
   a. Compute average echo SNR over last N pulses
   b. Adjust sensing horizon:
      R_max = R_0 + ΔR * tanh((SNR_avg - SNR_th) / SNR_th)
   c. Adjust pulse repetition rate:
      PRF = PRF_min + (PRF_max - PRF_min) * (1 - exp(-SNR_avg / SNR_ref))

5. Return x_pred, P_pred
```

---

## 4. BIBTEX REFERENCES

@article{Neuweiler1980,
  author={Neuweiler, Gerhard},
  title={Auditory processing of echoes: Peripheral processing},
  journal={Journal of the Acoustical Society of America},
  volume={68},
  number={3},
  pages={741--753},
  year={1980},
  doi={10.1121/1.384815}
}

@article{Schnitzler1968,
  author={Schnitzler, Hans-Ulrich},
  title={Die Ultraschall-Ortungslaute der Hufeisen-Flederm{"a}use (Chiroptera-Rhinolophidae) in verschiedenen Orientierungssituationen},
  journal={Zeitschrift f{"u}r vergleichende Physiologie},
  volume={57},
  pages={376--408},
  year={1968},
  doi={10.1007/BF00303062}
}

@article{Schuller1974,
  author={Schuller, Gerd and Beuter, Karl and Schnitzler, Hans-Ulrich},
  title={Response to frequency shifted artificial echoes in the bat, *Rhinolophus ferrumequinum*},
  journal={Journal of Comparative Physiology},
  volume={89},
  pages={275--286},
  year={1974},
  doi={10.1007/BF00694793}
}

@article{Suga1990,
  author={Suga, Nobuo},
  title={Cortical computational maps for auditory imaging},
  journal={Neural Networks},
  volume={3},
  number={1},
  pages={3--21},
  year={1990},
  doi={10.1016/0893-6080(90)90043-K}
}

@article{Portfors1999,
  author={Portfors, Christine V. and Wenstrup, Jeffrey J.},
  title={Delay-tuned neurons in the inferior colliculus of the mustached bat: Implications for analyses of target range},
  journal={Journal of Neurophysiology},
  volume={82},
  number={3},
  pages={1326--1338},
  year={1999},
  doi={10.1152/jn.1999.82.3.1326}
}

@article{Ulanovsky2007,
  author={Ulanovsky, Nachum and Moss, Cynthia F.},
  title={Hippocampal cellular and network activity in freely moving echolocating bats},
  journal={Nature Neuroscience},
  volume={10},
  pages={224--233},
  year={2007},
  doi={10.1038/nn1829}
}

@article{Yartsev2013,
  author={Yartsev, Michael M. and Ulanovsky, Nachum},
  title={Representation of three-dimensional space in the hippocampus of flying bats},
  journal={Science},
  volume={340},
  number={6130},
  pages={367--372},
  year={2013},
  doi={10.1126/science.1232838}
}

@article{Ginosar2021,
  author={Ginosar, Gily and Finkelstein, Arseny and Las, Liora and Ulanovsky, Nachum},
  title={Representation of 3D space in the entorhinal cortex of flying bats},
  journal={Nature},
  volume={596},
  pages={253--258},
  year={2021},
  doi={10.1038/s41586-021-03782-4}
}

@article{Heiligenberg1991,
  author={Heiligenberg, Walter},
  title={The neural basis of behavior: A neuroethological view},
  journal={Annual Review of Neuroscience},
  volume={14},
  pages={247--267},
  year={1991},
  doi={10.1146/annurev.ne.14.030191.001335}
}

@article{Au1993,
  author={Au, Whitlow W. L.},
  title={The sonar of dolphins},
  journal={Springer-Verlag, New York},
  year={1993},
  doi={10.1007/978-1-4612-4356-4}
}

@article{Windsor2008,
  author={Windsor, Shane P. and Tan, David and Montgomery, John C.},
  title={Swimming kinematics and hydrodynamic imaging in the blind Mexican cave fish (*Astyanax fasciatus*)},
  journal={Journal of Experimental Biology},
  volume={211},
  pages={2950--2959},
  year={2008},
  doi={10.1242/jeb.020453}
}

@article{Vater2011,
  author={Vater, Marianne and K{"o}ssl, Manfred},
  title={Comparative aspects of cochlear functional organization in mammals},
  journal={Hearing Research},
  volume={273},
  number={1-2},
  pages={89--99},
  year={2011},
  doi={10.1016/j.heares.2010.05.018}
}

@article{Duifhuis1985,
  author={Duifhuis, Hendrikus and Vater, Marianne},
  title={On the mechanics of the horseshoe bat cochlea},
  journal={Mechanics of Hearing},
  pages={89--96},
  year={1985},
  publisher={Delft University Press}
}

@article{Metzner1993,
  author={Metzner, Walter},
  title={An audio-vocal interface in echolocating horseshoe bats},
  journal={Journal of Neuroscience},
  volume={13},
  number={5},
  pages={1899--1915},
  year={1993},
  doi={10.1523/JNEUROSCI.13-05-01899.1993}
}

@article{Smotherman2007,
  author={Smotherman, Michael},
  title={Sensory feedback control of mammalian vocalizations},
  journal={Behavioural Brain Research},
  volume={182},
  number={2},
  pages={315--326},
  year={2007},
  doi={10.1016/j.bbr.2007.03.008}
}

---

## 5. INTEGRATION NOTES (200+ words)

### How Domain Contributions Connect to the Paper's Overall System

The biological principles detailed above map directly onto the paper's seven core technical chapters, providing the biological ground truth that grounds every engineering approximation.

**Chapter 2 (Bio-Mimetic Bat Model):** The acoustic fovea model (Equation ef{eq:bm_fovea_map}) provides the correct frequency mapping for the bat-inspired sonar transducer. The DSC control loop (Equation ef{eq:dsc_control} and Algorithm 1) replaces the simplistic Doppler compensation in the research briefs with a biologically accurate proportional-integral controller that achieves the bat's characteristic zero-overshoot performance. The head-scanning model in the paper should incorporate the bat's characteristic 8–12 Hz scanning rate with asymmetric amplitude (larger yaw than pitch), which differs from the symmetric scanning assumed in most engineering implementations.

**Chapter 3 (EKF Multi-Modal Fusion):** The adaptive sensor weighting in Algorithm 3 is directly inspired by the bat's ability to dynamically shift attention between echolocation, vision, and vestibular cues based on environmental conditions. The chi-squared gating test mirrors the bat's neural mechanisms for detecting echo degradation (e.g., in heavy clutter or rain). The bat's vestibular system provides a biological template for IMU integration, with semicircular canal dynamics that can be modeled as a second-order high-pass filter with a time constant of ~4–6 seconds.

**Chapter 4 (Acoustic SLAM):** The delay-tuned neuron model (Equation ef{eq:delay_tuned}) provides the biological basis for the range-gating mechanism in the occupancy grid update. The combination-sensitive verification in Algorithm 2 mirrors the bat auditory cortex's ability to reject clutter echoes that do not form coherent pulse-echo pairs. The hippocampal place cell model (Equation ef{eq:place_field_3d}) provides a biological template for the SLAM system's spatial representation, with the key insight that bat place fields are 3D and anisotropic (elongated vertically), which should inform the grid resolution in the occupancy map.

**Chapter 5 (Echo-Adaptive Path Planning):** The bat's foraging behavior—alternating between search, approach, and capture phases with distinct pulse designs—provides a biological template for the adaptive sensing horizon in the RRT* cost function. The bat reduces pulse duration and increases repetition rate during approach (the "buzz