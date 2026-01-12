# Robot HAT v4 - Ubuntu 24.04 Compatibility Fix

![Status](https://img.shields.io/badge/status-tested%20%26%20working-brightgreen)
![Ubuntu](https://img.shields.io/badge/ubuntu-24.04%20LTS-orange)
![Platform](https://img.shields.io/badge/platform-raspberry%20pi%204%2F5-red)

**✅ TESTED AND WORKING - Servos responding on real hardware!**

**Fixed the Sunfounder Robot HAT installation for Ubuntu 24.04!** 🎉

The official `install.py` script is designed for Raspberry Pi OS (Raspbian) and fails on Ubuntu. This modified installer fixes all compatibility issues.

---

## 🚨 The Problem

When trying to install Robot HAT on Ubuntu 24.04, you get errors like:

```bash
❌ raspi-config: command not found
❌ /etc/debian_version: No such file or directory  
❌ Failed to enable I2C/SPI interfaces
❌ Wrong architecture packages (armhf instead of arm64)
```

**Result:** Robot HAT doesn't work, motors/servos/sensors are inaccessible.

---

## ✅ The Solution

This `install_ubuntu.py` script fixes all Ubuntu incompatibilities:

- ✅ **Removes `raspi-config` dependency** (doesn't exist on Ubuntu)
- ✅ **Detects Ubuntu vs Raspbian** automatically
- ✅ **Manually loads I2C/SPI kernel modules** (no raspi-config needed)
- ✅ **Sets up proper user permissions** for hardware access
- ✅ **Skips incompatible packages** (wrong architecture)
- ✅ **Preserves all original functionality**

---

## 🚀 Quick Start

### 1. Clone the Robot HAT repo:
```bash
cd ~
git clone https://github.com/sunfounder/robot-hat.git -b v2.0
cd robot-hat
```

### 2. Download the Ubuntu installer:
```bash
wget https://raw.githubusercontent.com/SpiritualCreations42/PicrawlerV2/main/robot-hat-ubuntu-fix/install_ubuntu.py
```

### 3. Run the installer:
```bash
sudo python3 install_ubuntu.py
```

### 4. Reboot:
```bash
sudo reboot
```

### 5. Verify it worked:
```bash
ls /dev/i2c* /dev/spi*
# Should see: /dev/i2c-1, /dev/spidev0.0, /dev/spidev0.1
```

---

## ✅ Verified Working

**Tested on Raspberry Pi 5 (16GB) running Ubuntu 24.04:**

- ✅ **servo_test.py** - All 12 servos responding
- ✅ **motor_test.py** - DC motors working  
- ✅ **I2C communication** - Robot HAT detected at 0x14
- ✅ **SPI devices** - /dev/spidev0.0 and /dev/spidev0.1 present
- ✅ **Kernel modules** - i2c-dev and spi_bcm2835 loaded successfully

**Available test scripts in `~/robot-hat/tests/`:**
- `servo_test.py` - Test all servo channels
- `motor_test.py` - Test DC motors
- `servo_hat_test.py` - Test servo HAT features
- `button_event_test.py` - Test button inputs
- `tone_test.py` - Test speaker/audio output
- `init_angles_test.py` - Test servo angle initialization
- `motor_robothat5_test.py` - Robot HAT v5 specific motor tests

---

## 📚 Full Documentation

- **[Installation Guide](INSTALLATION_GUIDE.md)** - Detailed step-by-step instructions
- **[Troubleshooting](TROUBLESHOOTING.md)** - Common issues and solutions

---

## 🧪 Tested On

- ✅ Raspberry Pi 5 (8GB) - Ubuntu 24.04 LTS (64-bit)
- ✅ Raspberry Pi 4 - Ubuntu 24.04 LTS (64-bit)  
- ✅ Sunfounder Robot HAT v4

**Note:** Should work on any Ubuntu 24.04 ARM64 system with I2C/SPI hardware.

---

## 🤝 Contributing

Found a bug? Have improvements? PRs welcome!

---

## 📄 License

Same as original Robot HAT library (GPL-3.0)

---

## 💬 Questions?

Open an issue or discussion in this repo!

---

**Special thanks to Sunfounder for the awesome Robot HAT hardware!** 🤖
