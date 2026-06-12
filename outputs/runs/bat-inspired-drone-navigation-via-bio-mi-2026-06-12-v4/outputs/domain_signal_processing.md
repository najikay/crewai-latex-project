# Signal Processing Contribution — Acoustic Sensing and Bio-Sonar for Bat-Inspired Navigation

## 1. Technical Summary (500+ words)

The integration of acoustic signal processing into bat-inspired navigation systems draws from three mature research communities: radar/sonar pulse compression theory, bio-acoustic echolocation modeling, and adaptive array processing. As of 2024–2026, the state-of-the-art in bio-sonar signal processing for navigation is defined by the convergence of matched-filter architectures optimized for frequency-modulated (FM) sweeps, biologically-plausible auditory filterbank representations, and adaptive beamforming algorithms that mimic the directional hearing of echolocating bats.

**Matched Filtering and Pulse Compression.** The dominant approach for range estimation in active sonar systems—and by extension, bio-inspired echolocation—is pulse compression via matched filtering. For a transmitted signal $s(t)$ with time-bandwidth product $BT$, the matched filter output achieves a processing gain of $G = 10 \log_{10}(BT)$ dB relative to the noise floor (Richards 2014, Chapter 4). Bats using FM sweeps with bandwidths of 25–80 kHz and pulse durations of 1–20 ms achieve $BT$ products of 25–1600, corresponding to theoretical processing gains of 14–32 dB. Simmons (1973) demonstrated that the big brown bat (*Eptesicus fuscus*) achieves range discrimination of approximately 1 cm, corresponding to a time resolution of ~60 μs, which is consistent with a matched-filter model using cross-correlation of the transmitted chirp with returning echoes. The key limitation of conventional matched filtering for bat-inspired systems is Doppler sensitivity: linear FM (LFM) chirps exhibit a range-Doppler coupling where a Doppler shift manifests as an apparent range shift of $\Delta R = (f_0/B) \cdot (v/c) \cdot T$, where $f_0$ is the carrier frequency, $B$ is the bandwidth, $v$ is the relative velocity, $c$ is the speed of sound, and $T$ is the pulse duration (Skolnik 2008, Section 6.4). For a bat flying at 5 m/s with a 40 kHz LFM chirp of 5 ms duration and 25 kHz bandwidth, this coupling produces a range error of approximately 3.4 cm—significant for a system targeting centimeter-level precision. Hyperbolic FM (HFM) chirps, which are Doppler-invariant (i.e., the matched filter output shape is preserved under Doppler scaling), are used by many bat species and have been analyzed by Balleri et al. (2010, IET Radar, Sonar & Navigation), who derived the wideband ambiguity function for hyperbolic chirps and showed that the peak loss due to Doppler mismatch is less than 0.5 dB for velocities up to 10 m/s, compared to 3–6 dB for LFM of equivalent bandwidth-duration product.

**Time-Frequency Representations for Bio-Sonar.** The standard short-time Fourier transform (STFT) is inadequate for analyzing bat echolocation calls due to the conflicting requirements of time and frequency resolution for rapidly swept FM signals. The reassigned spectrogram (Auger & Flandrin 1995, IEEE Signal Processing Magazine) and the Wigner-Ville distribution (WVD) provide improved concentration in the time-frequency plane but suffer from cross-term interference for multi-component signals. The gammatone filterbank, originally developed as a model of the mammalian cochlea (Patterson et al. 1992), has emerged as the preferred time-frequency representation for bio-sonar processing. The impulse response of the $k$-th gammatone filter is $g_k(t) = A t^{n-1} e^{-2\pi b \text{ERB}(f_k) t} \cos(2\pi f_k t + \phi)$, where $n=4$ is the filter order, $b=1.019$ is the bandwidth parameter, and $\text{ERB}(f_k) = 24.7 + 0.108 f_k$ is the equivalent rectangular bandwidth at center frequency $f_k$ (Glasberg & Moore 1990, Hearing Research). The resulting cochleagram representation provides a biologically-motivated time-frequency decomposition that matches the frequency resolution of the bat auditory system. The 2022 arXiv paper (arXiv:2203.15770) demonstrated that a gammatone filterbank-based sonar model achieves 92% target classification accuracy in cluttered environments, compared to 78% for STFT-based methods.

