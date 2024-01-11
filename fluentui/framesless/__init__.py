import platform

system = platform.system()
if system == "Darwin":
    from .macos import FramelessHelper
elif system == "Windows":
    from .windows import FramelessHelper
else:
    raise ValueError("Unknown operating system")
