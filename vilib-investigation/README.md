# vilib Ubuntu 24.04 Investigation

⚠️ **Status**: NOT COMPATIBLE with Raspberry Pi 5

## Quick Summary

We attempted to get Sunfounder's vilib (vision library) working on Ubuntu 24.04 for Raspberry Pi 5. While we successfully installed all dependencies, **the camera cannot be accessed** due to Ubuntu's outdated libcamera version.

## The Problem

- **Ubuntu 24.04**: Ships with libcamera v0.2.0
- **Raspberry Pi 5**: Requires libcamera v0.3.0+ with rp1-cfe support
- **Result**: Camera hardware is detected but libcamera cannot access it

## What We Accomplished

### ✅ Successfully Installed
- vilib Python package
- picamera2 via pip
- All system dependencies (libcamera-ipa, libcamera-tools, opencv, etc.)
- Applied workarounds for Ubuntu-specific issues

### ⚠️ Issues Resolved
1. **libcap-dev missing** - Added to dependencies
2. **libcamera bindings** - Symlinked system to pip location  
3. **pykms unavailable** - Patched picamera2 for headless operation
4. **Flask/scipy conflicts** - Used `--ignore-installed` flag

### ❌ Unsolvable Issue
**libcamera v0.2.0 doesn't support Pi 5's rp1-cfe camera interface**

Error message:
```
DEBUG RPI vc4.cpp:179 Unable to acquire a Unicam instance
```

## Hardware Status

✅ **Everything works at hardware level:**
- Camera Module 3 (imx708) detected
- Kernel drivers loaded
- V4L2 devices present
- Media pipeline connections established
- i2c communication working

❌ **Software incompatibility:**
- libcamera v0.2.0 only has VC4 pipeline (Pi 4)
- Pi 5 needs rp1-cfe pipeline
- No amount of configuration fixes this

## Files in This Directory

- **UBUNTU_COMPATIBILITY.md** - Full investigation report with all details
- **install_ubuntu_v2.py** - Improved vilib installer (for future when libcamera updates)

## Solutions

### Option 1: Use Raspberry Pi OS ⭐ RECOMMENDED
Raspberry Pi OS has libcamera v0.3.0+ with full Pi 5 support.

### Option 2: Wait for Ubuntu
Ubuntu will eventually update libcamera. Monitor package updates.

### Option 3: Use USB Webcam
Bypass the Pi Camera Module entirely, use USB webcam with V4L2/OpenCV.

### Option 4: Build from Source (Advanced)
Build libcamera v0.3.0+ from Raspberry Pi's source. Complex and time-consuming.

## Lessons Learned

1. **Ubuntu for Pi is still maturing** - Raspberry Pi OS has better hardware support
2. **Camera support is complex** - Requires kernel drivers + userspace libraries + pipelines
3. **Pi 5 changed everything** - New camera interface breaks old assumptions
4. **robot-hat works great!** - For robotics without camera, Ubuntu 24.04 is excellent

## Related Success

While vilib doesn't work, we successfully created:
- **[robot-hat Ubuntu 24.04 fix](../robot-hat-ubuntu-fix/)** ✅ Fully working!
  - All servos working
  - I2C/SPI functional
  - Motor control operational
  - Tested on real hardware

## For Future Reference

When Ubuntu updates libcamera to v0.3.0+, this investigation provides:
- Complete dependency list
- Known workarounds for Ubuntu-specific issues
- Installation steps that worked
- Troubleshooting commands

## Tested Configuration

- **Board**: Raspberry Pi 5 (16GB)
- **OS**: Ubuntu 24.04.1 LTS
- **Camera**: Raspberry Pi Camera Module 3
- **Date**: January 11-12, 2025

## Recommendation

**For camera projects on Pi 5: Use Raspberry Pi OS**

**For robotics projects without camera: Ubuntu 24.04 works perfectly!**

See our robot-hat fix for full Ubuntu compatibility with servos, motors, and sensors.

---

*Investigation complete. We tried everything possible at the software level. The limitation is fundamental to Ubuntu's libcamera version.*
