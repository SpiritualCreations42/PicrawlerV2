#!/usr/bin/env python3
from os import path
import sys
import os
import time
import threading

here = path.abspath(path.dirname(__file__))
os.chdir(here)

# Try to import version from robot_hat if available, otherwise use default
__version__ = "1.0.0"
try:
    sys.path.append('./robot_hat')
    from version import __version__
except ImportError:
    pass  # Use default version if robot_hat not yet cloned

print("Robot Hat Python Library v%s (Ubuntu Edition)" % __version__)

avaiable_options = ["--no-dep", "--only-lib", "--no-build-isolation"]
options = []
if len(sys.argv) > 1:
    options = list.copy(sys.argv[1:])

# define color print
def warn(msg, end='\n', file=sys.stdout, flush=False):
    print(f'\033[0;33m{msg}\033[0m', end=end, file=file, flush=flush)

def error(msg, end='\n', file=sys.stdout, flush=False):
    print(f'\033[0;31m{msg}\033[0m', end=end, file=file, flush=flush)

# check if run as root
if os.geteuid() != 0:
    warn("Script must be run as root. Try \"sudo python3 install_ubuntu.py\".")
    sys.exit(1)

# utils
def run_command(cmd=""):
    import subprocess
    p = subprocess.Popen(cmd,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    result = p.stdout.read().decode('utf-8')
    status = p.poll()
    return status, result

errors = []
at_work_tip_sw = False

def working_tip():
    char = ['/', '-', '\\', '|']
    i = 0
    global at_work_tip_sw
    while at_work_tip_sw:
        i = (i + 1) % 4
        sys.stdout.write('\033[?25l')
        sys.stdout.write('%s\033[1D' % char[i])
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
    _thread.join()
    if status == 0 or status == None or result == "":
        print('Done')
    else:
        print('Error')
        errors.append("%s error:\n  Status:%s\n  Error:%s" % (msg, status, result))

def check_os_bit():
    _, os_bit = run_command("getconf LONG_BIT")
    return int(os_bit)

def detect_os():
    status, result = run_command("cat /etc/os-release | grep ^ID=")
    if "ubuntu" in result.lower():
        return "ubuntu"
    else:
        return "raspbian"

# check system
os_type = detect_os()
os_bit = check_os_bit()
print(f"Detected OS: {os_type} ({os_bit} bit)")

# Dependencies for Ubuntu (no raspi-config!)
APT_INSTALL_LIST = [
    "i2c-tools",
    "espeak",
    'libsdl2-dev',
    'libsdl2-mixer-dev',
    'portaudio19-dev',
    'sox',
]

# Skip TTS pico on Ubuntu for now (architecture mismatch)
# You can install it manually if needed

PIP_INSTALL_LIST = [
    'smbus2',
    'gpiozero',
    'pyaudio',
    'spidev',
    'pyserial',
    'pillow',
    "pygame>=2.1.2",
]

def enable_i2c_ubuntu():
    """Enable I2C on Ubuntu by loading kernel module"""
    # Check if i2c-dev is already loaded
    status, _ = run_command("lsmod | grep i2c_dev")
    if status != 0:
        do(msg="load i2c-dev module", cmd="modprobe i2c-dev")
        do(msg="make i2c-dev persistent", cmd="echo 'i2c-dev' >> /etc/modules")
    
    # Add user to i2c group
    status, result = run_command("whoami")
    if status == 0:
        username = result.strip()
        if username != "root":
            do(msg=f"add {username} to i2c group", cmd=f"usermod -a -G i2c {username}")

def enable_spi_ubuntu():
    """Enable SPI on Ubuntu by loading kernel module"""
    status, _ = run_command("lsmod | grep spi_bcm2835")
    if status != 0:
        do(msg="load spi module", cmd="modprobe spi_bcm2835")
        do(msg="make spi persistent", cmd="echo 'spi_bcm2835' >> /etc/modules")
    
    # Add user to spi group if it exists
    status, result = run_command("whoami")
    if status == 0:
        username = result.strip()
        if username != "root":
            status, _ = run_command("getent group spi")
            if status == 0:
                do(msg=f"add {username} to spi group", cmd=f"usermod -a -G spi {username}")

def install():
    _is_bsps = ''
    status, _ = run_command("pip3 help install|grep break-system-packages")
    if status == 0:
        _is_bsps = "--break-system-packages"

    _if_build_isolation = ""
    if "--no-build-isolation" in options:
        _if_build_isolation = "--no-build-isolation"
    
    do(msg=f"install robot_hat package {_if_build_isolation}",
       cmd=f'pip3 install ./ {_is_bsps} {_if_build_isolation}')

    if "--only-lib" not in options:
        if "--no-dep" not in options:
            print("Install dependencies with apt-get:")
            do(msg="update apt-get", cmd='apt-get update')
            
            for dep in APT_INSTALL_LIST:
                do(msg=f"install {dep}", cmd=f'apt-get install {dep} -y')
            
            print("Install dependencies with pip3:")
            if _is_bsps != '':
                print("\033[38;5;8m pip3 install with --break-system-packages\033[0m")
            
            do(msg="update pip3", cmd=f'apt-get upgrade -y python3-pip')
            
            for dep in PIP_INSTALL_LIST:
                do(msg=f"install {dep}", cmd=f'pip3 install {dep} {_is_bsps}')

        print("Setup interfaces (Ubuntu method)")
        enable_i2c_ubuntu()
        enable_spi_ubuntu()

        print("Copy dtoverlay")
        DEFAULT_OVERLAYS_PATH = "/boot/firmware/overlays/"
        LEGACY_OVERLAYS_PATH = "/boot/overlays/"
        _overlays_path = None
        
        if os.path.exists(DEFAULT_OVERLAYS_PATH):
            _overlays_path = DEFAULT_OVERLAYS_PATH
        elif os.path.exists(LEGACY_OVERLAYS_PATH):
            _overlays_path = LEGACY_OVERLAYS_PATH
        
        if _overlays_path is not None:
            do(msg="copy dtoverlay", cmd=f'cp ./dtoverlays/* {_overlays_path}')
        else:
            warn("Boot overlay path not found, skipping dtoverlay copy")

    if len(errors) == 0:
        print("\nFinished! You may need to reboot for I2C/SPI to work.")
        print("After reboot, verify with: 'ls /dev/i2c* /dev/spi*'")
    else:
        print("\n\nError happened in install process:")
        for err in errors:
            print(err)
        print("Try to fix it yourself, or contact service@sunfounder.com with this message")

if __name__ == "__main__":
    try:
        install()
    except KeyboardInterrupt:
        if len(errors) > 0:
            print("\n\nError happened in install process:")
            for err in errors:
                print(err)
            print("Try to fix it yourself, or contact service@sunfounder.com with this message")
        print("\n\nCanceled.")
    finally:
        sys.stdout.write(' \033[1D')
        sys.stdout.write('\033[?25h')
        sys.stdout.flush()
