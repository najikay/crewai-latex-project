# Physics Contribution — Matched Filter Theory, LFM Sonar Signal Design, and Acoustic Wave Propagation for Underwater SLAM

## 1. TECHNICAL ANALYSIS (500+ words)

### State-of-the-Art in Matched Filter Theory for Sonar Signal Processing

Matched filter theory constitutes the foundational framework for optimal detection in active sonar systems. The matched filter, derived by North (1943) and generalized by Turin (1960), maximizes the output signal-to-noise ratio (SNR) for a known signal in additive white Gaussian noise (AWGN). For underwater SLAM applications, the matched filter is employed in pulse compression of linear frequency modulated (LFM) chirps, enabling simultaneous high range resolution and long detection range—a trade-off that is fundamental to sonar system design.

The current state-of-the-art in sonar waveform design for underwater SLAM has evolved significantly. Classical approaches use LFM pulses with time-bandwidth products (BT) ranging from 10 to 1000, achieving range resolution Δr = c/(2B) independent of pulse duration τ (Skolnik, 2008). For a typical underwater sonar operating at 200 kHz center frequency with 20 kHz bandwidth, this yields Δr ≈ 3.75 cm—sufficient for feature-level SLAM. However, the Doppler tolerance of LFM waveforms, while superior to phase-coded waveforms, introduces a range-Doppler coupling that must be compensated: the apparent time delay shifts by τ_d = (f_d · τ)/B, where f_d is the Doppler shift (Rihaczek, 1969).

Recent advances have introduced adaptive waveform design techniques. Hayes and Gough (2009) demonstrated that wideband LFM waveforms with BT > 100 achieve near-optimal ambiguity function properties for underwater environments. The Woodward ambiguity function χ(τ, f_d) = ∫ s(t)s*(t+τ)e^{j2πf_d t} dt characterizes the joint range-Doppler resolution, with LFM waveforms exhibiting a characteristic "ridge" ambiguity that provides Doppler tolerance at the cost of range-Doppler coupling.

### Dominant Approaches and Known Failure Modes

Three dominant matched filter implementation approaches exist for sonar systems:

1. **Time-domain convolution**: Direct implementation of h(t) = s*(T-t) with computational complexity O(N²) for N samples. For typical sonar pulses (τ = 1–10 ms at f_s = 500 kHz, N = 500–5000 samples), this is feasible on modern DSPs but becomes prohibitive for real-time systems processing multiple beams.

2. **Frequency-domain matched filtering**: Using FFT-based convolution with complexity O(N log N). This is the dominant approach in modern sonar systems, enabling real-time pulse compression for phased-array beamformers with 64–256 channels.

3. **Stretch processing (deramp)**: For very wideband LFM signals (BT > 1000), stretch processing mixes the received signal with a reference chirp, converting time delay to frequency offset. This approach is particularly effective for synthetic aperture sonar (SAS) systems.

Known failure modes include:

- **Doppler mismatch**: When the target velocity is unknown, the matched filter is mismatched to the Doppler-shifted echo. For LFM waveforms, this manifests as a time shift (range bias) rather than SNR loss, but the bias must be compensated for accurate SLAM. The fractional SNR loss for a Doppler mismatch Δf is approximately (Δf/B)² for small mismatches (Skolnik, 2008).

- **Multipath interference**: In shallow-water environments, multipath arrivals create multiple correlation peaks that corrupt range estimation. The delay spread τ_mp can exceed the pulse duration, causing overlapping echoes that degrade SLAM data association.

- **Reverberation-limited operation**: In cluttered environments, reverberation rather than noise limits detection performance. The reverberation-limited sonar equation SE = SL - 2TL + TS - RL must be used instead of the noise-limited form.

- **Speed of sound uncertainty**: Variations in sound speed (c ≈ 1480–1520 m/s in seawater) due to temperature, salinity, and pressure gradients introduce systematic range errors of 0.5–1.5% if uncorrected. For SLAM over 500 m trajectories, this corresponds to 2.5–7.5 m drift.

### Quantitative Performance Benchmarks

For a typical underwater SLAM sonar (f_c = 200 kHz, B = 20 kHz, τ = 2 ms, BT = 40):
- Range resolution: Δr = c/(2B) = 1500/(2·20000) = 0.0375 m
- SNR gain from matched filtering: G = BT = 40 (16 dB)
- Doppler tolerance: f_d,max ≈ B/τ = 20,000/0.002 = 10 MHz (effectively unlimited for typical AUV velocities < 2 m/s, where f_d < 2·2·200000/1500 ≈ 533 Hz)
- Range-Doppler coupling: Δr_coupling = (f_d · c · τ)/(2B²) ≈ 0.04 m for f_d = 100 Hz

