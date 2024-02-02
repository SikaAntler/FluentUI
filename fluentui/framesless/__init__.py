import platform

system = platform.system()
if system == "Darwin":
    from .macos import MacFramelessDialog as FramelessDialog
    from .macos import MacFramelessMainWindow as FramelessMainWindow
    from .macos import MacFramelessWidget as FramelessWidget
elif system == "Windows":
    from .windows import FramelessHelper
else:
    raise ValueError("Unknown operating system")
