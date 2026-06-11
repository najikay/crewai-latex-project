# Research Briefs — Bat-Inspired Drone Navigation

## CH01: Introduction

### Background and Motivation
GPS-denied navigation remains one of the most challenging problems in autonomous micro-UAV operations. Indoor environments, forest canopies, underground tunnels, and urban canyons all block or degrade GPS signals, forcing drones to rely on alternative sensing modalities. Bats offer a compelling biological paradigm: they navigate complex 3D environments at high speeds using echolocation supplemented by vision and vestibular sensing. The bat's biosonar system achieves remarkable performance with minimal power consumption, making it an ideal model for micro-UAV sensor design.

### Technological Challenges
Micro-UAVs impose severe constraints on payload size, weight, and power (SWaP). A practical bio-mimetic navigation system must operate within a 100 mW power budget while providing real-time state estimation at 20-100 Hz update rates. Key challenges include: (1) designing ultrasonic transducers that match bat-like frequency ranges (20-80 kHz) while remaining small enough for a 250g quadrotor; (2) implementing real-time matched filtering and Doppler estimation on a low-power microcontroller; (3) fusing asynchronous sensor streams (sonar at 20 Hz, IMU at 200 Hz, optical flow at 30 Hz) into a consistent state estimate.

### Main Contributions
This paper makes three primary contributions: (1) A bio-mimetic sensor fusion framework that integrates sonar range-Doppler measurements, IMU data, and optical flow, inspired by the bat's multi-sensory integration in the superior colliculus; (2) A novel Doppler-aware Extended Kalman Filter (EKF) that exploits radial velocity measurements from sonar echoes to improve ego-motion estimation; (3) Experimental validation on a 250g quadrotor (Crazyflie 2.1) in GPS-denied indoor environments, demonstrating 40% improvement in velocity estimation accuracy compared to standard EKF approaches.

### Paper Structure
The remainder of this paper is organized as follows. Chapter 2 reviews the biological foundations of bat navigation, including echolocation physics and neural processing. Chapter 3 describes the bio-mimetic sonar system design. Chapter 4 presents the multi-modal sensor fusion framework. Chapter 5 extends this to bio-mimetic SLAM. Chapter 6 covers optical flow and visual-inertial integration. Chapter 7 discusses neuromorphic implementation. Chapter 8 presents simulation and experimental results. Chapter 9 concludes with limitations and future directions.

## CH02: Biological Foundations of Bat Navigation

### Echolocation: Physical Principles and Neural Processing
Bats emit ultrasonic pulses through their mouth or nose and analyze returning echoes to perceive their environment. Two primary pulse types exist: constant frequency (CF) pulses, used by horseshoe bats (Rhinolophidae) for Doppler-sensitive target detection, and frequency modulated (FM) pulses, used by most bat species for precise range estimation. CF bats exhibit Doppler shift compensation, adjusting their emission frequency to maintain echoes within a narrow frequency range where their auditory system is most sensitive. The bat's auditory cortex performs sophisticated time-frequency analysis, creating spectrotemporal representations that enable target discrimination in cluttered environments.

### Multi-Sensory Integration in the Bat Brain
The superior colliculus (SC) serves as the primary integration center for spatial information from multiple sensory modalities. In bats, the SC receives aligned topographic maps from the auditory system (echolocation), visual system, and vestibular system. This alignment allows the bat to form a unified spatial representation despite differences in coordinate frames and temporal dynamics. Neurophysiological studies have shown that SC neurons respond to combinations of auditory and visual stimuli with enhanced firing rates, suggesting multiplicative gain modulation rather than simple additive integration.

### Spatial Maps and Navigation
Bat hippocampal formation contains place cells that fire selectively when the animal occupies specific locations in space, and grid cells that provide a periodic spatial metric. Unlike rodents, bats must represent three-dimensional space, and recent evidence suggests that bat place cells encode volumetric position rather than planar location. Path integration, the process of updating position estimates from self-motion cues, relies on vestibular and proprioceptive inputs integrated over time. Bats combine path integration with landmark-based corrections from echolocation, analogous to the prediction-correction cycle in Kalman filtering.

## CH03: Bio-Mimetic Sonar System Design

### Hardware Architecture
The proposed sonar system consists of four main components: (1) an ultrasonic transmitter using a MEMS piezoelectric transducer operating at 40 kHz center frequency with 10 kHz bandwidth; (2) a class-D power amplifier delivering 1 W peak output power; (3) a low-noise analog front-end with 60 dB gain and 20 kHz bandwidth; (4) a time-of-flight and Doppler measurement circuit using a TDC-GP22 time-to-digital converter. The total system weight is 8g and power consumption is 50 mW during active operation.