## 2. EQUATIONS (LaTeX-ready)

### Equation 1: Matched Filter Impulse Response and Maximum SNR

The matched filter for a known signal s(t) in AWGN with power spectral density N₀/2 has impulse response h(t) = s*(T - t), where T is the observation interval. The output SNR at the optimal sampling instant t = T is:

\begin{equation}
\text{SNR}_{\text{out}} = \frac{2E}{N_0} = \frac{2}{N_0} \int_{-\infty}^{\infty} |S(f)|^2 \, df
\label{eq:matched_filter_snr}
\end{equation}

where E is the signal energy, S(f) = ℱ{s(t)} is the Fourier transform, and N₀/2 is the two-sided noise power spectral density. This result follows from the Schwarz inequality: the maximum SNR is achieved when the filter transfer function H(f) is proportional to S*(f)e^{-j2πfT} (Turin, 1960, Eq. 2.3; Proakis & Manolakis, 2007, Section 14.2).

### Equation 2: LFM Chirp Signal and Ambiguity Function

The complex envelope of an LFM chirp pulse is:

\begin{equation}
s(t) = \frac{1}{\sqrt{\tau}} \, \text{rect}\left(\frac{t}{\tau}\right) \, e^{j\pi \beta t^2}, \quad \beta = \frac{B}{\tau}
\label{eq:lfm_chirp}
\end{equation}

where τ is the pulse duration, B is the swept bandwidth, β = B/τ is the chirp rate, and rect(t/τ) = 1 for |t| ≤ τ/2 and 0 otherwise. The Woodward ambiguity function for this signal is:

\begin{equation}
\chi(\tau, f_d) = \int_{-\infty}^{\infty} s(t) s^*(t+\tau) e^{j2\pi f_d t} \, dt = \left(1 - \frac{|\tau|}{\tau}\right) \frac{\sin\left[\pi (f_d - \beta\tau)(\tau - |\tau|)\right]}{\pi (f_d - \beta\tau)(\tau - |\tau|)} \, e^{-j\pi f_d \tau}
\label{eq:lfm_ambiguity}
\end{equation}

for |τ| ≤ τ, and zero otherwise. The ambiguity function exhibits the characteristic "ridge" along the line f_d = βτ, indicating the range-Doppler coupling inherent to LFM waveforms (Woodward, 1953, Eq. 7.23; Rihaczek, 1969, Section 6.3).

### Equation 3: Active Sonar Equation with Reverberation Limit

The active sonar equation in noise-limited conditions is:

\begin{equation}
\text{SE} = \text{SL} - 2\text{TL} + \text{TS} - (\text{NL} - \text{DI}) - \text{DT}
\label{eq:active_sonar_noise}
\end{equation}

where SE is the signal excess (dB), SL = 10 log₁₀(P_T / P_ref) + 170.8 dB is the source level for source power P_T in watts referenced to 1 μPa at 1 m, TL = 20 log₁₀(r) + αr is the transmission loss (spherical spreading + absorption), TS = 10 log₁₀(σ/4π) is the target strength for target cross-section σ, NL is the ambient noise level, DI is the directivity index, and DT is the detection threshold. In reverberation-limited conditions, the equation becomes:

\begin{equation}
\text{SE} = \text{SL} - 2\text{TL} + \text{TS} - \text{RL} - \text{DT}
\label{eq:active_sonar_reverb}
\end{equation}

where RL = SL - 2TL + 10 log₁₀(V) + S_v is the reverberation level, V = cτψr²/2 is the reverberation volume for pulse length τ and beamwidth ψ, and S_v is the volume scattering strength (Urick, 1983, Chapter 8; ISO 9613-1, 1993).

### Equation 4: Doppler Shift for Moving Sonar Platform

The received frequency for a moving sonar platform and moving target is:

\begin{equation}
f_r = f_0 \left(\frac{c + v_r}{c + v_s}\right)
\label{eq:doppler_shift}
\end{equation}

where f_0 is the transmitted frequency, c is the speed of sound in the medium, v_r is the velocity of the receiver (positive toward the source), and v_s is the velocity of the source (positive toward the receiver). For the typical case of a monostatic sonar where source and receiver are co-located on the AUV, v_s = v_r = v_auv, and the Doppler shift for an echo from a stationary target is:

\begin{equation}
f_d = f_r - f_0 = f_0 \left(\frac{c + v_{\text{auv}}}{c - v_{\text{auv}}} - 1\right) \approx \frac{2f_0 v_{\text{auv}}}{c} \quad \text{for } v_{\text{auv}} \ll c
\label{eq:doppler_monostatic}
\end{equation}

