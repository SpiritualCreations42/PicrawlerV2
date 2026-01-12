# Robot HAT v4 - Ubuntu 24.04 Compatibility Fix

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
wget https://raw.githubusercontent.com/SpiritualCreations42/PiCrawler-Upgrades/main/robot-hat-ubuntu-fix/install_ubuntu.py
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
