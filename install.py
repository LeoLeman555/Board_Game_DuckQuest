import sys
import subprocess


def is_raspberry_pi():
    """Check if the system is a Raspberry Pi."""
    try:
        with open("/proc/cpuinfo", "r") as f:
            return "Raspberry Pi" in f.read()
    except FileNotFoundError:
        return False


# Upgrade pip first
subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)

# List of dependencies
common_requirements = [
    "contourpy==1.3.1",
    "cycler==0.12.1",
    "fonttools==4.55.3",
    "kiwisolver==1.4.7",
    "matplotlib==3.10.0",
    "networkx==3.4.2",
    "numpy==2.2.0",
    "packaging==24.2",
    "pillow==11.0.0",
    "psutil==6.1.1",
    "pygame==2.6.1",
    "pyparsing==3.2.0",
    "python-dateutil==2.9.0.post0",
    "six==1.17.0",
]

# Add RPi.GPIO only if running on a Raspberry Pi
if is_raspberry_pi():
    common_requirements.append("RPi.GPIO==0.7.1")

# Install dependencies
try:
    subprocess.run(
        [sys.executable, "-m", "pip", "install"] + common_requirements, check=True
    )
    print("✅ Installation completed successfully!")
except subprocess.CalledProcessError:
    print("❌ Installation failed. Check the error messages above.")
    sys.exit(1)