The approximation error is O((v/c)²), which for v = 2 m/s and c = 1500 m/s is approximately 1.8 × 10⁻⁶, or 0.36 Hz at f_0 = 200 kHz—negligible for SLAM applications (Skolnik, 2008, Section 2.6; ANSI S1.26, 1995).

### Equation 5: Absorption Coefficient in Seawater

The absorption coefficient α in dB/km for seawater follows the Thorp's formula (valid for 1–1000 kHz):

\begin{equation}
\alpha = \frac{0.11 f^2}{1 + f^2} + \frac{44 f^2}{4100 + f^2} + 2.75 \times 10^{-4} f^2 + 0.003
\label{eq:absorption_thorp}
\end{equation}

where f is frequency in kHz. For f = 200 kHz, this yields α ≈ 46.8 dB/km. The transmission loss due to absorption over range r (in km) is TL_abs = α · r dB. The frequency-dependent absorption imposes a fundamental trade-off: higher frequencies provide better range resolution but shorter maximum range (Urick, 1983, Section 3.4; ISO 9613-1, 1993, Annex A).

## 3. ALGORITHMS OR METHODS

### Algorithm 1: Frequency-Domain Matched Filter for LFM Pulse Compression

```
Input: 
  - Received signal x[n], n = 0, ..., N-1 (N = f_s · τ)
  - Transmitted LFM chirp template s[n], n = 0, ..., N-1
  - FFT length L ≥ 2N (zero-padded to avoid circular convolution)

Output:
  - Compressed pulse y[n], n = 0, ..., 2N-2
  - Peak detection with range estimate r_peak

Procedure:
  1. Generate matched filter impulse response:
     h[n] = s*[N-1 - n], n = 0, ..., N-1
  
  2. Zero-pad both signals to length L:
     x_zp[n] = { x[n] for n = 0..N-1, 0 for n = N..L-1 }
     h_zp[n] = { h[n] for n = 0..N-1, 0 for n = N..L-1 }
  
  3. Compute FFTs:
     X[k] = FFT{x_zp[n]}, k = 0, ..., L-1
     H[k] = FFT{h_zp[n]}, k = 0, ..., L-1
  
  4. Multiply in frequency domain:
     Y[k] = X[k] · H[k], k = 0, ..., L-1
  
  5. Inverse FFT:
     y[n] = IFFT{Y[k]}, n = 0, ..., L-1
  
  6. Extract valid samples (first 2N-1 samples):
     y_valid[n] = y[n], n = 0, ..., 2N-2
  
  7. Normalize by signal energy:
     E_s = sum(|s[n]|²) for n = 0..N-1
     y_norm[n] = y_valid[n] / sqrt(E_s)
  
  8. Peak detection:
     n_peak = argmax(|y_norm[n]|²)
     range_est = n_peak · c / (2 · f_s)
  
  9. Interpolate for sub-sample accuracy (optional):
     Use parabolic interpolation around n_peak:
     delta = (|y_norm[n_peak-1]|² - |y_norm[n_peak+1]|²) / 
             (2 · (2·|y_norm[n_peak]|² - |y_norm[n_peak-1]|² - |y_norm[n_peak+1]|²))
     range_est_sub = (n_peak + delta) · c / (2 · f_s)
  
  Return: y_norm, range_est_sub
```

**Computational Complexity**: O(L log₂ L) for FFT operations, where L = 2^ceil(log₂(2N)). For N = 2000 samples (τ = 2 ms at f_s = 1 MHz), L = 4096, requiring approximately 2 · 4096 · log₂(4096) ≈ 98,304 complex multiplications per pulse.

### Algorithm 2: Doppler Compensation via Frequency-Locked Loop (Bat-Inspired)