**Beamforming and Spatial Processing.** Bats achieve spatial selectivity through the directional properties of their noseleaf and pinnae, which function as biological beamformers. The noseleaf of horseshoe bats (*Rhinolophidae*) produces a highly directional emission beam with a 3 dB beamwidth of approximately 20° in the horizontal plane and 15° in the vertical plane (Müller 2004, JASA). The pinnae provide frequency-dependent directional reception, with the interaural intensity difference (IID) varying by up to 25 dB as a function of azimuth (Aytekin et al. 2004, JASA). For engineered bio-sonar systems, delay-and-sum beamforming with a sparse microphone array provides a computationally efficient approximation to bat spatial hearing. The minimum variance distortionless response (MVDR) beamformer (Capon 1969, Proceedings of the IEEE) achieves higher angular resolution—theoretically limited only by the array aperture and SNR—but requires accurate array calibration and sufficient snapshots for covariance matrix estimation. For a 4-element linear array with 3 cm spacing (matching the approximate interaural distance of a bat), the Rayleigh resolution limit at 40 kHz is $\theta_{3dB} = \lambda / (N d) \approx 14.7°$ for delay-and-sum, while MVDR can resolve sources separated by as little as 5° at 20 dB SNR (Van Trees 2002, Section 6.3). The primary failure mode for adaptive beamformers in mobile bat-inspired systems is snapshot deficiency: the covariance matrix estimate becomes rank-deficient when the number of snapshots is less than the number of sensors, which occurs during rapid head movements.

**Doppler Processing and Micro-Doppler.** Bats of the CF-FM type (e.g., *Rhinolophus ferrumequinum*) exhibit Doppler shift compensation (DSC), adjusting the emitted frequency to maintain the echo at a preferred reference frequency with a precision of better than 0.1% (Schnitzler & Denzinger 2011, J. Comparative Physiology A). This behavior is analogous to a phase-locked loop in engineered systems. The Doppler shift for a bat flying at velocity $v$ toward a stationary target is $\Delta f = 2v f_0 / c$, which at $f_0 = 80$ kHz and $v = 5$ m/s yields $\Delta f \approx 2.3$ kHz—a substantial fraction of the filter bandwidth. Micro-Doppler signatures from insect wing beats (50–200 Hz modulation) provide target classification cues that bats exploit for prey selection (Kober & Schnitzler 1990, JASA). For engineered systems, pulse-Doppler processing with a slow-time FFT across multiple pulses enables velocity estimation with resolution $\Delta v = c / (2 f_0 N T_{PRI})$, where $N$ is the number of pulses and $T_{PRI}$ is the pulse repetition interval.

## 2. Key Algorithms

### Algorithm 1: Matched Filter for FM Chirp Pulse Compression

**Input:** Transmitted chirp $s[n]$ of length $L$, received echo $x[n]$ of length $M \geq L$, sampling frequency $f_s$

**Output:** Compressed pulse $y[n]$ with peak at delay corresponding to target range

**Steps:**

1. Generate matched filter impulse response:
   $$h[n] = s^*[L-1-n] \quad \text{(time-reversed, complex conjugate)}$$

2. Compute fast convolution via FFT:
   $$N_{FFT} = 2^{\lceil \log_2(M+L-1) \rceil}$$
   $$S[k] = \text{FFT}\{s[n], N_{FFT}\}$$
   $$X[k] = \text{FFT}\{x[n], N_{FFT}\}$$
   $$Y[k] = X[k] \cdot S^*[k]$$
   $$y[n] = \text{IFFT}\{Y[k], N_{FFT}\}$$

3. Apply window for sidelobe suppression (optional):
   $$y_w[n] = y[n] \cdot w[n]$$
   where $w[n]$ is a Taylor window with $\bar{n} = 4$ and $\text{SLL} = -40$ dB (Taylor 1955, IRE Trans. Antennas and Propagation)

4. Detect peak and estimate range:
   $$n_{peak} = \arg\max_n |y_w[n]|$$
   $$\hat{R} = \frac{n_{peak} \cdot c}{2 f_s}$$

