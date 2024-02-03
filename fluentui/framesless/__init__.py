import platform

system = platform.system()
if system == "Darwin":
    from .macos import MacOSFramelessDialog as FramelessDialog
    from .macos import MacOSFramelessMainWindow as FramelessMainWindow
    from .macos import MacOSFramelessWidget as FramelessWidget
elif system == "Windows":
    from .windows import WindowsFrameDialog as FramelessDialog
    from .windows import WindowsFramelessMainWindow as FramelessMainWindow
    from .windows import WindowsFramesWidget as FramelessWidget
else:
    raise ValueError("Unknown operating system")
