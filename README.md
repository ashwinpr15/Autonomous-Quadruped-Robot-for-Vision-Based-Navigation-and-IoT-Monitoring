# Autonomous Quadruped Robot (Spider Bot) 🕷️🤖

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=flat-square)
![Raspberry Pi](https://img.shields.io/badge/Hardware-Raspberry%20Pi%204-red?style=flat-square)
![OpenCV](https://img.shields.io/badge/Vision-OpenCV-green?style=flat-square)
![ThingSpeak](https://img.shields.io/badge/IoT-ThingSpeak-orange?style=flat-square)

A four-legged autonomous robot designed for stable locomotion on irregular terrain. This project implements a custom **Creep Gait** algorithm, uses **Computer Vision (Canny Edge Detection)** for obstacle avoidance, and features real-time IoT environmental monitoring.

**Developer:** Ashwin Pillanda Ravindra

---

## 🎓 Academic Project Context
This project was developed as the **Final Year Capstone Project** for the **Bachelor of Engineering in Electronics and Communication Engineering** at **SDM Institute of Technology, Ujire** (Affiliated to Visvesvaraya Technological University, Belagavi).

> *"Certified that the Project Work titled ‘Quadruped Autonomous Robot’ is carried out by Mr. Ashwin Pillanda Ravindra, USN: 4SU17EC012, bonafide student of SDM Institute of Technology, Ujire, in partial fulfilment for the award of the degree of Bachelor of Engineering in Electronics and Communication Engineering during the year 2020-2021."*

---

## ⚡ Key Features
* **Autonomous Navigation:** Detects and bypasses obstacles using a Pi Camera and image processing algorithms (Canny Edge Detection).
* **Custom Locomotion Engine:** Implements a "Creep Gait" algorithm controlling 12 servo motors to maintain static stability while moving.
* **Manual Control:** Wi-Fi-based remote control via keyboard commands.
* **Live Surveillance:** Low-latency video streaming via VLC and Raspberry Pi Camera.
* **IoT Monitoring:** Real-time temperature and humidity tracking (DHT11) visualized on a ThingSpeak dashboard.

## 🛠️ Hardware Stack
* **Controller:** Raspberry Pi 4 (Quad-core Cortex-A72)
* **Actuators:** 12x SG90 Servo Motors driven by PCA9685 (16-channel PWM driver)
* **Sensors:** Pi Camera (5MP), HC-SR04 Ultrasonic, DHT11 (Temp/Humidity)
* **Power:** Li-ion Battery Pack with LM2596 Buck Converters (5V & 6V rails)
* **Chassis:** Custom 3D-printed quadruped frame (Coxa, Femur, Tibia design)

## 📊 Software Architecture
### 1. Locomotion (Creep Gait)
The robot mimics a predatory "creep" movement where 3 legs always remain on the ground to maintain the Center of Gravity (CoG).
* **Forward/Backward:** shifting legs between "Parallel" (90°) and "Lateral" (140°) positions.
* **Turning:** Pivotal motion created by opposing leg movements on left/right sides.

### 2. Obstacle Avoidance
* **Image Capture:** 640x480 frames.
* **Preprocessing:** Bilateral filtering for noise reduction.
* **Edge Detection:** Canny algorithm to identify object boundaries.
* **Decision Logic:** The frame is divided into 3 chunks. The robot steers towards the "chunk" with the fewest edge contours.

## 📂 Repository Structure
* `src/navigation.py`: Main autonomous driving logic using OpenCV.
* `src/locomotion.py`: Servo control sequences for walking gaits.
* `src/manual_control.py`: Threaded remote control interface.
* `src/iot_monitor.py`: Sensor data publisher (ThingSpeak).
* `src/stream_client.py`: Video streaming client.

## 🚀 Usage
1. **Setup:** Connect PCA9685 and Sensors to RPi GPIO/I2C pins.
2. **Install Dependencies:** `pip install -r requirements.txt`
3. **Run Autonomous Mode:**
   `python src/navigation.py`
4. **Run Manual Mode:**
   `python src/manual_control.py` (Use WASD keys)

---

## 📄 Project Report
For a deep dive into the engineering math, algorithms, and circuit diagrams used in this project, you can view the full documentation below:

[**View Full Project Report (PDF)**](src/Ashwin%20BE%20Project%20Report.pdf)