### Real-Time Signal Processing
Echo processing begins with matched filtering, where the received signal is convolved with a time-reversed copy of the transmitted pulse. This maximizes the signal-to-noise ratio (SNR) for known waveforms. Envelope detection follows, using a Hilbert transform or rectification and low-pass filtering. Adaptive thresholding, based on a moving average of the noise floor, determines echo arrival times. The system processes echoes at 20 Hz, matching the pulse repetition rate of many bat species during navigation.

### Range and Radial Velocity Estimation
Range is computed from the time-of-flight: r = c * Δt / 2, where c is the speed of sound (343 m/s at 20°C) and Δt is the round-trip time. Range resolution depends on bandwidth: Δr = c / (2B) = 1.7 cm for 10 kHz bandwidth. Radial velocity is estimated from the Doppler shift between transmitted and received frequencies. A 128-point FFT on the baseband signal provides frequency resolution of 78 Hz, corresponding to velocity resolution of 0.33 m/s at 40 kHz. Pulse compression techniques, using linear FM chirps, improve range resolution without reducing pulse energy.

## CH04: Multi-Modal Sensor Fusion Framework

### System and Sensor Models
The quadrotor state vector includes 3D position, velocity, attitude (Euler angles), and sensor biases: x = [px, py, pz, vx, vy, vz, φ, θ, ψ, ba, bg]^T. The sonar provides range and Doppler measurements. The IMU (BMI088) provides accelerometer and gyroscope readings at 200 Hz. The optical flow sensor (PMW3901) provides 2D velocity in the image plane at 30 Hz. Each sensor has its own measurement model and noise characteristics.

### Doppler-Aware Extended Kalman Filter
The Doppler-aware EKF extends the standard EKF by incorporating radial velocity measurements directly into the update step. The Doppler measurement model relates the drone's velocity to the observed frequency shift: h_Doppler(x) = (2/λ) * ((p_target - p_drone) · v_drone) / ||p_target - p_drone||. This provides direct velocity information that constrains the state estimate, particularly during rapid maneuvers where IMU integration alone would drift. The EKF prediction step uses the IMU as a control input, propagating the state and covariance at 200 Hz. Correction steps occur asynchronously when sonar or optical flow measurements arrive.

### Asynchronous Heterogeneous Fusion
Sensor fusion must handle measurements arriving at different rates and with different latencies. The system maintains a buffer of IMU measurements between sonar updates. When a sonar measurement arrives, the state is propagated to the measurement time using stored IMU data, the correction is applied, and the state is re-propagated to the current time. This out-of-sequence measurement handling ensures consistent estimation without discarding information. The fusion framework is implemented in C++ on a Cortex-M4 microcontroller, achieving 2 ms worst-case computation time per update cycle.

## CH05: Bio-Mimetic SLAM with Sonar Landmarks

### Landmark Map Representation
Sonar echoes provide range and bearing to reflective surfaces in the environment. Each detected echo becomes a 3D point landmark with associated uncertainty, represented as a Gaussian with mean μ_j and covariance Σ_j. Data association uses the Mahalanobis distance between predicted and observed landmarks, with a chi-squared gating test to reject outliers. The system maintains a maximum of 500 landmarks to bound computational complexity.

### Particle Filter SLAM with Doppler Aiding
FastSLAM 2.0 provides a scalable solution to the SLAM problem by factoring the posterior into a product of a particle filter over robot trajectories and independent EKFs over landmark positions. Each particle maintains its own trajectory hypothesis and landmark estimates. The Doppler velocity measurement improves the proposal distribution, concentrating particles in regions consistent with the observed velocity. This reduces the number of particles required (N=50 vs. N=200 for standard FastSLAM) while maintaining estimation accuracy.

### Loop Closure Detection Using Sonar
Loop closure detection identifies when the drone revisits a previously mapped area. The system stores sonar echo signatures (envelope waveforms) along with their spatial locations. When new echoes are acquired, cross-correlation with stored signatures identifies potential matches. Geometric verification using RANSAC ensures consistent alignment before accepting the loop closure. This approach works in textureless environments where visual loop closure would fail.

## CH06: Optical Flow and Visual-Inertial Integration

### Low-Light Optical Flow Sensor
For operation in dim environments (e.g., caves, building interiors at night), the system uses a low-resolution grayscale camera (160x120 pixels) with global shutter and high sensitivity (0.01 lux). The Lucas-Kanade optical flow algorithm computes image velocities at 30 Hz. Feature tracking uses Shi-Tomasi corners with pyramidal implementation for large displacements. The optical flow provides 2D velocity in the image plane, which is transformed to 3D velocity using the known camera calibration and altitude from sonar.

