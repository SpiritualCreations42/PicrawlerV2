# PiCrawler V2 🤖

---

## 🎯 Project Overview

This repo contains all the upgrades, fixes, and configurations for my heavily-modified Sunfounder PiCrawler robot. Unlike the stock PiCrawler running Raspberry Pi OS, this version runs **Ubuntu 24.04** and integrates modern robotics tools.

### Hardware Specs

**Base Platform:**

- Sunfounder PiCrawler chassis
- Raspberry Pi 5 (16GB RAM)
- Sunfounder Robot HAT v4
- Raspberry Pi AI HAT+ (Hailo-8L, 13 TOPS)

**Upgrades:**

- 🎥 **Camera**: Raspberry Pi Camera Module 3 (upgraded from stock)
- 🔊 **Audio**: USB speaker (upgraded), USB microphone
- 📡 **Networking**: Brostrend AX1800 WiFi 6E adapter
- 💾 **Storage**: 1TB NVMe drive via USB 3.0
- 🖥️ **Display**: Sunfounder 3.5" Display
- 📏 **Sensors**: Ultrasonic distance sensor (stock) + Adafruit TDK InvenSense ICM-20948 + Adafruit VL53L0X ToF
- ⚡ **Power**: 52Pi PD PowerPi Board + INIU 45W 10,000mAh battery+ + Sunfounder 7.4v Battery
- 🎮 **Servos**: 12x Sunfounder metal gear servos

**Additional Sensors:**

- Adafruit VL53L0X ToF distance sensor
- Adafruit TDK InvenSense ICM-20948 9-DoF IMU

---

## 📚 Repository Contents

### 🔧 [robot-hat-ubuntu-fix/](robot-hat-ubuntu-fix/)

#### ✅ Sunfounder Robot HAT Ubuntu 24.04 Compatibility Fix - WORKING!

The official Robot HAT installation script doesn't work on Ubuntu. This modified installer fixes all compatibility issues:

- ✅ Removes raspi-config dependency
- ✅ Manual I2C/SPI kernel module loading
- ✅ Comprehensive troubleshooting guide
- ✅ **Tested and working on Pi 5 16GB**
- ✅ All 12 servos functional
- ✅ I2C and SPI devices working

**[📖 Full Documentation →](robot-hat-ubuntu-fix/README.md)**

---

### 🕷️ [picrawler-setup/](picrawler-setup/)

#### ✅ Complete PiCrawler Ubuntu 24.04 Setup - WORKING!

**THE ROBOT WALKS!** Complete setup guide for getting the PiCrawler fully functional on Ubuntu 24.04.

**What We Fixed:**
- ✅ robot-hat I2C/SPI initialization
- ✅ GPIO library (lgpio for Pi 5)
- ✅ PiCrawler module installation
- ✅ All movement and servo control

**Quick Start:**
```bash
# Install lgpio for GPIO
sudo apt-get install -y python3-lgpio
sudo pip3 install rpi-lgpio --break-system-packages

# Install PiCrawler
git clone https://github.com/sunfounder/picrawler.git
cd picrawler
sudo python3 install.py
```

**[📖 Full Setup Guide →](picrawler-setup/UBUNTU_SETUP.md)**

---

### 📷 [vilib-investigation/](vilib-investigation/)

#### ⚠️ vilib Camera Library Ubuntu Investigation

Investigation into getting Sunfounder's vilib (vision library) working on Ubuntu 24.04 for Pi 5. 

**Camera Status:**
- ✅ **Camera hardware works!** Built libcamera v0.6.0 from source
- ✅ **CLI tools work**: rpicam-hello, rpicam-jpeg, rpicam-vid
- ❌ **Python picamera2**: Still uses old libcamera, doesn't see camera
- ❌ **vilib**: Depends on picamera2

**Solution**: Use command-line camera tools via subprocess in Python scripts.

**[📖 Full Investigation Report →](vilib-investigation/README.md)**

---

### 🤖 [ros2-gazebo/](ros2-gazebo/) *(Coming Soon)*

ROS2 integration and Gazebo simulation setup

- URDF model generation
- Gazebo world files
- ROS2 control nodes