```
Input:
  - Received echo signal x(t) after matched filtering
  - Transmitted frequency f_tx
  - Reference frequency f_ref (desired echo frequency)
  - Loop bandwidth B_loop (typically 10-50 Hz)
  - Update rate f_update (typically 100-200 Hz)

Output:
  - Compensated transmitted frequency f_tx_comp
  - Estimated Doppler shift f_d_est
  - Range bias correction Δr_corr

Procedure:
  1. Initialize:
     f_tx_curr = f_tx
     f_d_est = 0
     phase_error = 0
     integrator = 0
     K_p = 2 · B_loop  (proportional gain)
     K_i = B_loop²     (integral gain)

  2. For each received echo at time t_k:
     
     a. Extract echo frequency using zero-crossing detection or 
        maximum likelihood estimation:
        f_echo = argmax_f |∫ x(t) · e^{-j2πft} dt|²
        
     b. Compute frequency error:
        f_error = f_echo - f_ref
        
     c. Update phase-locked loop (second-order):
        phase_error = phase_error + f_error · (1/f_update)
        integrator = integrator + K_i · f_error · (1/f_update)
        f_correction = K_p · f_error + integrator
        
     d. Update transmitted frequency:
        f_tx_curr = f_tx_curr - f_correction
        
     e. Estimate Doppler shift:
        f_d_est = f_echo - f_tx_curr
        
     f. Compute range bias correction (for LFM):
        Δr_corr = (f_d_est · c · τ) / (2 · B)
        where τ is pulse duration, B is bandwidth
        
     g. Apply correction to range estimate:
        r_corrected = r_raw - Δr_corr
        
     h. Update AUV velocity estimate:
        v_est = f_d_est · c / (2 · f_tx_curr)
        
  3. If no echo detected for T_timeout seconds:
     Fade f_tx_curr back to nominal f_tx
     Reset integrator to zero

  Return: f_tx_comp, f_d_est, r_corrected
```

**Biological Inspiration**: This algorithm is directly inspired by the Doppler Shift Compensation (DSC) mechanism in horseshoe bats (Rhinolophidae) and mustached bats (Pteronotus parnellii). Schnitzler (1968) demonstrated that Rhinolophus ferrumequinum adjusts its emitted pulse frequency to maintain the returning echo within a narrow "auditory fovea"—a region of extremely sharp frequency tuning in the cochlea. The bat's DSC implements a real-time frequency-locked loop with a time constant of approximately 20-50 ms and a frequency resolution better than 0.1% (Schuller et al., 1974; Metzner et al., 2002). The analytical equivalence to a second-order PLL was established by Simmons (1974) and later formalized by Schnitzler and Denzinger (2011).

## 4. BIBTEX REFERENCES

@book{Woodward1953,
  author={P. M. Woodward},
  title={Probability and Information Theory, with Applications to Radar},
  publisher={Pergamon Press},
  year={1953},
  address={London}
}

@book{Rihaczek1969,
  author={A. W. Rihaczek},
  title={Principles of High-Resolution Radar},
  publisher={McGraw-Hill},
  year={1969},
  address={New York}
}

@book{Skolnik2008,
  author={M. I. Skolnik},
  title={Radar Handbook},
  edition={3rd},
  publisher={McGraw-Hill},
  year={2008},
  isbn={978-0-07-148547-0}
}

@book{Urick1983,
  author={R. J. Urick},
  title={Principles of Underwater Sound},
  edition={3rd},
  publisher={McGraw-Hill},
  year={1983},
  address={New York}
}

@book{Proakis2007,
  author={J. G. Proakis and D. K. Manolakis},
  title={Digital Signal Processing},
  edition={4th},
  publisher={Pearson Prentice Hall},
  year={2007},
  isbn={978-0-13-187374-2}
}

@article{Turin1960,
  author={G. L. Turin},
  title={An introduction to matched filters},
  journal={IRE Transactions on Information Theory},
  year={1960},
  volume={6},
  number={3},
  pages={311--329},
  doi={10.1109/TIT.1960.1057571}
}

@article{North1943,
  author={D. O. North},
  title={An analysis of the factors which determine signal/noise discrimination in pulsed-carrier systems},
  journal={Proceedings of the IEEE},
  year={1963},
  volume={51},
  number={7},
  pages={1016--1027},
  note={Reprint of 1943 RCA Laboratories Report},
  doi={10.1109/PROC.1963.2383}
}

@article{Schnitzler1968,
  author={H.-U. Schnitzler},
  title={Die Ultraschall-Ortungslaute der Hufeisen-Fledermäuse (Chiroptera-Rhinolophidae) in verschiedenen Orientierungssituationen},
  journal={Zeitschrift für Vergleichende Physiologie},
  year={1968},
  volume={57},
  number={4},
  pages={376--408},
  doi={10.1007/BF00303062}
}

@article{Schuller1974,
  author={G. Schuller and K. Beuter and H.-U. Schnitzler},
  title={Response to frequency shifted artificial echoes in the bat Rhinolophus ferrumequinum},
  journal={Journal of Comparative Physiology},
  year={1974},
  volume={89},
  number={3},
  pages={275--286},
  doi={10.1007/BF00694791}
}

@article{Metzner2002,
  author={W. Metzner and S. Zhang and M. Smotherman},
  title={A role for neural corticofugal feedback in the Doppler-shift compensation system of horseshoe bats},
  journal={Journal of Neurophysiology},
  year={2002},
  volume={87},
  number={6},
  pages={3003--3014},
  doi={10.1152/jn.2002.87.6.3003}
}