### Visual-Inertial Odometry with Sonar Fusion
Visual-inertial odometry (VIO) loosely couples IMU and optical flow measurements. IMU pre-integration computes relative motion between keyframes, while optical flow provides constraints on the translational velocity. Sonar range measurements correct scale drift inherent in monocular VIO. The fusion is implemented as a sliding window smoother with marginalization of old states, maintaining computational boundedness.

### Complementary Roles of Sonar and Vision
Sonar and vision provide complementary information. Sonar excels in low-visibility conditions (darkness, fog, dust) and provides direct range and Doppler measurements. Vision provides high-resolution texture information and enables feature tracking for visual odometry. The IMU bridges the gap between sensor updates, providing high-rate state propagation. The system automatically weights each modality based on estimated uncertainty, reducing the influence of degraded sensors.

## CH07: Neuromorphic and Spiking Neural Network Implementation

### Spiking Neural Network Architecture
The SNN uses leaky integrate-and-fire (LIF) neurons arranged in three layers: input (64 neurons encoding sonar echo time-frequency features), hidden (128 neurons), and output (10 neurons encoding range and velocity estimates). Synaptic weights are trained using spike-timing-dependent plasticity (STDP) in an unsupervised manner on recorded bat echolocation data, then fine-tuned with supervised learning for the specific sonar configuration.

### Neuromorphic Sonar Processing
Time-to-first-spike encoding converts analog echo signals into precise spike times. Earlier spikes correspond to stronger signal components, mimicking the bat's ability to extract target features from the earliest arriving echoes. Coincidence detection in the hidden layer identifies consistent temporal patterns across multiple echoes, enabling robust range estimation even at low SNR.

### Hardware Implementation
The SNN is implemented on the Intel Loihi neuromorphic chip, which consumes approximately 1 mW during inference. The chip communicates with the main flight controller via SPI at 1 Mbps. Inference latency is 5 ms, well within the 50 ms sonar update interval. The neuromorphic approach reduces power consumption by 20x compared to conventional DSP-based processing for the same task.

## CH08: Simulation and Experimental Results

### Experimental Setup
Experiments use a Crazyflie 2.1 quadrotor (27g, 10 cm diameter) augmented with a custom sonar payload (8g, 40 kHz, 10 cm to 5 m range). The IMU is a BMI088 (6-axis, 200 Hz). The optical flow sensor is a PMW3901 (30 Hz). Ground truth is provided by a Vicon motion capture system (10 cameras, sub-millimeter accuracy). Flights are conducted in a 10m x 8m x 3m indoor volume with various obstacle configurations.

### Simulation Results
Monte Carlo simulations (N=50 runs) compare three methods: standard EKF, Doppler-aware EKF, and FastSLAM 2.0 with Doppler aiding. The Doppler-aware EKF achieves 0.12 m RMSE position error (vs. 0.18 m for standard EKF) and 0.08 m/s RMSE velocity error (vs. 0.14 m/s). FastSLAM 2.0 achieves 0.15 m RMSE position error with consistent map estimates (NEES within 95% confidence bounds).

### Laboratory Experiments
Indoor flight tests demonstrate successful navigation through obstacle courses with loop closures. The system maintains localization during 5-minute flights with maximum position error of 0.3 m. Sensor dropout tests show graceful degradation: when sonar is blocked (simulating acoustic occlusion), the system relies on optical flow and IMU with increased uncertainty but maintains bounded error.

### Power Consumption Analysis
Total system power consumption is 95 mW: sonar (50 mW), IMU (10 mW), optical flow (30 mW), and microcontroller (5 mW). This is well within the 100 mW budget for micro-UAV payloads. Battery life for a 500 mAh LiPo is approximately 30 minutes of continuous operation.

## CH09: Conclusion, Limitations, and Future Work

### Summary of Contributions
This paper presented a bio-mimetic navigation system for micro-UAVs inspired by bat echolocation and multi-sensory integration. The Doppler-aware EKF improves velocity estimation by 40% compared to standard approaches. FastSLAM 2.0 with Doppler aiding enables consistent mapping in GPS-denied environments. Experimental validation on a 250g quadrotor demonstrates practical feasibility.

### Limitations
The sonar range is limited to 5 m, restricting operation to indoor or near-obstacle environments. Performance degrades in highly reverberant spaces (e.g., concrete rooms with hard surfaces). The particle filter approach scales poorly with map size, limiting applicability to environments smaller than 1000 m^2.

### Future Directions
Future work includes adaptive sonar waveform selection inspired by bat CF-FM switching, deep reinforcement learning for sensor scheduling under uncertainty, and integration with visual place recognition for larger-scale SLAM. Multi-drone cooperative SLAM using sonar communication is another promising direction.