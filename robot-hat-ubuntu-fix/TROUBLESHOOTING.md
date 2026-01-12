# Troubleshooting Guide - Robot HAT on Ubuntu 24.04

Common issues and solutions when installing/using Robot HAT on Ubuntu.

---

## Installation Issues

### ❌ "Script must be run as root"

**Problem:** You ran the installer without sudo.

**Solution:**
```bash
sudo python3 install_ubuntu.py
```

---

### ❌ "pip3: command not found"

**Problem:** Python pip is not installed.

**Solution:**
```bash
sudo apt update
sudo apt install python3-pip -y
```

---

### ❌ Package installation fails

**Problem:** Network issues or repository problems.

**Solution:**
```bash
# Update package lists
sudo apt update

# Fix broken dependencies
sudo apt --fix-broken install

# Try installation again
sudo python3 install_ubuntu.py
```

---

### ❌ "No module named 'version'"

**Problem:** You're not in the robot-hat directory.

**Solution:**
```bash
cd ~/robot-hat
sudo python3 install_ubuntu.py
```

---

## Hardware Issues

### ❌ No I2C devices after reboot

**Check if module is loaded:**
```bash
lsmod | grep i2c_dev
```

**If not loaded, load manually:**
```bash
sudo modprobe i2c-dev
```

**Make it permanent:**
```bash
echo 'i2c-dev' | sudo tee -a /etc/modules
```

**Check device permissions:**
```bash
ls -l /dev/i2c*
# Should be in i2c group
```

---

### ❌ No SPI devices after reboot

**Check if module is loaded:**
```bash
lsmod | grep spi
```

**If not loaded, load manually:**
```bash
sudo modprobe spi_bcm2835
```

**Make it permanent:**
```bash
echo 'spi_bcm2835' | sudo tee -a /etc/modules
```

---

### ❌ Permission denied accessing /dev/i2c-1

**Problem:** Your user is not in the i2c group.

**Solution:**
```bash
# Add user to i2c group
sudo usermod -a -G i2c $USER

# Log out and back in, then verify
groups
# Should see: i2c
```

---

### ❌ Permission denied accessing /dev/spidev0.0

**Problem:** Your user is not in the spi group.

**Solution:**
```bash
# Check if spi group exists
getent group spi

# If exists, add user to group
sudo usermod -a -G spi $USER

# If doesn't exist, create it
sudo groupadd spi
sudo chown root:spi /dev/spidev*
sudo chmod g+rw /dev/spidev*
sudo usermod -a -G spi $USER

# Log out and back in
```

---

## Python/Library Issues

### ❌ "ModuleNotFoundError: No module named 'robot_hat'"

**Problem:** Robot HAT library not installed or not in Python path.

**Solution:**
```bash
# Reinstall the library
cd ~/robot-hat
sudo python3 install_ubuntu.py --only-lib

# Or use pip directly
sudo pip3 install ./
```

---

### ❌ Import errors for dependencies (smbus2, gpiozero, etc.)

**Problem:** Dependencies not installed.

**Solution:**
```bash
# Reinstall with dependencies
cd ~/robot-hat
sudo python3 install_ubuntu.py

# Or install specific missing package
sudo pip3 install smbus2 gpiozero --break-system-packages
```

---

### ❌ "No module named 'pygame'"

**Problem:** Pygame not installed or wrong version.

**Solution:**
```bash
sudo pip3 install 'pygame>=2.1.2' --break-system-packages
```

---

## Audio Issues

### ❌ No audio output from speaker

**Check audio devices:**
```bash
aplay -l
# Should list audio devices
```

**Test audio:**
```bash
speaker-test -t wav -c 2
```

**If no audio devices:**
```bash
sudo apt install alsa-utils -y
sudo alsactl init
```

---

### ❌ espeak not working

**Solution:**
```bash
sudo apt install espeak -y

# Test
espeak "Hello World"
```

---

## Servo/Motor Issues

### ❌ Servos not responding

**Check power supply:**
- Robot HAT requires 6.0V-8.4V
- Battery must be connected and charged
- Check power LED indicators on HAT

**Test servo directly:**
```bash
cd ~/robot-hat/tests
python3 servo_test.py
```

**Check I2C communication:**
```bash
# Scan for I2C devices
sudo i2cdetect -y 1
# Should see device at 0x14 (Robot HAT MCU)
```

---

### ❌ Motors not responding

**Check connections:**
- Motor wires properly connected to M1/M2
- Power supply connected
- Battery charged

**Test motor directly:**
```bash
cd ~/robot-hat/tests
python3 motor_test.py
```

---

## System Issues

### ❌ Robot HAT not detected

**Check physical connection:**
- HAT properly seated on GPIO pins
- No bent pins
- Power connected

**Check I2C:**
```bash
sudo i2cdetect -y 1
```
Should see device at `0x14` (Robot HAT MCU)

If not:
```bash
# Reload I2C module
sudo modprobe -r i2c_dev
sudo modprobe i2c-dev

# Check again
sudo i2cdetect -y 1
```

---

### ❌ System crashes or freezes

**Possible causes:**
- Power supply insufficient
- Short circuit on HAT
- Overheating

**Solutions:**
- Use adequate power supply (2.5A+ for Pi 4/5)
- Check for shorts on HAT
- Ensure proper cooling
- Check system logs: `sudo dmesg | tail -50`

---

### ❌ Reboots after installation don't persist changes

**Problem:** Modules not loading on boot.

**Solution:**
```bash
# Verify modules in /etc/modules
cat /etc/modules

# Should contain:
# i2c-dev
# spi_bcm2835

# If missing, add them:
echo 'i2c-dev' | sudo tee -a /etc/modules
echo 'spi_bcm2835' | sudo tee -a /etc/modules

# Reboot
sudo reboot
```

---

## Upgrade/Reinstall Issues

### ❌ Want to reinstall everything

**Complete reinstall:**
```bash
cd ~/robot-hat
sudo pip3 uninstall robot-hat -y
sudo python3 install_ubuntu.py
sudo reboot
```

---

### ❌ Upgrade from Raspbian to Ubuntu

**Problem:** Existing Raspbian installation conflicts.

**Solution:**
```bash
# Uninstall old version
sudo pip3 uninstall robot-hat -y

# Remove old configs
sudo rm -rf ~/.robot-hat

# Fresh install with Ubuntu version
cd ~/robot-hat
sudo python3 install_ubuntu.py
sudo reboot
```

---

## Still Having Issues?

### Check Logs
```bash
# System logs
sudo dmesg | grep -i "i2c\|spi\|gpio"

# Python errors
python3 -c "from robot_hat import *" 2>&1
```

### Get Help
1. **GitHub Issues**: Open an issue on this repo
2. **Sunfounder Forum**: https://forum.sunfounder.com/
3. **Community**: Join robotics communities on Discord/Reddit

### Provide These Details
When asking for help, include:
- Ubuntu version: `lsb_release -a`
- Raspberry Pi model: `cat /proc/cpuinfo | grep Model`
- Python version: `python3 --version`
- Error messages (full text)
- Output of: `ls /dev/i2c* /dev/spi*`
- Output of: `lsmod | grep -E 'i2c|spi'`

---

**Happy Building! 🤖**