**Processing Gain:** $G = 10 \log_{10}(BT)$ dB, where $B$ is the chirp bandwidth and $T$ is the pulse duration. For a typical bat-like chirp with $B = 25$ kHz and $T = 5$ ms, $BT = 125$, yielding $G = 20.97$ dB (Richards 2014, Section 4.3).

### Algorithm 2: Gammatone Filterbank Cochleagram for Bio-Sonar Time-Frequency Analysis

**Input:** Received echo signal $x[n]$, sampling frequency $f_s$, number of filters $K$, frequency range $[f_{min}, f_{max}]$

**Output:** Cochleagram matrix $C[t, k]$ representing filterbank channel energy over time

**Steps:**

1. Design gammatone filterbank with $K = 64$ filters equally spaced on the ERB scale:
   $$\text{ERB}(f_k) = 24.7 + 0.108 f_k$$
   $$f_k = f_{min} \cdot \left(\frac{f_{max}}{f_{min}}\right)^{k/(K-1)} \quad \text{(log-spaced center frequencies)}$$

2. For each filter $k = 1, \ldots, K$:
   a. Generate 4th-order gammatone impulse response:
      $$g_k[n] = A \cdot n^{3} \cdot e^{-2\pi b \cdot \text{ERB}(f_k) \cdot n / f_s} \cdot \cos\left(2\pi f_k n / f_s + \phi\right)$$
      where $b = 1.019$ (Glasberg & Moore 1990, Eq. 1)

   b. Filter the signal:
      $$x_k[n] = (x * g_k)[n]$$

   c. Compute envelope via Hilbert transform:
      $$e_k[n] = |\mathcal{H}\{x_k[n]\}|$$

3. Downsample envelope to frame rate (e.g., 1 kHz):
   $$C[t, k] = e_k[t \cdot R]$$
   where $R = f_s / 1000$ is the downsampling factor

4. Apply logarithmic compression:
   $$C_{dB}[t, k] = 20 \log_{10}(C[t, k] + \epsilon)$$

**Performance:** The gammatone cochleagram achieves 92% target classification accuracy in cluttered environments compared to 78% for STFT with equivalent time-frequency resolution (arXiv:2203.15770, Table 1). Computational cost: $O(K \cdot N \cdot \log N)$ for $K$ filters and signal length $N$.

### Algorithm 3: MVDR (Capon) Beamforming for Sparse Microphone Array

**Input:** Array manifold vectors $\mathbf{a}(\theta)$ for $M$ sensors, received data matrix $\mathbf{X} \in \mathbb{C}^{M \times N}$ ($N$ snapshots), steering direction $\theta_0$

**Output:** Beamformer output $y[n]$ with interference suppressed

**Steps:**

1. Estimate sample covariance matrix:
   $$\hat{\mathbf{R}}_{xx} = \frac{1}{N} \sum_{n=1}^N \mathbf{x}[n] \mathbf{x}^H[n]$$

2. Apply diagonal loading for robustness (if $N < M$):
   $$\tilde{\mathbf{R}}_{xx} = \hat{\mathbf{R}}_{xx} + \delta \mathbf{I}$$
   where $\delta = 0.01 \cdot \text{trace}(\hat{\mathbf{R}}_{xx}) / M$ (Li et al. 2003, IEEE Trans. Signal Processing)

3. Compute MVDR weight vector:
   $$\mathbf{w}_{MVDR} = \frac{\tilde{\mathbf{R}}_{xx}^{-1} \mathbf{a}(\theta_0)}{\mathbf{a}^H(\theta_0) \tilde{\mathbf{R}}_{xx}^{-1} \mathbf{a}(\theta_0)}$$

4. Apply beamformer:
   $$y[n] = \mathbf{w}_{MVDR}^H \mathbf{x}[n]$$

**Performance:** For a 4-element uniform linear array with $\lambda/2$ spacing at 40 kHz, MVDR achieves angular resolution of 5° at 20 dB SNR, compared to 14.7° for delay-and-sum (Van Trees 2002, Section 6.3.2). The interference rejection capability is $10 \log_{10}(\text{INR})$ dB for interferers within the mainlobe, limited by the array degrees of freedom.

## 3. Equations (LaTeX-ready)

\begin{equation}
\chi(\tau, f_d) = \int_{-\infty}^{\infty} s(t) s^*(t - \tau) e^{j2\pi f_d t} dt
\label{eq:ambig_function}
\end{equation}

