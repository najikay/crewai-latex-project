# Domain Contribution: Matched Filter Theory, LFM/FM Sonar Signal Design, Acoustic Wave Propagation, Doppler Physics, Cochlear Mechanics, Range-Doppler Ambiguity, and Beamforming

## 1. Technical Analysis (500+ words)

### 1.1 Matched Filter Theory and Its Biological Basis

The matched filter (MF) is the optimal linear filter for maximizing the signal-to-noise ratio (SNR) in the presence of additive white Gaussian noise (AWGN) [Turin, 1960]. For a transmitted signal $s(t)$ of duration $T$, the impulse response of the matched filter is $h(t) = s^*(T - t)$, i.e., the time-reversed complex conjugate of the transmitted waveform. The MF output is the cross-correlation between the received signal $r(t)$ and the transmitted template $s(t)$:

\begin{equation}
y(\tau) = \int_{-\infty}^{\infty} r(t) s^*(t - \tau) dt
\end{equation}

Simmons (1979) demonstrated that the big brown bat (*Eptesicus fuscus*) achieves echo delay detection thresholds as fine as 500 nanoseconds — a temporal hyperacuity that is consistent with matched filter processing of its FM echolocation calls [Simmons, 1979]. This finding established that bat biosonar operates near the theoretical limits predicted by matched filter theory, with the bat's auditory system effectively implementing a bank of matched filters tuned to different echo delays and Doppler shifts.

### 1.2 LFM/FM Sonar Signal Design

Bats employ two primary signal types: constant-frequency (CF) and frequency-modulated (FM) calls. CF calls (used by horseshoe bats, Rhinolophidae) provide precise Doppler shift measurement for velocity estimation, while FM calls (used by most bat species) provide high range resolution via the time-bandwidth product [Schnitzler & Kalko, 2001].

The linear frequency-modulated (LFM) chirp is the engineering analog of bat FM calls:

\begin{equation}
s_{\text{LFM}}(t) = A \cdot \text{rect}\left(\frac{t}{T}\right) \cdot \exp\left(j2\pi\left(f_0 t + \frac{1}{2} \alpha t^2\right)\right)
\end{equation}

where $\alpha = B/T$ is the chirp rate, $B$ is the bandwidth, $T$ is the pulse duration, and $f_0$ is the starting frequency. The time-bandwidth product $BT$ determines the processing gain: $G = BT$ for the matched filter output SNR improvement.

### 1.3 Acoustic Wave Propagation and Doppler Physics

For a drone-mounted sonar operating at 40 kHz in air, the wavelength is $\lambda = c/f \approx 343/40000 \approx 8.6$ mm. The sonar equation governing received echo power is [Urick, 1983]:

\begin{equation}
\text{SNR} = \frac{P_{\text{emit}} G^2 \lambda^2 \sigma}{(4\pi)^3 r^4 k T B F}
\end{equation}

where $P_{\text{emit}}$ is transmitted power, $G$ is transducer gain, $\sigma$ is target cross-section, $r$ is range, $k$ is Boltzmann's constant, $T$ is temperature, $B$ is receiver bandwidth, and $F$ is noise figure.

The Doppler shift for a moving drone with velocity $v$ relative to a stationary target is:

\begin{equation}
f_d = \frac{2v \cos\theta}{\lambda} = \frac{2v f_0 \cos\theta}{c}
\end{equation}

where $\theta$ is the angle between the velocity vector and the line-of-sight to the target. For a drone traveling at 5 m/s with a 40 kHz sonar, the maximum Doppler shift is approximately $f_d = 2 \times 5 \times 40000 / 343 \approx 1166$ Hz — a significant fraction of the signal bandwidth.

### 1.4 Range-Doppler Ambiguity Function

The ambiguity function characterizes the joint range-Doppler resolution of a waveform [Woodward, 1953]. For narrowband signals, the ambiguity function is:

