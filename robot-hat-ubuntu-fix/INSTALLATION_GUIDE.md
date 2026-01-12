# Detailed Installation Guide - Robot HAT on Ubuntu 24.04

This guide walks you through installing the Sunfounder Robot HAT library on Ubuntu 24.04.

---

## Prerequisites

### Hardware Required:
- Raspberry Pi (3/4/5) running Ubuntu 24.04 LTS
- Sunfounder Robot HAT v4 (mounted on Pi)
- Power supply (6.0V-8.4V for Robot HAT)
- Internet connection

### Software Required:
- Ubuntu 24.04 LTS (64-bit ARM)
- Python 3 (comes with Ubuntu)
- sudo access

---

## Installation Steps

### Step 1: System Update
```bash
sudo apt update
sudo apt upgrade -y
```

### Step 2: Install Git (if not installed)
```bash
sudo apt install git -y
```

### Step 3: Clone Robot HAT Repository
```bash
cd ~
git clone https://github.com/sunfounder/robot-hat.git -b v2.0
cd robot-hat
```

### Step 4: Download Ubuntu Installer

**Option A - Direct Download:**
```bash
wget https://raw.githubusercontent.com/SpiritualCreations42/PiCrawler-Upgrades/main/robot-hat-ubuntu-fix/install_ubuntu.py
chmod +x install_ubuntu.py
```

**Option B - Manual Copy:**
If you already have `install_ubuntu.py` on your system:
```bash
# Copy it to the robot-hat directory
cp /path/to/install_ubuntu.py ~/robot-hat/
chmod +x install_ubuntu.py
```

### Step 5: Run the Installer
```bash
cd ~/robot-hat
sudo python3 install_ubuntu.py
```

**What happens during installation:**
- ✅ Installs robot_hat Python package
- ✅ Installs system dependencies (i2c-tools, espeak, SDL2, etc.)
- ✅ Installs Python dependencies (smbus2, gpiozero, pyaudio, etc.)
- ✅ Loads I2C kernel module (`i2c-dev`)
- ✅ Loads SPI kernel module (`spi_bcm2835`)
- ✅ Makes kernel modules persistent across reboots
- ✅ Adds your user to i2c/spi groups
- ✅ Copies device tree overlays

**Installation takes about 5-10 minutes.**

### Step 6: Reboot (CRITICAL!)
```bash
sudo reboot
```

**Why reboot is required:**
- Kernel modules need to initialize
- Group permissions need to apply
- Device tree overlays need to load

### Step 7: Verify Installation

After reboot, SSH back in and check:

**Check I2C devices:**
```bash
ls /dev/i2c*
# Expected: /dev/i2c-1 (or i2c-0)
```

**Check SPI devices:**
```bash
ls /dev/spi*
# Expected: /dev/spidev0.0, /dev/spidev0.1
```

**Check user groups:**
```bash
groups
# Should include: i2c, spi, gpio
```

**Check kernel modules:**
```bash
lsmod | grep -E 'i2c|spi'
# Should see: i2c_dev, spi_bcm2835
```

### Step 8: Test the Robot HAT

**Test Python import:**
```bash
python3 -c "from robot_hat import *; print('Robot HAT imported successfully!')"
```

**Run example scripts:**
```bash
cd ~/robot-hat/tests
python3 test_servo.py   # Test servo control
python3 test_motor.py   # Test motor control  
python3 test_battery.py # Test battery reading
```

---

## Installation Options

The installer supports optional flags:

### Skip Dependencies
```bash
sudo python3 install_ubuntu.py --no-dep
```
Use this if you already have dependencies installed.

### Library Only
```bash
sudo python3 install_ubuntu.py --only-lib
```
Installs only the Python library, skips hardware setup.

### No Build Isolation
```bash
sudo python3 install_ubuntu.py --no-build-isolation
```
Use if you have pip build issues.

### Combine Options
```bash
sudo python3 install_ubuntu.py --no-dep --only-lib
```

---

## What Gets Installed?

### APT Packages:
- `i2c-tools` - I2C utilities
- `espeak` - Text-to-speech
- `libsdl2-dev` - SDL2 development files
- `libsdl2-mixer-dev` - SDL2 mixer
- `portaudio19-dev` - Audio I/O library
- `sox` - Sound processing

### Python Packages:
- `smbus2` - I2C library
- `gpiozero` - GPIO control
- `pyaudio` - Audio interface
- `spidev` - SPI communication
- `pyserial` - Serial communication
- `pillow` - Image processing
- `pygame>=2.1.2` - Game/multimedia library

### Kernel Modules:
- `i2c-dev` - I2C device driver
- `spi_bcm2835` - SPI driver for BCM2835/2711/2712

---

## Next Steps

After successful installation:

1. **Build your robot project** - Use the Robot HAT library
2. **Add ROS2 integration** - Connect ROS2 to Robot HAT
3. **Voice control** - Use audio features for voice pipeline
4. **Computer vision** - Add camera and AI models

---

## Need Help?

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.