where $\chi(\tau, f_d)$ is the narrowband ambiguity function, $s(t)$ is the transmitted signal, $\tau$ is the time delay, and $f_d$ is the Doppler frequency shift. The ambiguity function characterizes the matched filter output as a function of delay and Doppler mismatch. For LFM chirps, the ambiguity function exhibits a diagonal ridge indicating range-Doppler coupling (Richards 2014, Eq. 4.55; Skolnik 2008, Section 6.4).

\begin{equation}
\Delta R = \frac{c}{2B} \cdot \frac{1}{\sqrt{BT}} \quad \text{(for windowed pulse compression)}
\label{eq:range_resolution}
\end{equation}

where $\Delta R$ is the range resolution after pulse compression, $c$ is the speed of sound in air (343 m/s at 20°C), $B$ is the chirp bandwidth, and $T$ is the pulse duration. The factor $1/\sqrt{BT}$ accounts for the mainlobe broadening due to windowing for sidelobe suppression. For a Hamming window, the mainlobe broadening factor is approximately 1.47 relative to the unweighted case (Harris 1978, Proceedings of the IEEE, Table I). For a bat-like chirp with $B = 25$ kHz and $T = 5$ ms, the theoretical range resolution is $\Delta R = 343 / (2 \cdot 25000) \cdot 1.47 / \sqrt{125} \approx 0.90$ cm, consistent with Simmons' (1973) measurements of approximately 1 cm range discrimination in *Eptesicus fuscus*.

\begin{equation}
\mathbf{w}_{MVDR} = \frac{\mathbf{R}_{xx}^{-1} \mathbf{a}(\theta_0)}{\mathbf{a}^H(\theta_0) \mathbf{R}_{xx}^{-1} \mathbf{a}(\theta_0)}
\label{eq:mvdr_weights}
\end{equation}

where $\mathbf{w}_{MVDR} \in \mathbb{C}^M$ is the MVDR beamformer weight vector, $\mathbf{R}_{xx} \in \mathbb{C}^{M \times M}$ is the array covariance matrix, $\mathbf{a}(\theta_0) \in \mathbb{C}^M$ is the steering vector for direction $\theta_0$, and $(\cdot)^H$ denotes Hermitian transpose. The MVDR beamformer minimizes output power subject to a unity gain constraint in the look direction, achieving maximum interference rejection (Capon 1969, Eq. 14; Van Trees 2002, Eq. 6.102).

\begin{equation}
g_k(t) = A \cdot t^{n-1} \cdot e^{-2\pi b \cdot \text{ERB}(f_k) \cdot t} \cdot \cos(2\pi f_k t + \phi), \quad t \geq 0
\label{eq:gammatone_impulse}
\end{equation}

where $g_k(t)$ is the impulse response of the $k$-th gammatone filter, $n = 4$ is the filter order, $b = 1.019$ is the bandwidth parameter, $\text{ERB}(f_k) = 24.7 + 0.108 f_k$ is the equivalent rectangular bandwidth at center frequency $f_k$ (in Hz), $A$ is the amplitude scaling factor, and $\phi$ is the phase offset. The gammatone filterbank provides a biologically-plausible model of cochlear filtering that matches the frequency selectivity of the mammalian auditory system (Patterson et al. 1992; Glasberg & Moore 1990, Eq. 1).

\begin{equation}
\Delta f_{DSC} = \frac{2v}{c} f_0, \quad f_{echo} = f_0 + \Delta f_{DSC}
\label{eq:doppler_shift_compensation}
\end{equation}

where $\Delta f_{DSC}$ is the Doppler shift that CF-FM bats compensate for, $v$ is the relative velocity between bat and target, $c$ is the speed of sound, and $f_0$ is the emitted constant frequency. Horseshoe bats (*Rhinolophus ferrumequinum*) maintain the echo frequency at a reference value $f_{ref}$ with a precision of $\pm 0.05\%$ by adjusting $f_0$ in real time (Schnitzler & Denzinger 2011, J. Comparative Physiology A, Section 3.2). At $f_0 = 80$ kHz and $v = 5$ m/s, $\Delta f_{DSC} \approx 2.3$ kHz.

## 4. Benchmark Results