\begin{equation}
\chi(\tau, f_D) = \int_{-\infty}^{\infty} s(t) s^*(t - \tau) e^{j2\pi f_D t} dt
\end{equation}

For bat FM signals, the wideband ambiguity function (WAF) must be used due to the large fractional bandwidth [Altes, 1973]:

\begin{equation}
\chi_{\text{WB}}(\tau, \eta) = \sqrt{|\eta|} \int_{-\infty}^{\infty} s(t) s^*(\eta(t - \tau)) dt
\end{equation}

where $\eta = (c - v_r)/(c + v_r)$ is the Doppler scale factor. The WAF of bat FM signals exhibits a characteristic "ridge" along the range-Doppler coupling line, which bats exploit for simultaneous range-velocity estimation [Lee et al., 1993].

### 1.5 Cochlear Mechanics and Auditory Filter Banks

The bat cochlea performs a real-time time-frequency decomposition analogous to a filter bank. The gammatone filter bank, which models mammalian cochlear filtering, has an impulse response [Patterson et al., 1992]:

\begin{equation}
g(t) = A t^{n-1} e^{-2\pi b t} \cos(2\pi f_c t + \phi)
\end{equation}

where $n$ is the filter order (typically 4), $b$ is the bandwidth parameter, $f_c$ is the center frequency, and $\phi$ is the phase. Horseshoe bats exhibit a specialized "acoustic fovea" — an over-representation of frequencies near the dominant CF component — achieved through cochlear mechanical tuning that provides a filter quality factor $Q_{10\text{dB}} > 400$ [Vater & Kossl, 2004].

### 1.6 Beamforming for Direction Estimation

Bats estimate target direction using binaural cues (interaural time difference, ITD; interaural level difference, ILD) and monaural spectral cues from the pinnae. The engineering analog is delay-and-sum beamforming with an array of $M$ microphones:

\begin{equation}
y_{\text{BF}}(t, \theta) = \sum_{m=1}^{M} w_m \cdot r_m(t - \tau_m(\theta))
\end{equation}

where $w_m$ are weights and $\tau_m(\theta) = (d_m \sin\theta)/c$ are the steering delays for direction $\theta$. For a two-element array with spacing $d$, the angular resolution is $\Delta\theta \approx \lambda/(Md \cos\theta)$.

## 2. Key Algorithms

### Algorithm 1: Matched Filter with Doppler Compensation for Bat-Inspired Sonar

```
Input: Transmitted signal s(t), received echo r(t), candidate Doppler shifts f_D ∈ [f_min, f_max]
Output: Range-Doppler map R(τ, f_D)

1. For each candidate Doppler shift f_D:
   a. Generate Doppler-shifted template: s_fD(t) = s(t) · exp(j2π f_D t)
   b. Compute matched filter output: y_fD(τ) = ∫ r(t) · s_fD*(t - τ) dt
   c. Store R(τ, f_D) = |y_fD(τ)|²
2. Estimate range: τ_hat = argmax_τ [max_fD R(τ, f_D)]
3. Estimate radial velocity: v_r_hat = (c/2) · (f_D_hat / f_0) where f_D_hat = argmax_fD R(τ_hat, f_D)
4. Return (τ_hat, v_r_hat)
```

This algorithm implements a bank of matched filters, each tuned to a different Doppler hypothesis. The computational cost is $O(N_\tau \times N_{f_D})$ where $N_\tau$ is the number of range bins and $N_{f_D}$ is the number of Doppler hypotheses. For real-time implementation on a micro-UAV, the Doppler search range is limited to $\pm 2\text{ kHz}$ (corresponding to $\pm 8.6$ m/s at 40 kHz).

### Algorithm 2: Gammatone Filter Bank for Bio-Mimetic Cochlear Processing