---

### 🔌 [hardware/](hardware/) *(Coming Soon)*

Hardware documentation and wiring diagrams

- Component specifications
- Wiring schematics
- Power distribution
- Sensor placement

---

### 📖 [docs/](docs/) *(Coming Soon)*

Project documentation

- Setup guides
- API documentation
- Architecture diagrams

---

### 🛠️ [scripts/](scripts/) *(Coming Soon)*

Utility scripts and tools

- Setup automation
- Testing tools
- Deployment scripts

---

## 🚀 Quick Start

### Prerequisites

- Raspberry Pi 4 or 5
- Ubuntu 24.04 LTS (64-bit ARM)
- Sunfounder Robot HAT v4
- Internet connection

### Installation

**1. Install Robot HAT (Ubuntu-compatible):**

```bash
cd ~
git clone https://github.com/sunfounder/robot-hat.git -b v2.0
cd robot-hat
wget https://raw.githubusercontent.com/SpiritualCreations42/PicrawlerV2/main/robot-hat-ubuntu-fix/install_ubuntu.py
sudo python3 install_ubuntu.py
sudo reboot
```

**2. Verify Installation:**

```bash
ls /dev/i2c* /dev/spi*
# Should see: /dev/i2c-1, /dev/spidev0.0, /dev/spidev0.1
```

**3. Test Hardware:**

```bash
cd ~/robot-hat/tests
python3 servo_test.py
```

---

## 🎯 Project Goals

- [x] **Get Robot HAT working on Ubuntu 24.04** ✅ COMPLETE
- [x] **Install and test PiCrawler module** ✅ COMPLETE - Robot walks!
- [x] **Get camera working** ✅ COMPLETE - Built libcamera from source
- [x] **Document Ubuntu 24.04 compatibility** ✅ COMPLETE
- [ ] Create URDF model from FreeCAD design
- [ ] Set up Gazebo simulation environment
- [ ] Integrate ROS2 control
- [ ] Implement voice control pipeline
- [ ] Add computer vision (CLI tools work, need Python integration)
- [ ] Test additional sensors (IMU, ToF, ultrasonic)
- [ ] Autonomous navigation
- [ ] Web-based control interface

---

## 📊 Current Status

| Component | Ubuntu 24.04 Status | Notes |
|-----------|-------------------|-------|
| Robot HAT v4 | ✅ Working | Servos, motors, I2C, SPI all functional |
| Servos (12x) | ✅ Working | Tested on real hardware |
| PiCrawler Module | ✅ Working | All movement functions operational |
| GPIO Control | ✅ Working | lgpio library (Pi 5 compatible) |
| I2C Devices | ✅ Working | Manual module loading required |
| SPI Devices | ✅ Working | Manual module loading required |
| Pi Camera Module 3 | ✅ Working | Built libcamera v0.6.0 from source |
| Camera CLI Tools | ✅ Working | rpicam-hello, rpicam-jpeg, rpicam-vid |
| Camera Python (picamera2) | ❌ Not Working | Uses old libcamera, doesn't see camera |
| vilib Library | ❌ Not Working | Depends on picamera2 Python bindings |
| USB Webcam | ⚠️ Untested | Should work with OpenCV |
| Ultrasonic Sensor | ⚠️ Untested | Should work via Robot HAT |
| IMU (ICM-20948) | ⚠️ Untested | Should work via I2C |
| ToF (VL53L0X) | ⚠️ Untested | Should work via I2C |

---

## 🤝 Contributing

Found a bug or have an improvement? Feel free to open an issue or PR!

---

## 📄 License

This project is open source. Individual components may have different licenses:

- Robot HAT library: GPL-3.0 (Sunfounder)
- My modifications and additions: MIT License

---

## 🙏 Acknowledgments

- **Sunfounder** for the excellent PiCrawler platform and Robot HAT
- **Ubuntu** for ARM64 support on Raspberry Pi
- **ROS2** community for robotics tools

---

## 📧 Contact

**Author**: SpiritualCreations42  
**GitHub**: <https://github.com/SpiritualCreations42>  

---

**Let's build amazing robots together!** 🤖✨
# PicrawlerV2