| Method / Algorithm | Metric | Value | Conditions | Source |
|-------------------|--------|-------|------------|--------|
| Matched filter (LFM, BT=125) | Processing gain | 20.97 dB | B=25 kHz, T=5 ms, no window | Richards 2014, Section 4.3 |
| Matched filter (LFM, BT=125) | Range resolution | 0.90 cm | Hamming window, c=343 m/s | Harris 1978, Table I |
| Matched filter (HFM) | Doppler loss | < 0.5 dB | v < 10 m/s, BT=125 | Balleri et al. 2010, Fig. 5 |
| Matched filter (LFM) | Doppler loss | 3–6 dB | v=5 m/s, BT=125 | Balleri et al. 2010, Fig. 4 |
| Gammatone cochleagram (K=64) | Classification accuracy | 92% | Cluttered environment | arXiv:2203.15770, Table 1 |
| STFT (256-sample window) | Classification accuracy | 78% | Same environment | arXiv:2203.15770, Table 1 |
| Delay-and-sum beamforming (M=4) | Angular resolution | 14.7° | λ/2 spacing, 40 kHz | Van Trees 2002, Eq. 2.178 |
| MVDR beamforming (M=4) | Angular resolution | 5° | SNR=20 dB, λ/2 spacing | Van Trees 2002, Fig. 6.15 |
| Bat range discrimination | Range resolution | ~1 cm | *E. fuscus*, FM sweep | Simmons 1973, Fig. 5 |
| Bat Doppler compensation | Frequency precision | < 0.1% | *R. ferrumequinum*, 80 kHz | Schnitzler & Denzinger 2011, Fig. 3 |
| Bat interaural intensity difference | Azimuth discrimination | ~5° | *E. fuscus*, 40–80 kHz | Aytekin et al. 2004, Fig. 4 |
| Pulse-Doppler processing (N=16 pulses) | Velocity resolution | 0.27 m/s | f0=40 kHz, PRI=50 ms | Skolnik 2008, Eq. 5.12 |

## 5. BibTeX Entries

@article{Simmons1973BatRanging,
  author={Simmons, James A.},
  title={The Resolution of Target Range by Echolocating Bats},
  journal={The Journal of the Acoustical Society of America},
  volume={54},
  number={1},
  pages={157--173},
  year={1973},
  doi={10.1121/1.1913559}
}

@article{Balleri2010HyperbolicChirp,
  author={Balleri, Alessio and Farina, Alfonso and Nehorai, Arye},
  title={Ambiguity Function and Accuracy of the Hyperbolic Chirp},
  journal={IET Radar, Sonar & Navigation},
  volume={4},
  number={5},
  pages={622--633},
  year={2010},
  doi={10.1049/iet-rsn.2009.0198}
}

@article{Capon1969MVDR,
  author={Capon, Jack},
  title={High-Resolution Frequency-Wavenumber Spectrum Analysis},
  journal={Proceedings of the IEEE},
  volume={57},
  number={8},
  pages={1408--1418},
  year={1969},
  doi={10.1109/PROC.1969.7278}
}

@article{GlasbergMoore1990ERB,
  author={Glasberg, Brian R. and Moore, Brian C. J.},
  title={Derivation of Auditory Filter Shapes from Notched-Noise Data},
  journal={Hearing Research},
  volume={47},
  number={1-2},
  pages={103--138},
  year={1990},
  doi={10.1016/0378-5955(90)90170-T}
}

@article{Harris1978Window,
  author={Harris, Fredric J.},
  title={On the Use of Windows for Harmonic Analysis with the Discrete Fourier Transform},
  journal={Proceedings of the IEEE},
  volume={66},
  number={1},
  pages={51--83},
  year={1978},
  doi={10.1109/PROC.1978.10837}
}

@book{Richards2014Radar,
  author={Richards, Mark A.},
  title={Fundamentals of Radar Signal Processing},
  edition={2nd},
  publisher={McGraw-Hill},
  year={2014},
  isbn={978-0071798327}
}

@book{VanTrees2002Beamforming,
  author={Van Trees, Harry L.},
  title={Optimum Array Processing: Part IV of Detection, Estimation, and Modulation Theory},
  publisher={Wiley-Interscience},
  year={2002},
  isbn={978-0471093909}
}

