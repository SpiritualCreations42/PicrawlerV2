#!/usr/bin/env python3
from distutils.log import warn
import os, sys
import time
import threading

# version
sys.path.append('./vilib')

import pwd
owner_uid = os.stat(__file__).st_uid
user_name = pwd.getpwuid(owner_uid).pw_name

from version import __version__
print("Start installing vilib %s for user %s (Ubuntu Edition)"%(__version__ ,user_name))

# define color print
def warn(msg, end='\n', file=sys.stdout, flush=False):
    print(f'\033[0;33m{msg}\033[0m', end=end, file=file, flush=flush)

def error(msg, end='\n', file=sys.stdout, flush=False):
    print(f'\033[0;31m{msg}\033[0m', end=end, file=file, flush=flush)

# check if run as root
if os.geteuid() != 0:
    warn("Script must be run as root. Try \"sudo python3 install_ubuntu.py\".")
    sys.exit(1)

# global variables defined
errors = []

avaiable_options = ['-h', '--help', '--no-dep']

usage = '''
Usage:
    sudo python3 install_ubuntu.py [option]

Options:
               --no-dep    Do not download dependencies
    -h         --help      Show this help text and exit
'''

# utils
def run_command(cmd=""):
    import subprocess
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read().decode('utf-8')
    status = p.poll()
    return status, result

at_work_tip_sw = False
def working_tip():
    char = ['/', '-', '\\', '|']
    i = 0
    global at_work_tip_sw
    while at_work_tip_sw:
            i = (i+1)%4
            sys.stdout.write('\033[?25l')
            sys.stdout.write('%s\033[1D'%char[i])
            sys.stdout.flush()
            time.sleep(0.5)

    sys.stdout.write(' \033[1D')
    sys.stdout.write('\033[?25h')
    sys.stdout.flush()

def do(msg="", cmd=""):
    print(" - %s ... " % (msg), end='', flush=True)
    global at_work_tip_sw
    at_work_tip_sw = True
    _thread = threading.Thread(target=working_tip)
    _thread.daemon = True
    _thread.start()
    status, result = run_command(cmd)
    at_work_tip_sw = False
    while _thread.is_alive():
        time.sleep(0.01)
    if status == 0 or status == None or result == "":
        print('Done')
    else:
        print('\033[1;35mError\033[0m')
        errors.append("%s error:\n  Status:%s\n  Error:%s" %
                      (msg, status, result))

def check_rpi_model():
    """Check Pi model - works on both Raspbian and Ubuntu"""
    _, result = run_command("cat /proc/device-tree/model 2>/dev/null | awk '{print $3}'")
    result = result.strip()
    if result == '3':
        return int(3)
    elif result == '4':
        return int(4)
    elif result == '5':
        return int(5)
    else:
        # Default to 4 if unknown (safe assumption for modern Pi)
        return int(4)

def detect_os():
    """Detect if running Ubuntu or Raspbian"""
    status, result = run_command("cat /etc/os-release | grep ^ID=")
    if "ubuntu" in result.lower():
        return "ubuntu"
    else:
        return "raspbian"

def check_ubuntu_version():
    """Get Ubuntu version (e.g., 24.04 returns 24)"""
    _, result = run_command("lsb_release -rs | cut -d'.' -f1")
    try:
        return int(result.strip())
    except:
        return 24  # Default to 24 if can't detect

def check_raspbain_version():
    """
    Check OS version - works for both Raspbian and Ubuntu
    For Ubuntu: returns equivalent Debian version
    Ubuntu 24.04 = Debian 12+ equivalent
    """
    os_type = detect_os()
    
    if os_type == "ubuntu":
        ubuntu_ver = check_ubuntu_version()
        # Map Ubuntu to Debian equivalent
        # Ubuntu 24.04 = Debian 12+ (bookworm)
        # Ubuntu 22.04 = Debian 11 (bullseye)
        if ubuntu_ver >= 24:
            return 12
        elif ubuntu_ver >= 22:
            return 11
        else:
            return 11
    else:
        # Original Raspbian detection
        _, result = run_command("cat /etc/debian_version | awk -F. '{print $1}'")
        try:
            return int(result.strip())
        except:
            return 12

def check_python_version():
    import sys
    major = int(sys.version_info.major)
    minor = int(sys.version_info.minor)
    micro = int(sys.version_info.micro)
    return major, minor, micro

def check_os_bit():
    _ , os_bit = run_command("getconf LONG_BIT")
    return int(os_bit)

# print system and hardware information
os_type = detect_os()
rpi_model = check_rpi_model()
python_version = check_python_version()
raspbain_version = check_raspbain_version()
os_bit = check_os_bit()