```
Input: Received echo signal r(t), number of channels N_ch, frequency range [f_low, f_high]
Output: Time-frequency representation S(t, f_c) for each channel

1. Initialize N_ch gammatone filters with center frequencies f_c[i] spaced on ERB scale:
   ERB(f) = 24.7 · (4.37 · f/1000 + 1)
2. For each channel i = 1 to N_ch:
   a. Compute filter coefficients for 4th-order gammatone:
      g_i(t) = A · t³ · exp(-2π · b · ERB(f_c[i]) · t) · cos(2π f_c[i] t)
   b. Filter the signal: s_i(t) = r(t) ∗ g_i(t)  (convolution)
   c. Compute envelope: e_i(t) = |Hilbert(s_i(t))|
   d. Detect threshold crossings for echo arrival times
3. Reconstruct echo delay from channel activation times
4. Return S(t, f_c) = [s_1(t), s_2(t), ..., s_N_ch(t)]
```

The gammatone filter bank provides a biologically plausible front-end that mimics the bat cochlea's frequency decomposition. The ERB spacing ensures that filter bandwidths match the critical bandwidths of the mammalian auditory system.

## 3. Equations (LaTeX-ready)

\begin{equation}
y(\tau) = \int_{-\infty}^{\infty} r(t) s^*(t - \tau) dt \quad \text{(Matched filter output)} \label{eq:matched_filter}
\end{equation}

\begin{equation}
\chi(\tau, f_D) = \int_{-\infty}^{\infty} s(t) s^*(t - \tau) e^{j2\pi f_D t} dt \quad \text{(Narrowband ambiguity function)} \label{eq:ambig_nb}
\end{equation}

\begin{equation}
\chi_{\text{WB}}(\tau, \eta) = \sqrt{|\eta|} \int_{-\infty}^{\infty} s(t) s^*(\eta(t - \tau)) dt \quad \text{(Wideband ambiguity function)} \label{eq:ambig_wb}
\end{equation}

\begin{equation}
g(t) = A t^{n-1} e^{-2\pi b \cdot \text{ERB}(f_c) \cdot t} \cos(2\pi f_c t + \phi) \quad \text{(Gammatone filter impulse response)} \label{eq:gammatone}
\end{equation}

\begin{equation}
y_{\text{BF}}(t, \theta) = \sum_{m=1}^{M} w_m \cdot r_m\left(t - \frac{d_m \sin\theta}{c}\right) \quad \text{(Delay-and-sum beamformer)} \label{eq:beamformer}
\end{equation}

\begin{equation}
\text{SNR} = \frac{P_{\text{emit}} G^2 \lambda^2 \sigma}{(4\pi)^3 r^4 k T B F} \quad \text{(Sonar equation)} \label{eq:sonar_eq}
\end{equation}

## 4. BibTeX References

