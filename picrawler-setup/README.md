# PiCrawler Setup Guide

✅ **Complete Ubuntu 24.04 compatibility achieved!**

## Quick Links

- **[UBUNTU_SETUP.md](UBUNTU_SETUP.md)** - Complete setup guide for Ubuntu 24.04
- **[Troubleshooting](#troubleshooting)** - Common issues and solutions

## What Works

- ✅ Robot HAT v4 - All servos, I2C, SPI
- ✅ PiCrawler movement - All gaits and functions
- ✅ GPIO control - Using lgpio (Pi 5 compatible)
- ✅ Camera - Command-line tools (rpicam-hello, rpicam-jpeg)

## What Doesn't

- ❌ Python camera access (picamera2) - Use CLI tools instead
- ❌ vilib - Incompatible with Ubuntu's libcamera

## Installation Summary

```bash
# 1. Install robot-hat (Ubuntu compatible)
cd ~
git clone https://github.com/sunfounder/robot-hat.git -b v2.0
cd robot-hat
wget https://raw.githubusercontent.com/SpiritualCreations42/PicrawlerV2/main/robot-hat-ubuntu-fix/install_ubuntu.py
sudo python3 install_ubuntu.py
sudo reboot

# 2. Install GPIO library
sudo apt-get install -y python3-lgpio
sudo pip3 install rpi-lgpio --break-system-packages

# 3. Install PiCrawler
cd ~
git clone https://github.com/sunfounder/picrawler.git
cd picrawler
sudo python3 install.py

# 4. Test!
cd ~/picrawler/examples
sudo python3 move.py
```

## Troubleshooting

### "BadPinFactory" error
Install lgpio:
```bash
sudo apt-get install python3-lgpio
sudo pip3 install rpi-lgpio --break-system-packages
```

### Servos don't work
Check I2C:
```bash
ls /dev/i2c*  # Should show /dev/i2c-1
i2cdetect -y 1  # Should show 0x14
```

### Camera not working
Use command-line tools:
```bash
rpicam-hello --list-cameras
rpicam-jpeg -o test.jpg
```

---

**See [UBUNTU_SETUP.md](UBUNTU_SETUP.md) for full documentation!**