print(f"Detected OS: {os_type}")
print(f"Python version: {python_version[0]}.{python_version[1]}.{python_version[2]}")
print(f"OS version equivalent: Debian {raspbain_version} ({os_bit}bit)")
print(f"Raspberry Pi model: {rpi_model}")
print("")

# check system - Ubuntu 24.04 is equivalent to Debian 12+
if raspbain_version <= 10:
    warn('System not be supported. Requires Debian 11 (bullseye) or Ubuntu 22.04+')
    print('Please use newer system or use "legacy" branch.')
    sys.exit(1)

# Dependencies list installed with apt
# Note: On Ubuntu, python3-picamera2 and rpicam-apps are not available via apt
APT_INSTALL_LIST = [
    "python3-libcamera",
    "libcap-dev",  # Required for python-prctl (picamera2 dependency)
    "python3-pyqt5",
    "python3-opengl",
    "python3-opencv",
    "opencv-data",
    "ffmpeg",
    # mediapipe dependencies
    "libgtk-3-0",
    "libxcb-shm0",
    "libcdio-paranoia-dev",
    "libsdl2-2.0-0",
    "libxv1",
    "libtheora0",
    "libva-drm2",
    "libva-x11-2",
    "libvdpau1",
    "libharfbuzz0b",
    "libbluray2",
    "libzbar0",
    "libopenblas-dev",
]

# Dependencies list installed with pip3
# Note: picamera2 must be installed via pip on Ubuntu (not available via apt)
PIP_INSTALL_LIST = [
    "picamera2",  # CRITICAL: Install via pip on Ubuntu
    "imutils",
    "qrcode",
    "pyzbar",
    "pyzbar[scripts]",
    "readchar",
    'protobuf>=3.20.0',
]

# check whether mediapipe is supported
# Note: On Ubuntu, may conflict with system scipy - use --ignore-installed
is_mediapipe_supported = False
if os_bit == 64 and raspbain_version >= 11 and python_version[0] == 3 and python_version[1] < 13:
    is_mediapipe_supported = True
else:
    is_mediapipe_supported = False
    warn("mediapipe is only supported on 64bit system with python 3.12 or older.")

if raspbain_version > 11:
    PIP_INSTALL_LIST.append("numpy")
else:
    PIP_INSTALL_LIST.append("numpy==1.26.4")

is_tensorflow_supported = False
if python_version[0] == 3 and python_version[1] < 13:
    is_tensorflow_supported = True
    PIP_INSTALL_LIST.append("tflite-runtime")
    APT_INSTALL_LIST.append("libatlas-base-dev")
    # Ubuntu-specific: check for correct libhdf5 package name
    if os_type == "ubuntu":
        # Ubuntu 24.04 uses different package name
        _, hdf5_check = run_command("apt-cache search libhdf5 | grep -E 'libhdf5-[0-9]+$' | head -1 | awk '{print $1}'")
        hdf5_pkg = hdf5_check.strip()
        if hdf5_pkg:
            APT_INSTALL_LIST.append(hdf5_pkg)
        else:
            APT_INSTALL_LIST.append("libhdf5-dev")  # Fallback
    else:
        APT_INSTALL_LIST.append("libhdf5-130")
else:
    is_tensorflow_supported = False
    warn("tflite-runtime is only supported on python 3.12 or older.")

