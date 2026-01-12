# vilib Ubuntu 24.04 Compatibility Report

## Status: ⚠️ NOT COMPATIBLE (Pi 5 Hardware Limitation)

### Summary
vilib can be **installed** on Ubuntu 24.04, but **cannot use the camera** on Raspberry Pi 5 due to libcamera version incompatibility.

### Root Cause
- **Ubuntu 24.04** ships with `libcamera v0.2.0`
- **Raspberry Pi 5** requires `libcamera v0.3.0+` with rp1-cfe pipeline support
- Pi 5 uses new camera interface (rp1-cfe), not the old Unicam interface

### Hardware Status ✅
Camera hardware is fully functional:
- ✅ Camera Module 3 (imx708) detected by kernel
- ✅ All V4L2 devices present (`/dev/video0-37`, `/dev/media0-3`)
- ✅ Media pipeline connections established
- ✅ Camera sensor accessible via i2c (address 0x1a on i2c-10)

### Software Status ❌
libcamera cannot access camera:
```
DEBUG RPI vc4.cpp:179 Unable to acquire a Unicam instance
```
libcamera v0.2.0 only has VC4 pipeline handler (Pi 4), not rp1-cfe (Pi 5)

### What Works
1. ✅ vilib package installation
2. ✅ picamera2 installation  
3. ✅ All Python dependencies
4. ✅ OpenCV with system camera
5. ✅ robot-hat (I2C/SPI devices)

### What Doesn't Work
1. ❌ Camera detection via libcamera
2. ❌ Camera access via picamera2
3. ❌ vilib import (crashes due to camera init)

### Solutions

#### Option 1: Use Raspberry Pi OS ⭐ RECOMMENDED
Raspberry Pi OS ships with libcamera v0.3.0+ which fully supports Pi 5.

#### Option 2: Build libcamera from Source (Advanced)
```bash
# Build Raspberry Pi's libcamera fork
# Complex, time-consuming, potential system conflicts
# Not recommended unless you need Ubuntu specifically
```

#### Option 3: Wait for Ubuntu
Ubuntu will eventually update to libcamera v0.3.0+

#### Option 4: Use USB Webcam
Bypass Pi camera entirely, use USB webcam with V4L2

### Installation Steps Attempted

#### Dependencies Installed
```bash
# System packages
sudo apt-get install -y \
    libcap-dev \
    python3-libcamera \
    libcamera-ipa \
    libcamera-tools \
    python3-opencv \
    opencv-data \
    ffmpeg \
    v4l-utils

# Python packages
sudo pip3 install picamera2 --break-system-packages
sudo pip3 install Flask --break-system-packages --ignore-installed blinker
```

#### Workarounds Applied
1. **libcamera symlink** - Linked system libcamera to pip location:
   ```bash
   sudo ln -sf /usr/lib/aarch64-linux-gnu/python3.12/site-packages/libcamera \
       /usr/local/lib/python3.12/dist-packages/libcamera
   ```

2. **picamera2 preview patch** - Made DRM preview optional (no pykms):
   ```bash
   # Patched: /usr/local/lib/python3.12/dist-packages/picamera2/previews/__init__.py
   # Made DrmPreview import optional (wrapped in try/except)
   ```

3. **Media pipeline configuration** - Attempted manual V4L2 setup:
   ```bash
   media-ctl -d /dev/media0 -l "'imx708':0 -> 'csi2':0[1]"
   media-ctl -d /dev/media0 -V "'imx708':0 [fmt:SRGGB10_1X10/1920x1080]"
   # Still couldn't capture frames - needs full ISP pipeline
   ```

### Diagnostic Commands Used
```bash
# Check camera hardware
libcamera-hello --list-cameras  # Not available on Ubuntu
vcgencmd get_camera             # Not available on Ubuntu
v4l2-ctl --list-devices         # Shows rp1-cfe devices
media-ctl -p                    # Shows imx708 sensor detected

# Check libcamera
cam -l                          # Shows "Unable to acquire Unicam"
LIBCAMERA_LOG_LEVELS=*:DEBUG cam -l

# Check Python
python3 -c "from picamera2 import Picamera2; print(Picamera2.global_camera_info())"
# Returns: [] (empty list)
```

### Files Modified
- `/usr/local/lib/python3.12/dist-packages/picamera2/previews/__init__.py`
  - Made DrmPreview import optional (no pykms dependency)
  - Made QtPreview/QtGlPreview imports optional

### Error Messages Encountered

1. **python-prctl dependency**:
   ```
   You need to install libcap development headers to build this module
   ```
   **Solution**: `sudo apt-get install libcap-dev`

2. **pykms missing**:
   ```
   ModuleNotFoundError: No module named 'pykms'
   ```
   **Solution**: Patched picamera2 to make preview optional

3. **Flask/blinker conflict**:
   ```
   ERROR: Cannot uninstall blinker 1.7.0, RECORD file not found
   ```
   **Solution**: `pip3 install Flask --ignore-installed blinker`

4. **libcamera camera detection**:
   ```
   DEBUG RPI vc4.cpp:179 Unable to acquire a Unicam instance
   ```
   **No solution**: Fundamental libcamera version limitation

### Tested On
- **Hardware**: Raspberry Pi 5 (16GB RAM)
- **OS**: Ubuntu 24.04.1 LTS (Noble Numbat)
- **Kernel**: 6.8.12
- **Camera**: Raspberry Pi Camera Module 3 (imx708 sensor)
- **libcamera**: v0.2.0-3fakesync1build6 (Ubuntu package)
- **Date**: January 11-12, 2025

### Key Findings

1. **Ubuntu's libcamera is outdated for Pi 5**
   - Only includes VC4 pipeline (Pi 4 and earlier)
   - Missing rp1-cfe pipeline (Pi 5 new camera interface)

2. **Hardware is fully functional**
   - All kernel drivers loaded correctly
   - Camera detected by V4L2 subsystem
   - Media pipeline connections established

3. **Manual V4L2 configuration doesn't work**
   - Pi 5's camera requires full ISP pipeline
   - Raw Bayer data needs processing
   - libcamera normally handles this automatically

### Conclusion
**For Pi 5 + Camera + Ubuntu 24.04: Not currently possible without building libcamera from source**

**Recommendations**:
- **For camera projects**: Use Raspberry Pi OS (has libcamera v0.3.0+)
- **For robotics without camera**: Ubuntu 24.04 works great! robot-hat fully functional
- **Future**: Monitor Ubuntu updates for libcamera v0.3.0+

### Related Work
This investigation complements the successful **robot-hat Ubuntu fix**:
- ✅ [robot-hat Ubuntu 24.04 compatibility](../robot-hat-ubuntu-fix/)
- ✅ Servos, motors, I2C, SPI all working perfectly on Ubuntu

---

## References
- [libcamera Documentation](https://libcamera.org/)
- [Raspberry Pi Camera Documentation](https://www.raspberrypi.com/documentation/computers/camera_software.html)
- [picamera2 Documentation](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)
- [V4L2 Documentation](https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/v4l2.html)

**Status**: Investigation complete. Solution: Use Raspberry Pi OS for camera functionality on Pi 5.