@article{Simmons1974,
  author={J. A. Simmons},
  title={Response of the Doppler echolocation system in the bat Rhinolophus ferrumequinum},
  journal={Journal of the Acoustical Society of America},
  year={1974},
  volume={56},
  number={2},
  pages={672--682},
  doi={10.1121/1.1903309}
}

@article{Schnitzler2011,
  author={H.-U. Schnitzler and A. Denzinger},
  title={Auditory fovea and Doppler shift compensation: adaptations for flutter detection in echolocating bats},
  journal={Journal of Comparative Physiology A},
  year={2011},
  volume={197},
  number={5},
  pages={541--559},
  doi={10.1007/s00359-011-0636-6}
}

@article{Hayes2009,
  author={M. P. Hayes and P. T. Gough},
  title={Synthetic aperture sonar: A review of current status},
  journal={IEEE Journal of Oceanic Engineering},
  year={2009},
  volume={34},
  number={3},
  pages={207--224},
  doi={10.1109/JOE.2009.2020853}
}

@standard{ISO9613-1,
  title={ISO 9613-1:1993 Acoustics — Attenuation of sound during propagation outdoors — Part 1: Calculation of the absorption of sound by the atmosphere},
  organization={International Organization for Standardization},
  year={1993}
}

@standard{ANSI_S1_26,
  title={ANSI S1.26-1995 (R2004) Method for Calculation of the Absorption of Sound by the Atmosphere},
  organization={Acoustical Society of America},
  year={1995}
}

## 5. INTEGRATION NOTES (200+ words)

### How Domain Contributions Connect to the Paper's Overall System

The physics contributions detailed above provide the foundational signal processing layer for the acoustic SLAM system described in the paper. Specifically:

1. **Matched filter theory (Equations 1-2, Algorithm 1)** directly supports the sonar preprocessing and feature extraction pipeline (Chapter 3). The frequency-domain matched filter implementation enables real-time pulse compression of LFM chirps, converting raw acoustic returns into high-resolution range profiles. The range resolution Δr = c/(2B) = 3.75 cm (for B = 20 kHz) determines the spatial precision with which sonar landmarks can be localized—a critical parameter for the SLAM data association step (Chapter 3, Section 3.3). The matched filter SNR gain G = BT = 40 (16 dB) extends the effective detection range, enabling the AUV to maintain feature tracking over longer baselines.

2. **The active sonar equation (Equation 3)** provides the theoretical framework for predicting detection performance as a function of range, frequency, and environmental conditions. This directly informs the sensor configuration (Chapter 2) by quantifying the trade-off between range resolution (improving with B) and maximum detection range (degrading with α(f)). For the proposed system operating at 200 kHz, the absorption coefficient α ≈ 46.8 dB/km limits useful detection to approximately 50-100 m in typical coastal waters—a constraint that must be incorporated into the SLAM front-end design.

3. **Doppler compensation via frequency-locked loop (Equation 4, Algorithm 2)** addresses a critical failure mode in underwater SLAM: range bias due to platform motion. For an AUV moving at 2 m/s, the Doppler shift at 200 kHz is approximately 533 Hz, which for an LFM chirp with B = 20 kHz and τ = 2 ms introduces a range bias of approximately 0.04 m. While this bias is small for individual measurements, uncorrected it accumulates over the trajectory and degrades SLAM consistency. The bat-inspired frequency-locked loop provides a computationally efficient mechanism for real-time Doppler compensation, directly analogous to the horseshoe bat's DSC system.

4. **The ambiguity function analysis (Equation 2)** informs waveform design choices for the sonar subsystem. The LFM waveform's range-Doppler coupling, while introducing a systematic bias, provides Doppler tolerance that is essential for moving platforms. The ambiguity function ridge ensures that even with imperfect Doppler compensation, the matched filter output maintains high SNR—a property that is exploited in the SLAM measurement model (Chapter 2, Equation 4).

5. **The bat biosonar connection** provides biological validation for the signal processing architecture. The horseshoe bat's DSC mechanism has been refined over 50 million years of evolution to solve precisely the problem we face: maintaining accurate range estimates from a moving platform using frequency-modulated echolocation. The analytical equivalence between the bat's neural frequency-locked loop and engineered PLL-based Doppler compensation (demonstrated by Simmons, 1974) provides confidence that the proposed approach is both theoretically sound and practically implementable.

In summary, these physics contributions form the signal processing backbone of the acoustic SLAM system, connecting the raw acoustic measurements to the feature extraction, data association, and state estimation modules that constitute the core SLAM pipeline.