```bibtex
@article{simmons1979,
  author={Simmons, J. A.},
  title={Perception of echo phase information in bat sonar},
  journal={Science},
  volume={207},
  number={4437},
  pages={1336--1338},
  year={1980},
  doi={10.1126/science.7355292}
}

@article{turin1960,
  author={Turin, G. L.},
  title={An introduction to matched filters},
  journal={IRE Transactions on Information Theory},
  volume={6},
  number={3},
  pages={311--329},
  year={1960},
  doi={10.1109/TIT.1960.1057571}
}

@article{altes1973,
  author={Altes, R. A.},
  title={Some invariance properties of the wideband ambiguity function},
  journal={Journal of the Acoustical Society of America},
  volume={53},
  number={4},
  pages={1154--1160},
  year={1973},
  doi={10.1121/1.1913442}
}

@article{schnitzler2001,
  author={Schnitzler, H.-U. and Kalko, E. K. V.},
  title={Echolocation by insect-eating bats},
  journal={BioScience},
  volume={51},
  number={7},
  pages={557--569},
  year={2001},
  doi={10.1641/0006-3568(2001)051[0557:EBIEB]2.0.CO;2}
}

@article{woodward1953,
  author={Woodward, P. M.},
  title={Theory of radar information},
  journal={Transactions of the IRE Professional Group on Information Theory},
  volume={1},
  number={1},
  pages={108--113},
  year={1953},
  doi={10.1109/IRETIT.1953.5218571}
}

@article{lee1993,
  author={Lee, D. and Huang, Y. and Feng, A.},
  title={Wideband ambiguity function of South-China FM bat sonar signals},
  journal={TENCON '93. Proceedings. Computer, Communication, Control and Power Engineering},
  volume={3},
  pages={79--82},
  year={1993},
  doi={10.1109/TENCON.1993.327896}
}

@article{patterson1992,
  author={Patterson, R. D. and Robinson, K. and Holdsworth, J. and McKeown, D. and Zhang, C. and Allerhand, M.},
  title={Complex sounds and auditory images},
  journal={Auditory Physiology and Perception},
  pages={429--446},
  year={1992},
  publisher={Pergamon Press}
}

@book{urick1983,
  author={Urick, R. J.},
  title={Principles of Underwater Sound},
  edition={3rd},
  publisher={McGraw-Hill},
  year={1983},
  address={New York}
}

@article{vater2004,
  author={Vater, M. and K{\"o}ssl, M.},
  title={The ears of bats: structure and function},
  journal={Echolocation in Bats and Dolphins},
  pages={83--92},
  year={2004},
  publisher={University of Chicago Press}
}

@book{thrun2005,
  author={Thrun, S. and Burgard, W. and Fox, D.},
  title={Probabilistic Robotics},
  publisher={MIT Press},
  year={2005},
  address={Cambridge, MA}
}
```

## 5. Integration Notes

This domain contribution connects to the paper in the following ways:

1. **Chapter 2 (Biological Foundations)**: The matched filter theory provides the mathematical framework for understanding bat echolocation performance. The gammatone filter bank model (Section 1.5) directly supports the discussion of cochlear mechanics and neural processing in the bat auditory system.

2. **Chapter 3 (Bio-Mimetic Sonar System Design)**: The LFM chirp design (Section 1.2) and matched filter implementation (Algorithm 1) form the core signal processing pipeline for the proposed sonar system. The sonar equation (Eq. \ref{eq:sonar_eq}) provides the link budget for transducer selection and power amplifier design.

3. **Chapter 4 (Multi-Modal Sensor Fusion Framework)**: The Doppler physics (Section 1.3) directly feeds into the Doppler-aware EKF measurement model. The range-Doppler ambiguity function (Section 1.4) characterizes the fundamental estimation limits that the EKF must respect.

4. **Chapter 5 (Bio-Mimetic SLAM)**: The beamforming algorithm (Section 1.6) provides direction-of-arrival estimates for sonar landmarks, enabling 3D landmark initialization in the SLAM framework.

5. **Chapter 7 (Neuromorphic Implementation)**: The gammatone filter bank (Algorithm 2) provides a biologically plausible front-end that can be mapped onto spiking neural network architectures for low-power neuromorphic implementation.

6. **Chapter 9 (Conclusion)**: The Cram\'er-Rao lower bound derivations for range-Doppler estimation (derived from the ambiguity function) provide theoretical performance bounds against which the experimental results can be compared.

**Key design parameters derived from this analysis:**
- Sonar frequency: 40 kHz (wavelength 8.6 mm, good for micro-UAV form factor)
- Bandwidth: 5-10 kHz (provides range resolution of 1.7-3.4 cm)
- Pulse duration: 1-5 ms (provides processing gain of 10-50 for matched filter)
- Doppler resolution: ~100 Hz (provides velocity resolution of ~0.4 m/s at 40 kHz)
- Array configuration: 2-4 MEMS microphones with 5-10 mm spacing (provides angular resolution of 5-10 degrees)

These parameters are consistent with bat echolocation systems and are achievable with off-the-shelf MEMS ultrasonic transducers and microcontrollers suitable for 250g-class micro-UAVs.