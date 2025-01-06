import os
import platform
import psutil
import socket


class RaspberryPiChecker:
    """Class to verify Raspberry Pi readiness and display system information."""
    def __init__(self):
        self.system_info = {}

    def get_system_info(self):
        """Retrieve essential system information."""
        try:
            self.system_info = {
                "System": platform.system(),
                "Node Name": platform.node(),
                "Release": platform.release(),
                "Version": platform.version(),
                "Machine": platform.machine(),
                "Processor": platform.processor(),
                "CPU Count": os.cpu_count(),
                "Memory": f"{round(psutil.virtual_memory().total / (1024 * 1024), 2)} MB",
                "Disk Space": f"{round(psutil.disk_usage('/').total / (1024 * 1024), 2)} MB",
                "Python Version": platform.python_version(),
            }
        except Exception as e:
            self.system_info = {"Error": f"Unable to retrieve system information: {e}"}

    def test_connectivity(self):
        """Test internet connectivity and provide detailed error messages."""
        try:
            # Attempt to connect to Google's public DNS
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True, "Internet connectivity: OK"
        except socket.timeout:
            return False, "Timeout error: Unable to reach the server (connection timed out)."
        except socket.gaierror as e:
            return False, f"Address-related error: {e}."
        except OSError as e:
            return False, f"OS error: {e}."
        except Exception as e:
            return False, f"Unknown error: {e}."

    def display_info(self):
        """Display the system information."""
        print("\nSystem Information:")
        for key, value in self.system_info.items():
            print(f"{key}: {value}")

    def check_readiness(self):
        """Check if the Raspberry Pi is ready for use."""
        print("Testing Raspberry Pi readiness...\n")
        connected, message = self.test_connectivity()
        if connected:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
            print("Please ensure the Raspberry Pi is connected to the internet.\n")
            return
        self.get_system_info()
        self.display_info()


if __name__ == "__main__":
    checker = RaspberryPiChecker()
    checker.check_readiness()