# main function
def install():
    options = []
    if len(sys.argv) > 1:
        options = sys.argv[1:]
        for opt in options:
            if opt not in avaiable_options:
                print("Option {} is not found.".format(opt))
                print(usage)
                sys.exit(0)
        if "-h" in options or "--help" in options:
            print(usage)
            sys.exit(0)

    # check whether pip has the option "--break-system-packages"
    _is_bsps = ''
    status, _ = run_command("pip3 help install|grep break-system-packages")
    if status == 0:
        _is_bsps = "--break-system-packages"

    print("Install vilib python package")
    do(msg="pip3 install ./",
        cmd=f'pip3 install ./ {_is_bsps}')
    do(msg="cleanup",
        cmd='rm -rf vilib.egg-info')

    if "--no-dep" not in options:
        # install dependencies with apt
        print("apt install dependency:")
        do(msg="dpkg configure",
            cmd='dpkg --configure -a')
        do(msg="update apt-get",
            cmd='apt-get update -y')
        for dep in APT_INSTALL_LIST:
            do(msg=f"install {dep}",
                cmd=f'apt-get install {dep} -y')

        # install dependencies with pip
        print("pip3 install dependency:")

        if _is_bsps != '':
            print("\033[38;5;8m pip3 install with --break-system-packages\033[0m")
        
        # update pip
        do(msg="update pip3", cmd="apt-get upgrade -y python3-pip")
        
        # Install core dependencies
        for dep in PIP_INSTALL_LIST:
            if dep.endswith('.whl'):
                dep_name = dep.split("/")[-1]
            else:
                dep_name = dep
            do(msg=f"install {dep_name}",
                cmd=f'pip3 install {dep} {_is_bsps}')
        
        # Install optional packages (may conflict with system packages)
        print("\nInstalling optional packages (AI/ML features)...")
        
        # Flask (optional - for web interface)
        if os_type == "ubuntu":
            print("  Flask: Installing with --ignore-installed to avoid conflicts...")
            do(msg="install Flask (optional)",
                cmd=f'pip3 install Flask {_is_bsps} --ignore-installed blinker')
        
        # mediapipe (optional - for advanced vision)
        if is_mediapipe_supported:
            print("  mediapipe: Installing with --ignore-installed to avoid conflicts...")
            do(msg="install mediapipe (optional)",
                cmd=f'pip3 install mediapipe {_is_bsps} --ignore-installed scipy protobuf')
        else:
            print('\033[38;5;8m  mediapipe is not supported on this platform... Skip \033[0m')
        
        # tflite-runtime (optional - for TensorFlow Lite)
        if is_tensorflow_supported:
            # tflite-runtime often not available for newer Python versions
            print("  tflite-runtime: Attempting install (may fail on newer Python)...")
            status, _ = run_command(f'pip3 install tflite-runtime {_is_bsps}')
            if status != 0:
                print('\033[38;5;8m  tflite-runtime install failed (not critical) \033[0m')
        else:
            print('\033[38;5;8m  tflite-runtime is not supported on this platform... Skip \033[0m')
    
    # Fix libcamera linking issue on Ubuntu
    # =====================================
    if os_type == "ubuntu":
        print("\nFixing libcamera Python bindings for Ubuntu...")
        print("  Ubuntu installs libcamera to arch-specific site-packages,")
        print("  but pip's picamera2 looks in local dist-packages.")
        print("  Creating symlinks...")
        
        # Find the Python version
        py_version = f"{python_version[0]}.{python_version[1]}"
        
        # Ubuntu uses arch-specific path for system packages
        system_path = f"/usr/lib/aarch64-linux-gnu/python{py_version}/site-packages"
        local_path = f"/usr/local/lib/python{py_version}/dist-packages"
        
        # Check if libcamera exists in system packages
        libcamera_path = f"{system_path}/libcamera"
        status, result = run_command(f"test -d {libcamera_path} && echo 'exists'")
        
        if "exists" in result:
            # Create symlink for libcamera package
            do(msg="link libcamera package",
                cmd=f'ln -sf {libcamera_path} {local_path}/libcamera')
            print("  ✓ libcamera linking complete")
        else:
            warn(f"  Could not find libcamera at {libcamera_path}")
            warn("  picamera2 may not work - try: sudo apt-get install python3-libcamera")

    print("\nCreate workspace")
    if not os.path.exists('/opt'):
        os.mkdir('/opt')
        run_command('chmod 774 /opt')
        run_command(f'chown -R {user_name}:{user_name} /opt')
    do(msg="create dir",
        cmd='mkdir -p /opt/vilib'
        + ' && chmod 774 /opt/vilib'
        + f' && chown -R {user_name}:{user_name} /opt/vilib'
        )
    do(msg="copy workspace",
        cmd='cp -r ./workspace/* /opt/vilib/'
        + ' && chmod 774 /opt/vilib/*'
        + f' && chown -R {user_name}:{user_name} /opt/vilib/*'
        )

    # check errors
    if len(errors) == 0:
        print("\n" + "="*60)
        print("✅ vilib installation completed successfully!")
        print("="*60)
        print("\nNext steps:")
        print("  1. Test vilib import:")
        print("     python3 -c 'import vilib; print(vilib.__version__)'")
        print("\n  2. Test camera with picamera2:")
        print("     libcamera-hello -t 3000")
        print("\n  3. Check examples:")
        print("     ls /opt/vilib/")
        print("\n  4. Test vilib camera:")
        print("     cd ~/vilib/examples")
        print("     python3 [example_file].py")
        print("\n" + "="*60)
    else:
        print("\n\n⚠️  Some errors occurred during installation:")
        print("="*60)
        for error in errors:
            print(error)
        print("="*60)
        print("\n💡 Note: Core vilib functionality may still work.")
        print("   Some optional features (AI/ML) may be unavailable.")
        print("   Contact service@sunfounder.com if you need these features.")


if __name__ == "__main__":
    try:
        install()
    except KeyboardInterrupt:
        print("\n\nCanceled.")
    finally:
        sys.stdout.write(' \033[1D')
        sys.stdout.write('\033[?25h')
        sys.stdout.flush()