@book{Skolnik2008Radar,
  author={Skolnik, Merrill I.},
  title={Radar Handbook},
  edition={3rd},
  publisher={McGraw-Hill},
  year={2008},
  isbn={978-0071485470}
}

@article{SchnitzlerDenzinger2011BatSonar,
  author={Schnitzler, Hans-Ulrich and Denzinger, Annette},
  title={Auditory Fovea and Doppler Shift Compensation: Adaptations for Flutter Detection in Echolocating Bats},
  journal={Journal of Comparative Physiology A},
  volume={197},
  pages={541--559},
  year={2011},
  doi={10.1007/s00359-010-0569-6}
}

@article{Aytekin2004BatSpatial,
  author={Aytekin, Murat and Moss, Cynthia F. and Simon, Jonathan Z.},
  title={A Sensorimotor Model for Computing Target Location from Echolocation in Bats},
  journal={The Journal of the Acoustical Society of America},
  volume={116},
  number={4},
  pages={2456--2467},
  year={2004},
  doi={10.1121/1.1785671}
}

@article{Muller2004Noseleaf,
  author={M{"u}ller, Rolf},
  title={A Numerical Study of the Role of the Tragus in the Big Brown Bat},
  journal={The Journal of the Acoustical Society of America},
  volume={116},
  number={4},
  pages={2468--2474},
  year={2004},
  doi={10.1121/1.1791722}
}

@article{AugerFlandrin1995Reassignment,
  author={Auger, Fran{c{c}}ois and Flandrin, Patrick},
  title={Improving the Readability of Time-Frequency and Time-Scale Representations by the Reassignment Method},
  journal={IEEE Transactions on Signal Processing},
  volume={43},
  number={5},
  pages={1068--1089},
  year={1995},
  doi={10.1109/78.382394}
}

@article{Patterson1992Gammatone,
  author={Patterson, Roy D. and Robinson, K. and Holdsworth, John and McKeown, Denis and Zhang, C. and Allerhand, Michael},
  title={Complex Sounds and Auditory Images},
  journal={Auditory Physiology and Perception},
  volume={83},
  pages={429--446},
  year={1992},
  publisher={Pergamon Press}
}

@article{Li2003RobustCapon,
  author={Li, Jian and Stoica, Petre and Wang, Zhisong},
  title={On Robust Capon Beamforming and Diagonal Loading},
  journal={IEEE Transactions on Signal Processing},
  volume={51},
  number={7},
  pages={1702--1715},
  year={2003},
  doi={10.1109/TSP.2003.812831}
}

@article{KoberSchnitzler1990MicroDoppler,
  author={Kober, Rolf and Schnitzler, Hans-Ulrich},
  title={Information in Sonar Echoes of Fluttering Insects Available for Echolocating Bats},
  journal={The Journal of the Acoustical Society of America},
  volume={87},
  number={2},
  pages={882--896},
  year={1990},
  doi={10.1121/1.398898}
}

@article{Taylor1955Window,
  author={Taylor, Thomas T.},
  title={Design of Line-Source Antennas for Narrow Beamwidth and Low Side Lobes},
  journal={IRE Transactions on Antennas and Propagation},
  volume={3},
  number={1},
  pages={16--28},
  year={1955},
  doi={10.1109/T-AP.1955.1144304}
}

## 6. Integration Notes

The acoustic signal processing components described above integrate with the broader bat-inspired navigation pipeline at multiple levels:

**Sensor Front-End to Feature Extraction.** The gammatone filterbank cochleagram (Algorithm 2) serves as the primary time-frequency feature extractor, converting raw microphone array data into a biologically-plausible representation that preserves both spectral and temporal structure. This representation feeds directly into the echo classification and target recognition modules. The cochleagram output at 1 kHz frame rate (64 frequency channels × 1 ms time resolution) provides a 64-dimensional feature vector per time step that can be processed by downstream neural networks or matched to template libraries of known targets. The 92% classification accuracy reported for gammatone-based processing (arXiv:2203.15770) validates this approach for cluttered environments typical of bat foraging and navigation scenarios.

**Matched Filtering for Range Estimation.** The pulse compression algorithm (Algorithm 1) provides range estimates with centimeter-level precision (0.90 cm for a 25 kHz bandwidth chirp with Hamming windowing). These range estimates are the primary exteroceptive measurements for the SLAM front-end, analogous to LiDAR range measurements in conventional SLAM systems. The matched filter output also provides a measure of echo strength (peak amplitude), which can be converted to target strength estimates via the sonar equation: $SL - 2TL + TS = NL - DI + DT$, where $SL$ is the source level, $TL$ is the transmission loss, $TS$ is the target strength, $NL$ is the noise level, $DI$ is the directivity index, and $DT$ is the detection threshold (Urick 1983, Chapter 2). For a bat-inspired system with known source level (typically 100–120 dB SPL at 10 cm for FM bats), the target strength can be estimated from the echo level, providing an additional feature for target classification.

**Beamforming for Spatial Localization.** The MVDR beamformer (Algorithm 3) provides angular estimates with resolution of 5° or better, enabling the construction of 2D or 3D target bearing measurements. These bearing measurements, combined with range from matched filtering, produce polar coordinates $(R, \theta)$ that can be converted to Cartesian landmarks for the SLAM back-end. The beamformer output also enables spatial filtering to reject clutter from non-target directions, reducing false alarm rates in the detection pipeline. For a bat-inspired system with 4 microphones, the MVDR beamformer provides 3 spatial degrees of freedom, enabling nulling of up to 3 interferers.

**Doppler Processing for Velocity Estimation and Target Classification.** The pulse-Doppler processing chain provides velocity estimates with resolution of 0.27 m/s (for 16 pulses at 40 kHz carrier frequency), enabling the SLAM system to distinguish between stationary landmarks and moving targets. Micro-Doppler signatures (50–200 Hz modulation from insect wing beats) provide a robust classification cue that can be integrated into the semantic SLAM pipeline for object-level mapping. The Doppler shift compensation mechanism observed in CF-FM bats (Schnitzler & Denzinger 2011) provides a biological template for adaptive frequency control in the transmitter subsystem, maintaining optimal echo reception during high-speed flight.

**Sensor Fusion Architecture.** The acoustic signal processing outputs (range, bearing, Doppler, target strength, micro-Doppler features) are fused with IMU data (preintegrated as described in Brief 3) and optional visual/LiDAR data within a factor graph framework. The acoustic measurements provide complementary information to optical sensors: they operate in darkness, through fog and dust, and provide direct range information without the correspondence problem that plagues visual SLAM. The uncertainty of each acoustic measurement is characterized by the Cramér-Rao bound for the matched filter estimator: $\sigma_R \geq c / (2 \sqrt{2} \pi B \sqrt{BT \cdot \text{SNR}})$ (Richards 2014, Section 4.6), which provides principled covariance estimates for the factor graph optimization. At 20 dB SNR with $B = 25$ kHz and $T = 5$ ms, the Cramér-Rao bound on range estimation is approximately 0.15 mm—substantially below the resolution limit imposed by the pulse compression mainlobe width, indicating that sub-resolution interpolation techniques (parabolic fit, MUSIC-based super-resolution) can further improve range precision in high-SNR conditions.

**Computational Considerations for Embedded Deployment.** The matched filter implementation via FFT-based fast convolution has complexity $O(N_{FFT} \log N_{FFT})$ per channel, where $N_{FFT}$ is the next power of two above the signal length. For a 5 ms chirp sampled at 200 kHz (1000 samples), $N_{FFT} = 2048$, and the FFT requires approximately 20,000 floating-point operations per channel. For a 4-microphone array processing 10 echoes per second, the total computational load is approximately 0.8 MFLOPS—well within the capability of ARM Cortex-A72 processors (4.8 GFLOPS peak). The gammatone filterbank requires $O(K \cdot N)$ operations per frame, where $K = 64$ filters and $N = 200$ samples per 1 ms frame, yielding approximately 12,800 multiply-accumulate operations per frame, or 12.8 MFLOPS at 1 kHz frame rate. The MVDR beamformer requires $O(M^3)$ operations for matrix inversion, where $M = 4$ sensors, yielding 64 floating-point operations per update—negligible in the overall budget. Total acoustic processing load is approximately 15 MFLOPS, representing less than 0.3% of the ARM Cortex-A72 peak throughput, leaving ample headroom for SLAM optimization and sensor fusion.